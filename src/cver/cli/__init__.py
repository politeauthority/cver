"""
    Cver Cli
    Primary entrypoint to cli script.

"""
import argparse
import logging
import logging.config

from rich.console import Console
from rich.table import Table


from cver.api.version import version as cver_version
from cver.shared.utils.log_config import log_config
from cver.shared.utils import display
from cver.client.collections.images import Images
# from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.image_build_pulls import ImageBuildPulls
from cver.client.collections.options import Options
from cver.client.collections.registries import Registries
from cver.client.collections.tasks import Tasks
from cver.client.collections.users import Users
from cver.client.models.image import Image
from cver.client.models.image_build import ImageBuild
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.client.models.option import Option
from cver.client.models.task import Task
from cver.client.models.scan import Scan
from cver.client.collections.scans import Scans
from cver.client import Client as CverClient
from cver.cli.utils import pretty
from cver.cli.utils import misc


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
        # self.client = CverClient(config=self.args.config)
        self.client = CverClient()

    def run(self):
        """Primary entrypoint to the Cver Cli."""
        if self.args.verb == "get":
            self.gets()
        elif self.args.verb == "edit":
            self.edits()
        elif self.args.verb == "delete":
            self.deletes()
        else:
            print("Error: Unknown Command")
            exit(1)

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
        elif self.args.noun in ["ibps", "image-build-pulls"]:
            self.get_image_build_pulls()
        elif self.args.noun in ["ibp", "image-build-pull"]:
            self.get_image_build_pull()
        elif self.args.noun in ["options"]:
            self.get_options()
        elif self.args.noun in ["registries"]:
            self.get_registries()
        elif self.args.noun in ["scans"]:
            self.get_scans()
        elif self.args.noun in ["tasks"]:
            self.get_tasks()
        elif self.args.noun in ["task"]:
            self.get_task()
        elif self.args.noun in ["users"]:
            self.get_users()
        else:
            print("Error: Unknown Command")
            exit(1)
        return True

    def edits(self) -> bool:
        """Edit actions router."""
        if self.args.noun in ["option"]:
            self.edit_option()
        else:
            print("Error: Unknown Command")
            exit(1)
        return True

    def deletes(self) -> bool:
        """Delete actions router."""
        if self.args.noun in ["task"]:
            self.delete_task()
        elif self.args.noun in ["scan"]:
            self.delete_scan()
        else:
            print("Error: Unknown Command")
            exit(1)
        return True

    def get_info(self) -> bool:
        """Get Cver info
        :cmd: cver-cli get info
        """
        client = CverClient()
        info = client.info()
        table = Table(title="Totals")
        table.add_column("Model", justify="right", style="cyan", no_wrap=True)
        table.add_column("Total", justify="right", style="green")

        table.add_row("Api Keys", str(info["model_totals"]["api-keys"]))
        table.add_row("Apps", str(info["model_totals"]["apps"]))
        table.add_row("Cluster Images", str(info["model_totals"]["cluster-images"]))
        table.add_row("Images", str(info["model_totals"]["images"]))
        table.add_row("Image Builds", str(info["model_totals"]["image-builds"]))
        table.add_row("Image Build Waitings", str(info["model_totals"]["image-build-waitings"]))
        table.add_row("Migrations", str(info["model_totals"]["migrations"]))
        table.add_row("Options", str(info["model_totals"]["options"]))
        table.add_row("Perms", str(info["model_totals"]["perms"]))
        table.add_row("Role Perms", str(info["model_totals"]["role_perms"]))
        table.add_row("Roles", str(info["model_totals"]["roles"]))
        table.add_row("Scanners", str(info["model_totals"]["scanners"]))
        table.add_row("Scans", str(info["model_totals"]["scans"]))
        table.add_row("Tasks", str(info["model_totals"]["tasks"]))
        table.add_row("Users", str(info["model_totals"]["users"]))

        console = Console()
        console.print(table)

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
        pretty.entity_table(image)
        return True

    def get_images(self) -> bool:
        """Get all Images."""
        # filters = self.args.filters
        image_col = Images()
        images = image_col.get(page=self.args.page)
        response = image_col.response_last
        rj = response.json()
        if response.status_code != 200:
            print("Error making request")
            exit(1)

        print("Images (%s)" % rj["info"]["total_objects"])
        images_dict = {}
        for image in images:
            images_dict[image.id] = image.name

        display.print_dict(images_dict, pad=2)
        display.print_pagination_info(rj)
        return True

    def get_image_build(self) -> bool:
        """Get a single ImageBuild."""
        ib = ImageBuild()
        ib.get_by_id(self.args.selector)
        image = Image()
        image.get_by_id(ib.image_id)
        pretty.entity_table(ib)
        pretty.entity_table(image)
        return True

    def get_image_build_pulls(self) -> bool:
        """Get all ImageBuildPulls."""
        entity_col = ImageBuildPulls()
        ibps = entity_col.get(page=self.args.page)
        response = entity_col.response_last
        rj = response.json()

        table = Table(title="Image Build Pulls (%s)" % rj["info"]["total_objects"])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Image", justify="left", style="green")
        table.add_column("Image Build ID", justify="left", style="green")
        table.add_column("Created", justify="right", style="green")

        for ibw in ibps:
            image = Image()
            image.get_by_id(ibw.image_id)
            table.add_row(
                str(ibw.id),
                image.name,
                str(ibw.image_build_id),
                pretty.date_display(ibw.created_ts)
            )

        console = Console()
        console.print(table)
        pretty.print_pagination(rj["info"])
        return True

    def get_image_buld_waiting(self):
        ibw = ImageBuildWaiting()
        ibw.get_by_id(self.args.selector)
        print(self.args.selector)
        # image = Image()
        # image.get_by_id(ibw.response_last)
        # has_ib = False
        # if ibw.image_build_id:
        #     ib = ImageBuild()
        #     has_ib = ib.get_by_id(ibw.image_build_id)
        pretty.entity_table(ibw)
        # print("ImageBuildWaiting")
        # print("ID:\t\t%s" % ibw.id)
        # print("Created:\t%s" % ibw.created_ts)
        # print("Updated:\t%s" % ibw.updated_ts)
        # print("Image ID:\t%s" % ibw.image_id)
        # print("Image Build ID:\t%s" % ibw.image_build_id)
        # print("Waiting:\t%s" % ibw.waiting)
        # print("Waiting For:\t%s" % ibw.waiting_for)
        # print("")
        # print("Image")
        # print(f"\t\tID:       {image.id}")
        # print(f"\t\tName:     {image.name}")
        # print(f"\t\tRegistry: {image.registry}")
        # print("")
        # if has_ib:
        #     print("Image Build")
        #     print(f"\t\tID:\t{ib.id}")
        #     print(f"\t\tSha:                {ib.sha}")
        #     print("\t\tTags:               %s" % ", ".join(ib.tags))
        #     print(f"\t\tRegistry Imported: {ib.registry_imported}")
        return True

    def get_options(self) -> bool:
        """Get all Options."""
        entity_col = Options()
        options = entity_col.get(page=self.args.page)
        rj = entity_col.response_last_json
        # if response:
        #     print("Error: Could not fetch options")
        #     return False

        table = Table(title="Options  (%s)" % rj["info"]["total_objects"])
        table.add_column("Name", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", justify="right", style="green")
        for option in options:
            table.add_row(option.name, str(option.value))

        console = Console()
        console.print(table)
        print("\n")
        print("Info")
        print("\tPage: %s/%s" % (rj["info"]["current_page"], rj["info"]["last_page"]))
        print("\tPer Page: %s" % rj["info"]["per_page"])
        return True

    def get_registries(self) -> bool:
        """Get all Regiestries."""
        entity_col = Registries()
        registries = entity_col.get(page=self.args.page)
        rj = entity_col.response_last_json

        table = Table(title="Tasks (%s)" % rj["info"]["total_objects"])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Name", justify="right", style="green")
        table.add_column("Url", justify="right", style="green")
        table.add_column("Pull-Thru", justify="right", style="green")

        for registry in registries:
            table.add_row(str(registry.id), registry.name, registry.url, registry.url_pull_thru)

        console = Console()
        console.print(table)
        pretty.print_pagination(rj["info"])
        return True

    def get_tasks(self) -> bool:
        """Get all Tasks."""
        entity_col = Tasks()
        tasks = entity_col.get(page=self.args.page)
        rj = entity_col.response_last_json

        table = Table(title="Tasks (%s)" % rj["info"]["total_objects"])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Task", justify="right", style="green")
        table.add_column("Image", justify="right", style="green")
        table.add_column("Created", justify="right", style="green")
        table.add_column("Status", justify="right", style="green")
        table.add_column("Status Reason", justify="right", style="green")

        for task in tasks:
            image = Image()
            image.get_by_id(task.image_id)
            table.add_row(
                str(task.id),
                task.name,
                image.name,
                pretty.date_display(task.created_ts),
                str(task.status),
                task.status_reason,
            )

        console = Console()
        console.print(table)
        pretty.print_pagination(rj["info"])
        return True

    def get_task(self) -> bool:
        """Get a single Task."""
        task = Task()
        task_search = self.args.selector
        if not task.get_by_id(task_search):
            print("Not Found")
            return False
        image = Image()
        image.get_by_id(task.image_id)
        ib = ImageBuild()
        ib.get_by_id(task.image_build_id)
        console.print("Task", style="bold")
        pretty.entity_table(task)
        pretty.entity_table(image)
        pretty.entity_table(ib)
        return True

    def get_scans(self) -> bool:
        """Get all Scans."""
        entity_col = Scans()
        collect_args = misc.collect_args(self.args)
        collect_args["query"] = True
        collect_args["limit"] = 5
        scans = entity_col.get(collect_args)
        rj = entity_col.response_last_json

        table = Table(title="Scans (%s)" % rj["info"]["total_objects"])
        table.add_column("ID", justify="right", style="cyan", no_wrap=True)
        table.add_column("Image", justify="left", style="green")
        table.add_column("Critical CVEs", justify="right", style="red")
        table.add_column("High CVEs", justify="right", style="red")
        table.add_column("Medium CVEs", justify="right", style="yellow")
        table.add_column("Low CVEs", justify="right", style="black")

        for scan in scans:
            image = Image()
            image.get_by_id(scan.image_id)
            table.add_row(
                str(scan.id),
                image.name,
                str(scan.cve_critical_int),
                str(scan.cve_high_int),
                str(scan.cve_medium_int),
                str(scan.cve_low_int),
            )
        console = Console()
        console.print(table)
        pretty.print_pagination(rj["info"])
        return True

    def edit_option(self) -> bool:
        """Edit an Option.
        @note: Currently only works with the selector as a name value.
        """
        print("This hasnt been built yet")
        option = Option()
        option_search = self.args.selector
        if not option.get_by_name(option_search):
            print("Error: Could not find option: %s" % option_search)
            return False
        print("Option: %s")
        print("\tCurrent Value:\t%s" % option.value)
        new_value = input("\tNew Value:\t")
        validate = input("Save?\t")
        if validate in ["y", "yes"]:
            option.value = new_value
            if option.save():
                print("Saved: %s" % option)
            else:
                print("Error Saving: %s" % option)
                return False
        else:
            print("Not saving")
        return True

    def delete_task(self) -> bool:
        task = Task()
        task_search = self.args.selector
        if not task.get_by_id(task_search):
            print("Not Found")
            return False
        console.print("Task", style="bold")
        pretty.entity(task)
        validate = input("Delete?\t")
        if validate in ["y", "yes"]:
            if task.delete():
                print("Deleted: %s" % task)
            else:
                print("Error Saving: %s" % task)
                return False
        else:
            print("Not saving")

    def delete_scan(self):
        entity = Scan()
        entity_search = self.args.selector
        if not entity.get_by_id(entity_search):
            print("Not Found")
            return False
        console.print("Scan", style="bold")
        pretty.entity(entity)
        validate = input("Delete?\t")
        if validate in ["y", "yes"]:
            if entity.delete():
                print("Deleted: %s" % entity)
            else:
                print("Error Saving: %s" % entity)
                return False
        else:
            print("Not saving")

    def get_users(self):
        col = Users()
        users = col.get(page=self.args.page)
        response = col.response_last
        rj = response.json()
        if response.status_code != 200:
            print("Error making request")
            exit(1)

        # import ipdb; ipdb.set_trace()

        print("Users (%s)" % rj["info"]["total_objects"])
        the_dict = {}
        for user in users:
            the_dict[user.id] = user.name

        display.print_dict(the_dict, pad=2)
        display.print_pagination_info(rj)
        return True


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
    parser.add_argument('-c', '--config', default=None)
    parser.add_argument('-f', '--filter', default=None)
    parser.add_argument(
        "o",
        nargs='?',
        default=None,
        help="Output")
    parser.add_argument('-o', '--output', default=None)
    parser.add_argument('--order', default=None)
    # parser.add_argument('--delete-token', default=None)
    the_args = parser.parse_args()
    return the_args


if __name__ == "__main__":
    console.print(LOGO, style="bold red")
    console.print("                  %s\n" % cver_version)
    args = parse_args()
    Cver(args).run()

# End File: cver/src/cver/cli/__init__.py
