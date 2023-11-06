"""
    Cver Client Unit Test
    Client Model: App
    Source: cver/src/cver/cver_client/model/app.py

"""

from cver.client.models.app import App


class TestClientModelApp:

    def test____init__(self):
        """Test the Model's initialization.
        :method: App().__init__
        """
        model = App()
        assert model
        assert hasattr(model, "name")
        assert hasattr(model, "slug_name")
        assert hasattr(model, "software_id")
        assert hasattr(model, "url_git")
        assert hasattr(model, "url_marketing")

    def test____repr__(self):
        """Test the model's representation.
        :method: ApiKey().__repr__
        """
        model = App()
        assert str(model) == "<App>"

        model.id = 1
        assert str(model) == "<App: 1>"


# End File: cver/tests/cver_client/models/test_client_model_app.py
