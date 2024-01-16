"""
    Cver Api
    Stats
    Totals

"""
from cver.api.collects.api_keys import ApiKeys
from cver.api.collects.clusters import Clusters
from cver.api.collects.cluster_images import ClusterImages
from cver.api.collects.images import Images
from cver.api.collects.image_builds import ImageBuilds
from cver.api.collects.image_build_pulls import ImageBuildPulls
from cver.api.collects.image_build_waitings import ImageBuildWaitings
from cver.api.collects.migrations import Migrations
from cver.api.collects.options import Options
from cver.api.collects.organizations import Organizations
from cver.api.collects.perms import Perms
from cver.api.collects.registries import Registries
from cver.api.collects.role_perms import RolePerms
from cver.api.collects.roles import Roles
from cver.api.collects.users import Users
from cver.api.collects.scans import Scans
from cver.api.collects.scanners import Scanners
from cver.api.collects.softwares import Softwares
from cver.api.collects.tasks import Tasks


def get_model_totals():
    ret = {
        "api-keys": ApiKeys().get_count_total(),
        "apps": Softwares().get_count_total(),
        "clusters": Clusters().get_count_total(),
        "cluster-images": ClusterImages().get_count_total(),
        "images": Images().get_count_total(),
        "image-builds": ImageBuilds().get_count_total(),
        "image-build-pulls": ImageBuildPulls().get_count_total(),
        "image-build-waitings": ImageBuildWaitings().get_count_total(),
        "migrations": Migrations().get_count_total(),
        "options": Options().get_count_total(),
        "organizations": Organizations().get_count_total(),
        "perms": Perms().get_count_total(),
        "registries": Registries().get_count_total(),
        "role_perms": RolePerms().get_count_total(),
        "roles": Roles().get_count_total(),
        "users": Users().get_count_total(),
        "scans": Scans().get_count_total(),
        "scan_raw": Scans().get_count_total(),
        "scanners": Scanners().get_count_total(),
        "tasks": Tasks().get_count_total(),
    }
    total_totals = 0
    for key, value in ret.items():
        total_totals += value
    ret["total_totals"] = total_totals
    return ret


# End File: cver/src/api/stats/totals.py
