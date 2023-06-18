"""
    Cver Test Unit
    Api Model: Role

    Source: src/cver/api/model/role.py

"""

from cver.api.models.role import Role


class TestApiModelRole:

    def test____init__(self):
        """Test the model's initialization.
        :method: Role().__init__
        """
        model = Role()
        assert hasattr(model, "name")
        assert hasattr(model, "slug_name")

    def test____repr__(self):
        """Test the model's representation.
        :method: Role().__repr__
        """
        model = Role()
        assert str(model) == "<Role>"


# End File: cver/tests/api/models/test_api_model_role.py
