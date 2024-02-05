"""
    Cver Engine
    Engine Priority
        Download
            - Images within active clusters without a scan
"""
import logging

from cver.engine.utils import glow
from cver.client.models.image_build import ImageBuild
from cver.client.models.image_build_pull import ImageBuildPull
from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.cluster_image_builds import ClusterImageBuilds
# from cver.engine.utils import glow
# from cver.shared.utils import date_utils

logger = logging.getLogger("cver")


class EnginePriority:

    def __init__(self):
        self.images = {}
        self.image_builds = {}
        self.cluster_image_builds = {}
        self.registries = glow.registry_info["registries"]
        self.local_registry = glow.registry_info["local"]
        self.data = {}

    def run(self, phase: str) -> dict:
        logging.info("Determining Engine Priority")
        if phase == "download":
            logging.info("Determining Engine Priority - Download")
            self.get_download_priority()
        elif phase == "scan":
            logging.info("Determining Engine Priority - Scan")
            self.get_scan_priority()
        return self.data

    def get_download_priority(self) -> bool:
        """
        """
        self.get_image_builds()
        self.get_cluster_image_builds()
        self.images = {}
        for ib_id, ib in self.image_builds.items():
            self.images[ib_id] = {
                "score": 0,
                "image_build": ib
            }
            self.score_image_build_download(ib)
        sorted_by_score = dict(sorted(self.images.items(), key=lambda item: item[1]["score"], reverse=True))
        self.data["download"] = sorted_by_score
        # import ipdb; ipdb.set_trace()
        return True

    def get_scan_priority(self) -> bool:
        """Create the Engine Scan priorty list based off the most recent information.
        """
        print("hiya")
        # import ipdb; ipdb.set_trace()
        # self.get_image_builds()
        # self.get_cluster_image_builds()

        return True

    def get_image_builds(self) -> bool:
        """Get all Images Builds, which are Image Builds we assume to be active live currently in
        a cluster.
        """
        col_ibs = ImageBuilds()
        ibs = col_ibs.get_all()
        for ib in ibs:
            if ib.id not in self.image_builds:
                self.image_builds[ib.id] = ib
        return True

    def get_cluster_image_builds(self):
        """Get all CLuster Images, which are Image Builds we assume to be active live currently in
        a cluster.

        @ todo: filter on enabled clusters and enabled image_builds
        """
        col_cibs = ClusterImageBuilds()
        cibs = col_cibs.get_all()
        for ci_ib in cibs:
            if ci_ib.id not in self.cluster_image_builds:
                self.cluster_image_builds[ci_ib.id] = ci_ib
        return True

    def score_image_build_download(self, ib: ImageBuild) -> True:
        """Score an Image Build.
        """
        ibp = self.get_image_build_pull(ib.id)

        # If we we've had a success ImageBuildPull, score this 0 and return.
        if ibp.status_download:
            self.images[ib.id]["score"] = 0
            return True

        # Check the registry details
        ib_registry = self.registries[ib.registry_id]
        # If the registry is the local url
        if ib_registry.url == self.local_registry["url"]:
            self.images[ib.id]["score"] += 200
            print(ib_registry.url_pull_thru)

        if ib_registry.url_pull_thru and ib_registry.url_pull_thru != "":
            # If the registry has a pull though give 100 points
            self.images[ib.id]["score"] += 100

        for cib_id, cib in self.cluster_image_builds.items():
            if cib.image_build_id != ib.id:
                continue
            if cib.present:
                self.images[ib.id]["score"] += 100
        return True

    def get_image_build_pull(self, image_build_id: int) -> ImageBuildPull:
        ibp = ImageBuildPull()
        ibp.get_by_field("image_build_id", image_build_id)
        return ibp


# End File: cver/src/cver/engine/modules/engine_priorty.py
