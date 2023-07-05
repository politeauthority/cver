"""
    Cver Test Unit
    Api Model: Migration

    Source: src/cver/api/model/migration.py

"""

from cver.api.models.migration import Migration


class TestApiModelMigration:

    def test____init__(self):
        """Test the models initialization.
        :method: Migration().__init__
        """
        image = Migration()
        assert hasattr(image, "number")
        assert hasattr(image, "success")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Migration()
        assert str(model) == "<Migration>"


# End File: cver/tests/api/models/test_api_model_migration.py
