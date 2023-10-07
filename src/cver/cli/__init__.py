"""
    Cver Cli
    Primary entrypoint to cli script.

"""
import logging
import logging.config
import sys

from cver.shared.utils.log_config import log_config
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
# from cver.cver_client.collections.scans import Scans

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Cver:

    def run(self, verb, noun, entity_id: int):

        if noun == "image":
            self.get_image(entity_id)
        elif noun == "ibw":
            self.get_image_buld_waiting(entity_id)

    def get_image(self, image_id):
        image = Image()
        image.get_by_id(image_id)
        # scans = Scans().get({"image_id": image_id})
        print("Image")
        print("ID:\t\t%s" % image.id)
        print("Name:\t\t%s" % image.name)
        print("Registry:\t%s" % image.registry)

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
    Cver().run(sys.argv[1], sys.argv[2], sys.argv[3])

# End File: cver/src/cver/cli/__init__.py
