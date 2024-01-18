"""
    Cver Engine
    Cluster Presence

"""
import logging

from cver.client.collections.clusters import Clusters
from cver.client.collections.cluster_images import ClusterImages
from cver.client.collections.cluster_image_builds import ClusterImageBuilds
from cver.engine.utils import glow
from cver.shared.utils import date_utils


class ClusterPresence:

    def __init__(self):
        self.cluster_presence_hours = glow.engine_info["cluster_presence_hours"]
        self.data = {
            "clusters": [],
            "total_cluster_images": 0,
            "total_cluster_image_builds": 0,
        }

    def run(self):
        logging.info("Starting Cluster Presence checks.")
        logging.info("Cluster presence interval hours: %s" % self.cluster_presence_hours)
        clusters = self.get_clusters()
        for cluster in clusters:
            self.handle_cluster(cluster)
        logging.info("Ran clusrter presence successfully")
        return self.data

    def get_clusters(self):
        col_cluster = Clusters()
        return col_cluster.get()

    def handle_cluster(self, cluster):
        """
        @todo: Filter by cluster_id, last_seen_time, and currently present
        """
        self.handel_cluster_images(cluster)
        self.handel_cluster_image_builds(cluster)

    def handel_cluster_images(self, cluster):
        col_ci = ClusterImages()
        cluster_images = col_ci.get_all()
        logging.info("Found %s CluserImages for cluster %s" % (len(cluster_images), cluster))
        for cluster_image in cluster_images:
            if not cluster_image.present:
                continue
            if date_utils.interval_ready(cluster_image.last_seen, self.cluster_presence_hours):
                cluster_image.present = False
                cluster_image.save()
                logging.info("Setting %s to no longer present in cluster %s" % (
                    cluster_image, cluster))

    def handel_cluster_image_builds(self, cluster):
        col_ci = ClusterImageBuilds()
        cluster_image_builds = col_ci.get_all()
        total_for_cluster = len(cluster_image_builds)
        logging.info("Found %s CluserImageBuilds for cluster %s" % (
            total_for_cluster, cluster))
        for cluster_image_build in cluster_image_builds:
            if not cluster_image_build.present:
                continue
            interval_ready = date_utils.interval_ready(
                cluster_image_build.last_seen,
                self.cluster_presence_hours)
            if interval_ready:
                cluster_image_build.present = False
                cluster_image_build.save()
                logging.info("Setting %s to no longer present in cluster %s" % (
                    cluster_image_build, cluster))

# End File: cver/src/cver/engine/modules/cluster_presence.py
