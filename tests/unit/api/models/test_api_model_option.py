"""
    Cver Test Unit
    Api Model: Option

    Source: src/cver/api/model/option.py

"""
from datetime import datetime

from cver.api.models.option import Option

from cver_test_tools.fixtures import db


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

    def test__get_by_name(self):
        """
        :method: Option().get_by_name()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            1, datetime.now(), datetime.now(), "bool", "test-option", 1, "write-all", "read-all", 0
        ]
        model = Option(db.Conn(), cursor)
        assert model.get_by_name("test-option")
        assert 1 == model.id

    def test__build_from_list(self):
        """
        :method: Option().build_from_list()
        """
        cursor = db.Cursor()
        raw = [
            1, datetime.now(), datetime.now(), "bool", "test-option", 1, "write-all", "read-all", 0
        ]
        model = Option(db.Conn(), cursor)
        assert model.build_from_list(raw)
        assert "test-option" == model.name
        assert model.value

    def test__sql_value_override_for_model(self):
        """
        :method: Option().sql_value_override_for_model()
        """
        option_value_field = {
            "name": "value",
            "type": "str",
            "api_writeable": True
        }
        model = Option()
        model.value = "just-one"
        assert "just-one" == model.sql_value_override_for_model(option_value_field)
        model.value = ["heres-one", "heres-two"]
        # assert "heres-one,heres-two" == model.sql_value_override_for_model(option_value_field)

    def test___set_bool(self):
        """
        :method: Option()._set_bool()
        """
        model = Option()
        model.value = "just-one"
        assert model._set_bool(True)
        assert model._set_bool(1)
        assert model._set_bool("1")
        assert not model._set_bool(False)
        assert not model._set_bool(0)
        assert not model._set_bool("0")

# End File: cver/tests/api/models/test_api_model_option.py
