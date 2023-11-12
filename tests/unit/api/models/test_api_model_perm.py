"""
    Cver Test Unit
    Api Model: Perm

    Source: src/cver/api/model/perm.py

"""
from datetime import datetime

from cver.api.models.perm import Perm

from cver_test_tools.fixtures import db


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

    def test__get_by_slug(self):
        """
        :method: Perm().get_by_slug()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), "Write all", "write-all"]
        model = Perm(db.Conn(), cursor)
        assert model.get_by_slug("write-all")
        assert 5 == model.id
        assert "write-all" == model.slug_name

# End File: cver/tests/api/models/test_api_model_perm.py
