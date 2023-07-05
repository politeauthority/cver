"""
    Cver Test Unit
    Api Model: Base
    Tests File: cver/api/models/base.py

"""
from datetime import datetime
from dateutil.tz import tzutc

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
    }
}


class TestApiModelBase:

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
        """Tests that a model builds out it's field description
        :method: Base().__desc__
        """
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
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

    def test__setup(self):
        """
        :method: Base().get_field()
        """
        base = Base().setup()
        assert base

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

    def test___gen_get_by_id_sql(self):
        """
        :method: Base()._gen_get_by_id_sql
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        base.id = 1
        expected_res = '\n            SELECT *\n            FROM `base`\n            '
        expected_res += 'WHERE `id` = 1;'
        assert base._gen_get_by_id_sql() == expected_res

    def test___sql_fields_sanitized(self):
        """
        :method: Base()._sql_fields_sanitized
        """
        base = Base()
        assert base._sql_fields_sanitized({}) == ""
        base.field_map = BASE_MAP
        base.setup()
        assert base._sql_fields_sanitized({}) == "`id`, `created_ts`, `updated_ts`"

    def test___sql_insert_values_santized(self):
        """
        :method: Base()._sql_insert_values_santized
        """
        base = Base()
        assert base._sql_insert_values_santized({}) == ""
        base.field_map = BASE_MAP
        base.setup()
        base.id = 1
        base.created_ts = datetime(2023, 6, 3, 20, 19, 22, tzinfo=tzutc())
        base.updated_ts = datetime(2023, 6, 3, 20, 19, 22, tzinfo=tzutc())
        expected_res = '1, "2023-06-03 20:19:22+00:00", "2023-06-03 20:19:22+00:00"'
        assert base._sql_insert_values_santized({}) == expected_res

    def test___sql_update_fields_values_santized(self):
        """
        :method: Base()._sql_update_fields_values_santized
        """
        base = Base()
        assert base._sql_update_fields_values_santized({}) == ""
        base.field_map = BASE_MAP
        base.setup()
        base.id = 1
        base.created_ts = datetime(2023, 6, 3, 20, 19, 22, tzinfo=tzutc())
        base.updated_ts = datetime(2023, 6, 3, 20, 19, 22, tzinfo=tzutc())
        expected_res = '`id`=1, `created_ts`="2023-06-03 20:19:22+00:00", '
        expected_res += '`updated_ts`="2023-06-03 20:19:22+00:00"'
        assert base._sql_update_fields_values_santized({}) == expected_res

    def test___set_defaults(self):
        """Checks that default field types are applied to the model.
        @todo: Currently only tests bools, need to test more types.
        :method: Base()._set_defaults
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["new"] = {
            "name": "new",
            "type": "bool",
            "default": True
        }
        base = Base()
        base.field_map = FIELD_MAP
        set_detaults = base._set_defaults()
        assert set_detaults
        assert base.new


# End File: cver/tests/unit/api/models/test_base.py
