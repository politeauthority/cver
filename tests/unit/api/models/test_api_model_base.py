"""
    Cver Test Unit
    Api Model: Base
    Tests File: cver/src/cver/api/models/base.py

"""
import arrow

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

    def test___gen_insert_sql(self):
        """Check that we create a correct SQL statement for an insert.
        :method: Base()._gen_insert_sql
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        result = base._gen_insert_sql()
        assert len(result) == 127
        expected = 'INSERT INTO `base` (`created_ts`, `updated_ts`) VALUES ('
        assert result[:56] == expected

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

    def test___sql_field_value(self):
        """
        :method: Base()._sql_field_value
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        field_map_info = {
            "name": "image_id",
            "type": "int"
        }
        field_data = {
            "field": "image_build_id",
            "value": 1,
            "op": "eq"
        }
        assert base._sql_field_value(field_map_info, field_data) == 1
        field_map_info = {
            "name": "name",
            "type": "str",
        }
        field_data = {
            "field": "name",
            "value": "hello",
            "op": "eq"
        }
        assert base._sql_field_value(field_map_info, field_data) == '"hello"'

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

    def test___get_sql_value_santized_typed(self):
        """
        :method: Base()._get_sql_value_santized_typed
        """
        base = Base()
        base.field_map = BASE_MAP
        field = BASE_MAP["id"]
        assert base._get_sql_value_santized_typed(field, 6) == 6
        assert base._get_sql_value_santized_typed(field, "6") == 6
        field = BASE_MAP["created_ts"]
        now = arrow.now()
        assert isinstance(base._get_sql_value_santized_typed(field, now.datetime), str)

        bool_field = {
            "name": "bool_field",
            "type": "bool",
        }
        assert base._get_sql_value_santized_typed(bool_field, True) == 1
        assert base._get_sql_value_santized_typed(bool_field, "true") == 1
        assert base._get_sql_value_santized_typed(bool_field, "True") == 1
        assert base._get_sql_value_santized_typed(bool_field, False) == 0
        assert base._get_sql_value_santized_typed(bool_field, "False") == 0

    # def test___gen_sql_get_by_fields(self):
    #     """
    #     :method: Base()._gen_sql_get_by_fields
    #     """
    #     SCAN_MAP = {
    #         "image_id": {
    #             "name": "image_id",
    #             "type": "int",
    #             "api_searchable": True
    #         },
    #         "image_build_id": {
    #             "name": "image_build_id",
    #             "type": "int",
    #             "api_searchable": True
    #         }
    #     }
    #     new_map = BASE_MAP
    #     new_map.update(SCAN_MAP)
    #     fields = [
    #         {
    #             "field": "image_id",
    #             "value": 1,
    #             "op": "eq"
    #         },
    #         {
    #             "field": "image_build_id",
    #             "value": 1,
    #             "op": "eq"
    #         }
    #     ]
    #     base = Base()
    #     base.table_name = "base"
    #     base.field_map = new_map
    #     base.setup()
    #     result = base._gen_sql_get_by_fields(fields)
    #     assert result == "`image_id` = 1 AND `image_build_id` = 1"

# End File: cver/tests/unit/api/models/test_base.py
