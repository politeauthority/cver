"""
    Cver Test Unit
    Api Model: Option

    Source: src/cver/api/model/option.py

"""

from cver.api.models.option import Option


class TestApiModelOption:

    def test____init__(self):
        """Test the model's initialization.
        :method: Option().__init__
        """
        model = Option()
        assert hasattr(model, "type")
        assert hasattr(model, "name")
        assert hasattr(model, "value")

    def test____repr__(self):
        """Test the model's representation.
        :method: Option().__repr__
        """
        model = Option()
        assert str(model) == "<Option>"


# End File: cver/tests/api/models/test_api_model_option.py
