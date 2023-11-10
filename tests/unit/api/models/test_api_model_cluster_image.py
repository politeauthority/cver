"""
    Cver Test Unit
    Api Model: Image
    Source: src/cver/api/model/cluster_image.py

"""
from datetime import datetime

from cver.api.models.cluster_image import ClusterImage

from cver_test_tools.fixtures import db


class TestApiModelClusterImage:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: ClusterImage().__init__
        """
        model = ClusterImage()
        assert hasattr(model, "cluster_id")
        assert hasattr(model, "image_id")

    def test____repr__(self):
        """Test the model's representation.
        :method: ClusterImage().__repr__
        """
        model = ClusterImage()
        assert str(model) == "<ClusterImage>"

    def test__get_by_cluster_and_image_id(self):
        """Test the model's representation.
        :method: ClusterImage().get_by_cluster_and_image_id()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), 10, 1, datetime.now(), datetime.now()]
        model = ClusterImage(db.Conn(), cursor)
        assert model.get_by_cluster_and_image_id(1, 10)
        assert 5 == model.id


# End File: cver/tests/api/models/test_api_model_cluster_image.py
