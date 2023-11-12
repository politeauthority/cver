"""
    Cver Cli
    Primary entrypoint to cli script.

"""
import argparse
import logging
import logging.config

from rich.console import Console

from cver.api.version import version as cver_version
from cver.shared.utils.log_config import log_config
from cver.shared.utils import display
from cver.client.collections.images import Images
from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.image_build_waitings import ImageBuildWaitings
from cver.client.collections.options import Options
from cver.client.collections.tasks import Tasks
from cver.client.models.image import Image
from cver.client.models.image_build import ImageBuild
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.client.models.task import Task
# from cver.client.collections.scans import Scans
from cver.client import Client as CverClient
from cver.cli.utils import pretty

LOGO = """
   ______
  / ____/   _____  _____
 / /   | | / / _ \/ ___/
/ /___ | |/ /  __/ /
\____/ |___/\___/_/
"""

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True

console = Console()


class Cver:

    def __init__(self, cli_args):
        self.args = cli_args
        self.client = CverClient()

    def run(self):
        """Primary entrypoint to the Cver Cli."""
        if self.args.verb == "get":
            self.gets()

    def gets(self):
        if self.args.noun == "info":
            self.get_info()
        elif self.args.noun == "image":
            self.get_image()
        elif self.args.noun == "images":
            self.get_images()
        elif self.args.noun == "image":
            self.get_image()
        elif self.args.noun in ["ib", "image-build"]:
            self.get_image_build()
        elif self.args.noun in ["ibw", "image-build-waiting"]:
            self.get_image_buld_waiting()
        elif self.args.noun in ["options"]:
            self.get_options()
        elif self.args.noun in ["tasks"]:
            self.get_tasks()
        elif self.args.noun in ["task"]:
            self.get_task()
        else:
            print("Error: Unknown Command")
            exit(1)
        return True

    def get_info(self):
        client = CverClient()
        info = client.info()
        info_base = {
            "env": info["env"],
            "migration": info["migration"],
        }
        info_totals = {
            "api-keys": info["model_totals"]["api-keys"],
            "apps": info["model_totals"]["apps"],
            "cluster-images": info["model_totals"]["cluster-images"],
            "image-build-waitings": info["model_totals"]["image-build-waitings"],
            "image-builds": info["model_totals"]["image-builds"],
            "images": info["model_totals"]["images"],
            "migrations": info["model_totals"]["migrations"],
            "options": info["model_totals"]["options"],
            "perms": info["model_totals"]["perms"],
            "role_perms": info["model_totals"]["role_perms"],
            "roles": info["model_totals"]["roles"],
            "scanners": info["model_totals"]["scanners"],
            "scans": info["model_totals"]["scans"],
            "tasks": info["model_totals"]["tasks"],
            "users": info["model_totals"]["users"],
        }
        display.print_dict(info_base)
        print("Totals")
        display.print_dict(info_totals, pad=2)
        return True

    def get_image(self) -> bool:
        """Get a single Image."""
        image = Image()
        image_search = self.args.selector
        if image_search and image_search.isdigit():
            if not image.get_by_id(image_search):
                print("Not Found")
                return False
        else:
            if not image.get_by_name(image_search):
                print("Not Found")
                return False
        ibs_collect = ImageBuilds()
        # scans_collect = Scans()
        ibs = ibs_collect.get_by_image_id(image.id)
        ibws = ImageBuildWaitings().get_by_image_id(image.id)
        # scans = Scans().get({"image_id": image_id})
        image_dict = {
            "ID": image.id,
            "Created": image.created_ts,
            "Name": image.name,
            "Registry": image.registry,
            "Image Builds": len(ibs),
            "Image Builds Waiting": len(ibws)
        }
        console.print("Image", style="bold")
        display.print_dict(image_dict)

    def get_images(self):
        """Get all Images."""
        # filters = self.args.filters
        # import ipdb; ipdb.set_trace()
        image_col = Images()
        images = image_col.get(page=self.args.page)
        response = image_col.response_last

        print("Images (%s)" % response["info"]["total_objects"])
        for image in images:
            print("\t%s" % image.name)

        print("\n")
        print("Info")
        print("\tPage: %s/%s" % (response["info"]["current_page"], response["info"]["last_page"]))
        print("\tPer Page: %s" % response["info"]["per_page"])

    def get_image_build(self):
        """Get a single ImageBuild."""
        ib = ImageBuild()
        ib.get_by_id(self.args.selector)
        image = Image()
        image.get_by_id(ib.image_id)
        # scans_collect = Scans()
        # scans = scans_collect.get_by_image_build_id(ib.id)
        ib_build = {
            "ID": ib.id,
            "Created": ib.created_ts,
            "Updated": ib.updated_ts,
            "Sha": ib.sha,
            "Sha Imported": ib.sha_imported,
            "Image ID": ib.image_id,
            "Reg": ib.registry,
            "Reg Imported": ib.registry_imported
        }
        console.print("ImageBuild", style="bold")
        display.print_dict(ib_build)

        # print("Scans: %s" % len(scans))
        # print("")
        # print("Image")
        # print(f"\t\tID:       {image.id}")
        # print(f"\t\tName:     {image.name}")
        # print(f"\t\tRegistry: {image.registry}")
        # print("")

    def get_image_buld_waiting(self):
        ibw = ImageBuildWaiting()
        ibw.get_by_id(self.args.selector)
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

    def get_options(self):
        """Get all Options."""
        entity_col = Options()
        options = entity_col.get(page=self.args.page)
        response = entity_col.response_last

        console.print("Options (%s)" % response["info"]["total_objects"], style="bold")

        msg = ""
        for option in options:
            msg += "[b]%s[/b]\t%s\n" % (option.name, option.value)
        console.print(msg)
        print("\n")
        print("Info")
        print("\tPage: %s/%s" % (response["info"]["current_page"], response["info"]["last_page"]))
        print("\tPer Page: %s" % response["info"]["per_page"])

    def get_tasks(self):
        """Get all Tasks."""
        entity_col = Tasks()
        tasks = entity_col.get(page=self.args.page)
        response = entity_col.response_last

        console.print("Tasks (%s)" % response["info"]["total_objects"], style="bold")

        for task in tasks:
            data = {
                "ID": task.id,
                "Created": pretty.date_display(task.created_ts),
                "Updated": task.updated_ts,
                "Name": task.name,
                "Image ID": task.image_id,
                "Image Build ID": task.image_build_id,
                "Image Build Waiting ID": task.image_build_waiting_id,
                "Status": task.status,
                "Status Reason": task.status_reason
            }
            display.print_dict(data, pad=2)
            print("\n")

        print("\n")
        print("Info")
        print("\tPage: %s/%s" % (response["info"]["current_page"], response["info"]["last_page"]))
        print("\tPer Page: %s" % response["info"]["per_page"])

    def get_task(self) -> bool:
        """Get a single Task."""
        task = Task()
        task_search = self.args.selector
        if not task.get_by_id(task_search):
            print("Not Found")
            return False
        console.print("Task", style="bold")
        pretty.entity(task)


def parse_args():
    """Parse the CLI arguments."""
    parser = argparse.ArgumentParser(description="Cver Cli")
    parser.add_argument("verb", type=str)
    parser.add_argument("noun", type=str)
    parser.add_argument(
        "selector",
        nargs='?',
        default=None,
        help='Item selector (name or id)')
    parser.add_argument(
        "page",
        nargs='?',
        default=None,
        help='Item selector (name or id)')
    parser.add_argument('-p', '--page', default=None)
    parser.add_argument(
        "filter",
        nargs='?',
        default=None,
        help='Allows filtering of results')
    parser.add_argument('-f', '--filter', default=None)
    parser.add_argument(
        "o",
        nargs='?',
        default=None,
        help="Output")
    parser.add_argument('-o', '--output', default=None)
    the_args = parser.parse_args()
    return the_args


if __name__ == "__main__":
    console.print(LOGO, style="bold red")
    console.print("                  %s\n" % cver_version)
    args = parse_args()
    Cver(args).run()

# End File: cver/src/cver/cli/__init__.py
