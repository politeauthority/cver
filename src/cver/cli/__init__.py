"""
    Cver Cli
    Primary entrypoint to cli script.

"""
import logging
import logging.config
import sys

from cver.shared.utils.log_config import log_config
from cver.shared.utils import display
from cver.cver_client.collections.image_builds import ImageBuilds
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.cver_client.collections.scans import Scans
from cver.cver_client import CverClient

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Cver:

    def run(self, verb, noun, entity_id: int = None):

        if noun == "info":
            self.get_info()
        if noun == "image":
            self.get_image(entity_id)
        elif noun in ["ib", "image-build"]:
            self.get_image_buld(entity_id)
        elif noun in ["ibw", "image-build-waiting"]:
            self.get_image_buld_waiting(entity_id)

    def get_info(self):
        client = CverClient()
        print(client.info())
        import ipdb; ipdb.set_trace()

    def get_image(self, image_id):
        """Get a single Image."""
        image = Image()
        image.get_by_id(image_id)
        ibs_collect = ImageBuilds()
        scans_collect = Scans()
        ibs = ibs_collect.get_by_image_id(image_id)
        ibws = ImageBuildWaitings().get_by_image_id(image_id)
        # scans = Scans().get({"image_id": image_id})
        image_dict = {
            "ID": image.id,
            "Created": image.created_ts,
            "Name": image.name,
            "Registry": image.registry,
            "Image Builds": len(ibs),
            "Image Builds Waiting": len(ibws)
        }
        display.print_dict(image_dict)
        if ibs:
            print("")
            print("Image Builds")
            for ib in ibs:
                scans = scans_collect.get_by_image_build_id(ib.id)
                ib_dict = {
                    "ID": ib.id,
                    "Sha": ib.sha,
                    "Registry": ib.registry,
                    "Registry Imported": ib.registry_imported,
                    "Tags": ", ".join(ib.tags),
                    "Scans": len(scans),
                }
                display.print_dict(ib_dict, 2)
            print("")
        if ibws:
            print("")
            print("Image Builds Waiting")
            for ibw in ibws:
                ibw_dict = {
                    "ID": ibw.id,
                    "Sha": ibw.sha,
                    "Tag": ibw.tag,
                    "Waiting": ibw.waiting,
                    "Waiting For": ibw.waiting_for,
                    "Status": ibw.status,
                }
                display.print_dict(ibw_dict, 2)
            print("")

    def get_image_buld(self, ibw_id: int):
        """Get a single ImageBuild."""
        ib = ImageBuild()
        ib.get_by_id(ibw_id)
        image = Image()
        image.get_by_id(ib.image_id)
        scans_collect = Scans()
        scans = scans_collect.get_by_image_build_id(ib.id)
        print("ImageBuild")
        print("ID:\t\t%s" % ib.id)
        print("Created:\t%s" % ib.created_ts)
        print("Updated:\t%s" % ib.updated_ts)
        print("Image ID:\t%s" % ib.image_id)
        print("Scans: %s" % len(scans))
        print("")
        print("Image")
        print(f"\t\tID:       {image.id}")
        print(f"\t\tName:     {image.name}")
        print(f"\t\tRegistry: {image.registry}")
        print("")

    def get_image_buld_waiting(self, ibw_id: int):
        ibw = ImageBuildWaiting()
        ibw.get_by_id(ibw_id)
        image = Image()
        image.get_by_id(ibw.image_id)
        has_ib = False
        if ibw.image_build_id:
            ib = ImageBuild()
            has_ib = ib.get_by_id(ibw.image_build_id)
        print("ImageBuildWaiting")
        print("ID:\t\t%s" % ibw.id)
        print("Created:\t%s" % ibw.created_ts)
        print("Updated:\t%s" % ibw.updated_ts)
        print("Image ID:\t%s" % ibw.image_id)
        print("Image Build ID:\t%s" % ibw.image_build_id)
        print("Waiting:\t%s" % ibw.waiting)
        print("Waiting For:\t%s" % ibw.waiting_for)
        print("")
        print("Image")
        print(f"\t\tID:       {image.id}")
        print(f"\t\tName:     {image.name}")
        print(f"\t\tRegistry: {image.registry}")
        print("")
        if has_ib:
            print("Image Build")
            print(f"\t\tID:\t{ib.id}")
            print(f"\t\tSha:                {ib.sha}")
            print("\t\tTags:               %s" % ", ".join(ib.tags))
            print(f"\t\tRegistry Imported: {ib.registry_imported}")


if __name__ == "__main__":
    verb = sys.argv[1]
    noun = sys.argv[2]
    entity_id = None
    if len(sys.argv) > 3:
        entity_id = sys.argv[3]
    Cver().run(verb, noun, entity_id)

# End File: cver/src/cver/cli/__init__.py
