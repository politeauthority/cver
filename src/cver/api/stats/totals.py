"""
    Cver Api - Stats
    Totals

"""
from cver.api.collects.api_keys import ApiKeys
from cver.api.collects.softwares import Softwares
from cver.api.collects.images import Images
from cver.api.collects.image_builds import ImageBuilds
from cver.api.collects.image_build_waitings import ImageBuildWaitings
from cver.api.collects.cluster_images import ClusterImages
from cver.api.collects.migrations import Migrations
from cver.api.collects.options import Options
from cver.api.collects.perms import Perms
from cver.api.collects.role_perms import RolePerms
from cver.api.collects.roles import Roles
from cver.api.collects.users import Users
from cver.api.collects.scans import Scans
from cver.api.collects.scanners import Scanners


def get_model_totals():
    ret = {
        "api-keys": ApiKeys().get_count_total(),
        "apps": Softwares().get_count_total(),
        "cluster-images": ClusterImages().get_count_total(),
        "images": Images().get_count_total(),
        "image-builds": ImageBuilds().get_count_total(),
        "image-build-waitings": ImageBuildWaitings().get_count_total(),
        "migrations": Migrations().get_count_total(),
        "options": Options().get_count_total(),
        "perms": Perms().get_count_total(),
        "role_perms": RolePerms().get_count_total(),
        "roles": Roles().get_count_total(),
        "users": Users().get_count_total(),
        "scans": Scans().get_count_total(),
        "scan_raw": Scans().get_count_total(),
        "scanners": Scanners().get_count_total(),
    }
    return ret

# End File: cver/src/api/stats/totals.py
