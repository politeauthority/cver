"""
    Cver Engine
    Engine Priority
        Download
            - Images within active clusters without a scan
"""
import logging

# from cver.client.collections.clusters import Clusters
# from cver.client.collections.cluster_images import ClusterImages
from cver.client.collections.cluster_image_builds import ClusterImageBuilds
# from cver.engine.utils import glow
# from cver.shared.utils import date_utils


class EnginePriority:

    def __init__(self):
        self.cluster_image_builds = {}
        self.data = {}

    def run(self, phase: str) -> dict:
        logging.info("Determining Engine Priority")
        if phase == "download":
            logging.info("Determining Engine Priority - Download")
            self.get_download_priority()

    def get_download_priority(self):
        """
        @ todo: filter on enabled clusters and enabled image_builds
        """
        self.get_cluster_image_builds()

    def get_cluster_image_builds(self):
        """Get all CLuster Images, which are Image Builds we assume to be active live currently in
        a cluster.

        @ todo: filter on enabled clusters and enabled image_builds
        """
        col_ibs = ClusterImageBuilds()
        cibs = col_ibs.get_all()
        for ci_ib in cibs:
            if ci_ib.id not in self.cluster_image_builds:
                self.cluster_image_builds[ci_ib.id] = ci_ib
        return True

# End File: cver/src/cver/engine/modules/engine_priorty.py
