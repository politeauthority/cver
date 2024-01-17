"""
    Cver Ingest
    Ingest
    This runs inside the kubernetes cluster and collects all the images being used in the cluster.
    It then submits those images to Cver and tags their association to the cluster.

    @todo:
        - Figure out K8s Api TLS
        - Figure out cluster id settings

"""
import logging
import logging.config
import os

import requests

from cver.shared.utils.log_config import log_config
from cver.shared.utils import misc
from cver.client.ingest.ingest_k8s import IngestK8s
from cver.client import Client as CverClient


logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Ingest:

    def __init__(self):
        self.cluster_id = 1
        self.pod_images = []

    def run(self):
        if not self.preflight_check():
            logging.error("Failed Pre flight checks, exiting.")
            exit(1)
        images = self.get_pod_images()
        self.submit_pod_images(images)
        logging.info("Completed Ingest successfully")

    def preflight_check(self) -> bool:
        """Preflight checks for ingest job run.
        @todo: Add check for kubernetes api access.
        """
        cver = CverClient()
        if cver.login():
            logging.info("Successfully authed to Cver Api: %s" % cver.api_url)
            return True
        else:
            logging.critical("Failed to auth to Cver Api: %s" % cver.api_url)
            return False

    def get_pod_images(self):
        """Get the names of all the unique images from the local Kubernetes api."""
        token = self.get_k8s_token()
        url = "https://kubernetes.default.svc.cluster.local/api/v1/pods"
        params = {
            "fieldSelector": "metadata.namespace!="
        }
        headers = {
            "Authorization": "Bearer %s" % token
        }
        response = requests.get(url, params=params, headers=headers, verify=False)
        if response.status_code != 200:
            logging.critical("Got response: %s from the Kubernetes api." % response.status_code)
            exit(1)
        print(response)
        logging.info("Recieved pod response from Kubernetes api")
        response_json = response.json()
        images = []
        for pod in response_json["items"]:
            container_number = 0
            image = {
                "name": None,
                "sha": None
            }
            for container in pod["spec"]["containers"]:
                if container["image"] not in images:
                    image["name"] = container["image"]
                    if "containerStatuses" not in pod["status"]:
                        msg = "Cannot find container status for %s. Pod is likely errored."
                        logging.error(msg % pod["metadata"]["name"])
                        continue
                    image["sha"] = pod["status"]["containerStatuses"][container_number]["imageID"]
                    image_map = misc.container_url(image["sha"])
                    sha = image_map["sha"]
                    if sha:
                        image["sha"] = sha
                    images.append(image)

                container_number += 1
        logging.info("Found %s unique images from the Kubernetes api" % len(images))
        return images

    def get_k8s_token(self):
        if not os.path.exists("/var/run/secrets/kubernetes.io/serviceaccount/token"):
            logging.critical("Cannot find service account token")
            exit(1)
        token = open("/var/run/secrets/kubernetes.io/serviceaccount/token").read()
        return token

    def submit_pod_images(self, images):
        """Submit the pod images to Cver."""
        logging.info("Submmiting %s Images for Cluster %s" % (
            len(images), self.cluster_id))
        logging.warning("Using hardcoded Cluster ID 1")
        for image in images:
            response = IngestK8s().image(self.cluster_id, image["name"], image["sha"])
            logging.info("Submitted: %s" % image)
            if response["status"] != "success":
                logging.critical("Error submitting image to Cver Api: %s" % response["message"])
                break
        return True


if __name__ == "__main__":
    Ingest().run()


# End File: cver/src/cver/ingest/ingest.py
