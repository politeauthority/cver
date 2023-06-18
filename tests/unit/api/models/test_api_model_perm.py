"""
    Cver Test Unit
    Api Model: Perm

    Source: src/cver/api/model/perm.py

"""

from cver.api.models.perm import Perm


class TestApiModelPerm:

    def test____init__(self):
        """Test the model's initialization.
        :method: Perm().__init__
        """
        model = Perm()
        assert hasattr(model, "name")
        assert hasattr(model, "slug_name")

    def test____repr__(self):
        """Test the model's representation.
        :method: Perm().__repr__
        """
        model = Perm()
        assert str(model) == "<Perm>"


# End File: cver/tests/api/models/test_api_model_perm.py
