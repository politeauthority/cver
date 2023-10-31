"""
    Cver Client Unit Test
    Client Model: Base
    Source: cver/src/cver/cver_client/model/base.py

"""

from cver.cver_client.models.base import Base


class TestClientModelBase:

    def test____init__(self):
        """Test the Base Model's initialization.
        :method: Base().__init__
        """
        base = Base()
        assert hasattr(base, "api_url")
        assert hasattr(base, "client_id")

    # def test____repr__(self):
    #     """Test the model's representation.
    #     :method: ImageBuild().__repr__
    #     """
    #     model = ImageBuild()
    #     assert str(model) == "<ImageBuild>"


# End File: cver/tests/cver_client/models/test_base.py
