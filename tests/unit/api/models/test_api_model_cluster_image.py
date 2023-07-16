"""
    Cver Test Unit
    Api Model: Image
    Source: src/cver/api/model/cluster_image.py

"""

from cver.api.models.cluster_image import ClusterImage


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


# End File: cver/tests/api/models/test_api_model_cluster_image.py
