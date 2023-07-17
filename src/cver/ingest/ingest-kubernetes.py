"""
    Cver Ingest
    Ingest Kubernetes

"""
import logging

from kubernetes import client, config

# from cver.shared.utils import misc
# from cver.cver_client.models.image import Image
# from cver.cver_client.ingest.ingest_k8s import IngestK8s


class KubernetesIngest:

    def __init__(self):
        config.load_kube_config()
        self.pod_images = ["docker.io/calico/node:v3.20.2"]

    def run(self):
        self.get_pod_images()
        self.submit_pod_images()

    def get_pod_images(self):
        """List all pod images and store them as a list."""
        v1 = client.CoreV1Api()
        logging.info("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        for i in ret.items:
            for c in i.spec.containers:
                if c.image not in self.pod_images:
                    print(c.image)
                    self.pod_images.append(c.image)
        logging.info("Found %s unique images" % len(self.pod_images))
        return True

    def submit_pod_images(self):
        cluster_id = 2
        logging.info("Submmiting %s Images for Cluster %s" % (len(self.pod_images), cluster_id))
        # for pod_image in self.pod_images:
        #     IngestK8s().image(cluster_id, pod_image)


if __name__ == "__main__":
    KubernetesIngest().run()


# End File: cver/src/cver/ingest/kubernetes_ingest.py
