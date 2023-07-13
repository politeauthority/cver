"""
    Cver Test Unit
    Api Model: RolePerm

    Source: src/cver/api/model/role_perm.py

"""

from cver.api.models.role_perm import RolePerm


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
        :method: Option().__repr__
        """
        model = RolePerm()
        assert str(model) == "<RolePerm>"


# End File: cver/tests/api/models/test_api_model_role_perm.py
