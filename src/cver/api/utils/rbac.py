"""
    Rbac Utilities

"""
import logging

from cver.api.utils import glow

ACL = {
    "/": {
        "GET": ["read-all"],
    },
    "/info": {
        "GET": ["read-all"],
    },
    "/app": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/apps": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/api-key": {
        "GET": ["read-all", "get-api-key"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/api-keys": {
        "GET": ["read-all", "get-api-key"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/cluster": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/clusters": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/cluster-image": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/cluster-images": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/image": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/images": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/image-build": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/image-builds": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/image-build-waiting": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/image-build-waitings": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/migrations": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/option": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/options": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/perm": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/perms": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/roles": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role-perm": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/role-perms": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan-raw": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan-raws": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scan": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scans": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scanner": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/scanners": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/submit-scan": {
        "POST": ["write-all", "write-scan"],
    },
    "/ingest-k8s/image": {
        "POST": ["write-all", "write-scan"],
    },
    "/ingest-k8s": {
        "POST": ["write-all", "write-scan"],
    },
    "/user": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
    "/users": {
        "GET": ["read-all"],
        "POST": ["write-all"],
        "DELETE": ["write-all"],
    },
}


def check_role_uri_access(user_role_perms: list, request) -> bool:
    """Checks a list of user role perms against the ACL list, checking to see if they line up.
    @todo: Unit test this, it's BRITTLE AF
    """
    rp_og = request.path
    if rp_og.count("/") > 1:
        rp = rp_og[rp_og.find("/"):rp_og.rfind("/")]
    else:
        rp = rp_og

    if rp not in ACL:
        logging.warning("Request path: %s not in ACL" % rp)
        return False
    acl_route = ACL[rp]
    rm = request.method
    if request.method not in acl_route:
        logging.warning("Request method: %s not in ACL path: %s" % (rm, rp))
        return False
    acl_route_method = acl_route[rm]
    # print("has %s:" % user_role_perms)
    # print("needs %s:" % acl_route_method)
    for perm in acl_route_method:
        if perm in user_role_perms:
            return True
    return False


def get_perms_by_role_id(role_id: int) -> list:
    """Get all enabled RolePerm slug names for a given Role id."""
    sql = """
    SELECT `p`.name, `p`.slug_name
    FROM `roles` as r
    JOIN `role_perms` as rp
        ON `r`.id = `rp`.role_id
    JOIN `perms` as p
        ON `rp`.perm_id = `p`.id
    WHERE
        r.id = %s
        AND
        `rp`.enabled = 1;

    """ % role_id
    glow.db["cursor"].execute(sql)
    res = glow.db["cursor"].fetchall()
    role_perms = []
    for rp in res:
        role_perms.append(rp[1])
    return role_perms

# End File: cver/src/api/utils/rbac.py
