"""
    Cver Test Unit
    Api Util: Rbac
    Source: src/cver/api/utils/rbac.py

"""

from cver.api.utils import rbac

from .fixture.request import Request


class TestApiUtilsRbac:

    def test__check_role_uri_access(self):
        """Test Rbac's check against role access to a uri.
        :method: rbac.check_role_uri_access
        """
        role_perms_admin = ["write-all", "read-all"]
        request = Request()
        request.path = "/users"
        request.method = "GET"
        rbac_res_users = rbac.check_role_uri_access(role_perms_admin, request)
        assert rbac_res_users

        request.path = "/image-build-waitings"
        request.method = "GET"
        rbac_res_ibws = rbac.check_role_uri_access(role_perms_admin, request)
        assert rbac_res_ibws

# End File: cver/tests/api/utils/test_rbac.py
