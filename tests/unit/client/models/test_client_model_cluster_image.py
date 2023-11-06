"""
    Cver Client Unit Test
    Client Model: ClusterImage
    Source: cver/src/cver/cver_client/model/cluster_image.py

"""

from cver.client.models.cluster_image import ClusterImage


class TestClientModelClusterImage:

    def test____init__(self):
        """Test the Model's initialization.
        :method: ClusterImage().__init__
        """
        model = ClusterImage()
        assert model
        assert hasattr(model, "image_id")
        assert hasattr(model, "cluster_id")
        assert hasattr(model, "first_seen")
        assert hasattr(model, "last_seen")

    def test____repr__(self):
        """Test the model's representation.
        :method: ApiKey().__repr__
        """
        model = ClusterImage()
        assert str(model) == "<ClusterImage>"

        model.id = 1
        assert str(model) == "<ClusterImage: 1>"


# End File: cver/tests/cver_client/models/test_client_model_cluster_image.py
