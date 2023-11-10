"""
    Cver Test Unit
    Api Model: RolePerm

    Source: src/cver/api/model/role_perm.py

"""
from datetime import datetime

from cver.api.models.role_perm import RolePerm

from cver_test_tools.fixtures import db


class TestApiModelRolePerm:

    def test____init__(self):
        """Test the model's initialization.
        :method: RolePerm().__init__
        """
        model = RolePerm()
        assert hasattr(model, "role_id")
        assert hasattr(model, "perm_id")
        assert hasattr(model, "enabled")

    def test____repr__(self):
        """Test the model's representation.
        :method: RolePerm().__repr__
        """
        model = RolePerm()
        assert str(model) == "<RolePerm>"

    def test__get_by_role_perm(self):
        """
        :method: Perm().get_by_role_perm()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), 8, 11, 1]
        model = RolePerm(db.Conn(), cursor)
        assert model.get_by_role_perm(role_id=8, perm_id=11)
        assert 5 == model.id
        assert 8 == model.role_id
        assert 11 == model.perm_id

# End File: cver/tests/api/models/test_api_model_role_perm.py
