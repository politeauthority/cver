"""
    Cver Test Unit
    Api Model: Organization

    Source: src/cver/api/model/organization.py

"""
from datetime import datetime

from cver.api.models.organization import Organization

from cver_test_tools.fixtures import db


class TestApiModelMigration:

    def test____init__(self):
        """Test the models initialization.
        :method: Organization().__init__
        """
        model = Organization()
        assert hasattr(model, "name")
        assert hasattr(model, "email")
        assert hasattr(model, "last_access")

    def test____repr__(self):
        """Test the model's representation.
        :method: Organization().__repr__
        """
        model = Organization()
        assert str(model) == "<Org>"

    def test__get_by_email(self):
        """
        :method: Organization().get_by_email()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), "test-org", "test-org@example.com", datetime.now()]
        model = Organization(db.Conn(), cursor)
        assert model.get_by_email("test-org@example.com")
        assert 5 == model.id
        assert "test-org@example.com" == model.email

# End File: cver/tests/api/models/test_api_model_organization.py
