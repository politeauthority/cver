"""
    Cver Test Unit
    Api Model: Image
    Source: src/cver/api/model/image.py

"""
from datetime import datetime

from cver.api.models.image import Image

from cver_test_tools.fixtures import db


class TestImage:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: Image().__init__
        """
        image = Image()
        assert hasattr(image, "id")
        assert hasattr(image, "created_ts")
        assert hasattr(image, "updated_ts")
        assert hasattr(image, "name")
        assert hasattr(image, "registry_id")
        assert hasattr(image, "maintained")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Image()
        assert str(model) == "<Image>"

    def test__get_by_registry_id_and_name(self):
        """
        :method: Image().get_by_registry_id_and_name()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5,                              # id
            datetime.now(),                 # created_ts
            datetime.now(),                 # updated_ts
            "politeauthority/cver-api",     # name
            1,                              # registry_id
            1                               # maintained
        ]
        model = Image(db.Conn(), cursor)
        assert model.get_by_registry_id_and_name("docker.io", "politeauthority/cver-api")
        assert 5 == model.id

# End File: cver/tests/api/models/test_image.py
