"""
    Cver Test Unit
    Api Model: Base

"""
from cver.api.models.base import Base


BASE_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
}


class TestBase:

    def test____init__(self):
        """Test the Base Model's initialization.
        :method: Base().__init__
        """
        base = Base()
        assert hasattr(base, "table_name")
        assert hasattr(base, "backend")
        assert hasattr(base, "field_map")

    def test____repr__(self):
        """Test the Base Model's representation.
        :method: Base().__repr__
        """
        base = Base()
        assert str(base) == "<Base>"

    def test____desc__(self):
        """
        :method: Base().__desc__
        """
        base = Base()
        base.field_map = BASE_MAP
        base.id = 7
        assert base.__desc__() is None

    def test__connect(self):
        """
        :method: Base().connect
        """
        base = Base()
        base.total_map = BASE_MAP
        assert base.connect("conn", "cursor")
        assert hasattr(base, "conn")
        assert base.conn == "conn"
        assert hasattr(base, "cursor")
        assert base.cursor == "cursor"

    def test__get_field(self):
        """
        :method: Base().get_field()
        """
        base = Base()
        base.field_map = BASE_MAP
        base.id = 1
        field = base.get_field("id")
        assert isinstance(field, dict)
        assert "name" in field
        assert "type" in field

    def test___sql_fields_sanitized(self):
        """
        :method: Base()._sql_fields_sanitized
        """
        base = Base()
        assert base._sql_fields_sanitized({}) == ""
        base.total_map = BASE_MAP
        assert base._sql_fields_sanitized({}) == "`id`, `created_ts`, `updated_ts`"

    def test___sql_insert_values_santized(self):
        """
        :method: Base()._sql_insert_values_santized
        """
        base = Base()
        base.total_map = BASE_MAP
        import ipdb; ipdb.set_trace()
        base.setup()
        assert base._sql_insert_values_santized() == "`id`"


# End File: cver/tests/unit/api/models/test_base.py
