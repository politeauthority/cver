"""
    Cver Client Unit Test
    Client Model: Cluster
    Source: cver/src/cver/cver_client/model/cluser.py

"""

from cver.client.models.cluster import Cluster


class TestClientModelCluster:

    def test____init__(self):
        """Test the Model's initialization.
        :method: Cluster().__init__
        """
        model = Cluster()
        assert model
        assert hasattr(model, "org_id")
        assert hasattr(model, "name")
        assert hasattr(model, "maintained")

    def test____repr__(self):
        """Test the model's representation.
        :method: ApiKey().__repr__
        """
        model = Cluster()
        assert str(model) == "<Cluster>"

        model.id = 1
        assert str(model) == "<Cluster: 1>"


# End File: cver/tests/cver_client/models/test_client_model_cluster.py
