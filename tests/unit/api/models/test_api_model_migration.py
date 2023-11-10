"""
    Cver Test Unit
    Api Model: Migration

    Source: src/cver/api/model/migration.py

"""
from datetime import datetime

from cver.api.models.migration import Migration

from cver_test_tools.fixtures import db


class TestApiModelMigration:

    def test____init__(self):
        """Test the models initialization.
        :method: Migration().__init__
        """
        model = Migration()
        assert hasattr(model, "number")
        assert hasattr(model, "success")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Migration()
        assert str(model) == "<Migration>"

    def test__get_last_successful(self):
        """
        :method: Migration().get_last_successful()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), 1, 1]
        model = Migration(db.Conn(), cursor)
        assert model.get_last_successful()
        assert 5 == model.id

# End File: cver/tests/api/models/test_api_model_migration.py
