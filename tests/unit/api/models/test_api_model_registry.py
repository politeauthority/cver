"""
    Cver Test Unit
    Api Model: Registry
    Source: src/cver/api/model/registry.py

"""
from cver.api.models.registry import Registry


class TestRegistry:

    def test____init__(self):
        """Test the Registry Model's initialization.
        :method: Registry().__init__
        """
        model = Registry()
        assert hasattr(model, "id")
        assert hasattr(model, "created_ts")
        assert hasattr(model, "updated_ts")
        assert hasattr(model, "name")
        assert hasattr(model, "url")
        assert hasattr(model, "url_pull_thru")
        assert hasattr(model, "maintained")
        assert hasattr(model, "daily_limit")
        assert hasattr(model, "public")

    def test____repr__(self):
        """Test the model's representation.
        :method: Registry().__repr__
        """
        model = Registry()
        assert str(model) == "<Registry>"


# End File: cver/tests/api/models/test_api_model_registry.py
