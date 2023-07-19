"""
    Cver Test Unit
    Api Model: Cluster
    Source: src/cver/api/model/cluster.py

"""

from cver.api.models.cluster import Cluster


class TestCluster:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: Cluster().__init__
        """
        model = Cluster()
        assert hasattr(model, "org_id")
        assert hasattr(model, "name")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Cluster()
        assert str(model) == "<Cluster>"


# End File: cver/tests/api/models/test_api_model_cluster.py
