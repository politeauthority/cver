"""
    Cver Test Unit
    Api Util: Rbac
    Source: src/cver/api/utils/rbac.py

"""

from cver.api.utils import glow


class TestApiUtilsGlow:

    def test__db(self):
        """Test that glow vars exist.
        :data: glow.db
        """
        assert isinstance(glow.db, dict)
        assert "conn" in glow.db
        assert "cursor" in glow.db
        assert "HOST" in glow.db
        assert "PORT" in glow.db
        assert "USER" in glow.db
        assert "PASS" in glow.db
        assert "NAME" in glow.db

    def test__general(self):
        """Test that glow vars exist.
        :data: glow.general
        """
        assert isinstance(glow.general, dict)
        assert "LOG_LEVEL" in glow.general
        assert "VERSION" in glow.general
        assert "CVER_BUILD" in glow.general
        assert "CVER_BUILD_SHORT" in glow.general
        assert "CVER_ENV" in glow.general
        assert "CVER_JWT_EXPIRE_MINUTES" in glow.general
        assert "CVER_SECRET_KEY" in glow.general
        assert "CVER_TEST" in glow.general
        assert "CVER_LOG_HEALTH_CHECKS" in glow.general
        assert "CVER_DEPLOYED_AT" in glow.general

    def test__user(self):
        """Test that glow vars exist.
        :data: glow.user
        """
        assert isinstance(glow.user, dict)
        assert "user_id" in glow.user
        assert "org_id" in glow.user
        assert "role_id" in glow.user
        assert "role_perms" in glow.user

    def test__session(self):
        """Test that glow vars exist.
        :data: glow.session
        """
        assert isinstance(glow.session, dict)
        assert "uuid" in glow.session
        assert "short-id" in glow.session

    def test__start_session(self):
        """Test that glow vars exist.
        :data: glow.session
        """
        assert glow.start_session()
        assert glow.session
        assert 36 == len(glow.session["uuid"])
        assert 8 == len(glow.session["short_id"])

# End File: cver/tests/api/utils/test_glow.py
