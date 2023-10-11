"""
    Cver Test Unit
    Api Model: Base
    Tests File: cver/src/cver/api/models/base.py
    @todo: Many of these tests could stand to be expanded out to test more types and complex models.

"""
from datetime import datetime
from dateutil.tz import tzutc
import json

import arrow
from pytest import raises

from cver.api.models.base import Base

from cver_test_tools.fixtures import db


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

    def test__create_table(self):
        """
        :method: Base().create_table()
        """
        base = Base(db.Conn(), db.Cursor())
        base.field_map = BASE_MAP
        base.setup()
        with raises(AttributeError):
            assert base.create_table()
        base.table_name = "base_table"
        assert base.save()

    def test__create_table_sql(self):
        """
        :method: Base().create_table_sql()
        """
        base = Base()
        with raises(AttributeError):
            assert base.create_table_sql()
        base.table_name = "base_table"
        base.field_map = BASE_MAP
        base.setup()
        expected = "CREATE TABLE IF NOT EXISTS base_table \n(`id` INTEGER PRIMARY KEY "
        expected += "AUTO_INCREMENT,\n`created_ts` DATETIME,\n`updated_ts` DATETIME)"
        assert expected == base.create_table_sql()

    def test__setup(self):
        """
        :method: Base().get_field()
        """
        base = Base().setup()
        assert base

    def test__save(self):
        """
        :method: Base().save()
        """
        base = Base(db.Conn(), db.Cursor())
        base.table_name = "base_table"
        FIELD_MAP = BASE_MAP
        FIELD_MAP["new_field"] = {
            "name": "new_field",
            "type": "str"
        }
        base.field_map = FIELD_MAP
        base.setup()
        BASE_MAP.pop("new_field")
        assert base
        assert not base.id, None
        assert base.save()
        assert isinstance(base.id, int)

    def test__insert(self):
        """
        :method: Base().insert()
        """
        base = Base(db.Conn(), db.Cursor())
        base.table_name = "base_table"
        FIELD_MAP = BASE_MAP
        FIELD_MAP["new_field"] = {
            "name": "new_field",
            "type": "str"
        }
        base.field_map = FIELD_MAP
        base.setup()
        BASE_MAP.pop("new_field")
        assert base
        assert not base.id
        assert base.insert()
        assert isinstance(base.id, int)

    def test__iodku(self):
        """
        :method: Base().idoku()
        """
        base = Base(db.Conn(), db.Cursor())
        base.table_name = "base_table"
        base.field_map = BASE_MAP
        base.setup()
        base.id = 5
        assert base
        assert base.iodku()

    def test__delete(self):
        """
        :method: Base().delete()
        """
        base = Base(db.Conn(), db.Cursor())
        base.table_name = "base_table"
        base.field_map = BASE_MAP
        base.setup()
        base.id = 5
        assert base
        assert base.delete()

    def test__get_by_id(self):
        """
        :method: Base().get_by_id()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [5, datetime.now(), datetime.now()]
        base = Base(db.Conn(), cursor)
        base.table_name = "base_table"
        base.field_map = BASE_MAP
        base.setup()
        assert base.get_by_id(5)
        assert 5 == base.id
        assert isinstance(base.created_ts, datetime)
        assert isinstance(base.updated_ts, datetime)

    def test__get_by_name(self):
        """
        :method: Base().get_by_name()
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["name"] = {
            "name": "name",
            "type": "str"
        }
        cursor = db.Cursor()
        cursor.result_to_return = [5, datetime.now(), datetime.now(), "hello-world"]
        base = Base(db.Conn(), cursor)
        base.table_name = "base_table"
        base.field_map = FIELD_MAP
        base.setup()
        assert base.get_by_name("hello-world")
        assert "hello-world" == base.name
        BASE_MAP.pop("name")

    def test__get_by_unique_key(self):
        """
        :@note: WIP
        :method: Base().get_by_unique_key()
        """
        new_map = BASE_MAP
        EXTRAS = {
            "image_id": {
                "name": "image_id",
                "type": "int",
                "api_writeable": True,
                "api_searchable": True,
            },
            "image_build_id": {
                "name": "image_build_id",
                "type": "int",
                "api_writeable": True,
                "api_searchable": True,
            },
            "tag": {
                "name": "tag",
                "type": "str",
                "api_writeable": True,
                "api_searchable": True,
            }
        }
        new_map.update(EXTRAS)
        cursor = db.Cursor()
        cursor.result_to_return = [5, datetime.now(), datetime.now(), 5, 10, "hello"]
        base = Base(db.Conn(), cursor)
        base.table_name = "base"
        base.field_map = new_map
        field_meta = {
            "unique_key": ["image_id", "image_build_id", "tag"]
        }
        base.field_meta = field_meta
        base.setup()
        fields = {
            "image_id": 5,
            "image_build_id": 10,
            "tag": "latest"
        }

        assert base.get_by_unique_key(fields)
        assert 5 == base.image_id
        assert 10 == base.image_build_id
        assert "hello" == base.tag
        BASE_MAP.pop("image_id")
        BASE_MAP.pop("image_build_id")
        BASE_MAP.pop("tag")

    def test__get_by_field(self):
        """
        :method: Base().get_by_field()
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["name"] = {
            "name": "name",
            "type": "str"
        }
        cursor = db.Cursor()
        cursor.result_to_return = [5, datetime.now(), datetime.now(), "hello-world"]
        base = Base(db.Conn(), cursor)
        base.table_name = "base_table"
        base.field_map = FIELD_MAP
        base.setup()
        assert base.get_by_field("name", "hello-world")
        assert "hello-world" == base.name
        BASE_MAP.pop("name")

    def test__get_by_fields(self):
        """
        :method: Base().get_by_fields()
        """
        FIELD_MAP = BASE_MAP
        FIELD_MAP["image_id"] = {
            "name": "image_id",
            "type": "int"
        }
        FIELD_MAP["image_build_id"] = {
            "name": "image_build_id",
            "type": "int"
        }
        cursor = db.Cursor()
        cursor.result_to_return = [
            5,
            datetime.now(),
            datetime.now(),
            5,
            10]
        fields = [
            {
                "field": "image_id",
                "value": 5,
                "op": "eq"
            },
            {
                "field": "image_build_id",
                "value": 10,
                "op": "eq"
            }
        ]
        base = Base(db.Conn(), cursor)
        base.table_name = "base_table"
        base.field_map = FIELD_MAP
        base.setup()
        assert base.get_by_fields(fields)
        assert 5 == base.image_id
        assert 10 == base.image_build_id
        BASE_MAP.pop("image_id")
        BASE_MAP.pop("image_build_id")

    def test__get_last(self):
        """
        :method: Base().get_last()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [5, datetime.now(), datetime.now()]
        base = Base(db.Conn(), cursor)
        base.table_name = "base_table"
        base.field_map = BASE_MAP
        base.setup()
        assert base.get_last()
        assert 5 == base.id

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

    def test__build_from_list(self):
        """
        :method: Base().build_from_list()
        """
        test_record = [5, datetime.now(), datetime.now()]
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
        assert base.build_from_list(test_record)
        assert 5 == base.id
        assert isinstance(base.created_ts, datetime)
        assert isinstance(base.updated_ts, datetime)

        with raises(AttributeError):
            test_record_error = test_record
            test_record_error.append("hello-world")
            base.build_from_list(test_record_error)

    def test__build_from_dict(self):
        """
        :method: Base().build_from_dict()
        :@todo: This can be expanded to handle more types.
        """
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
        test_record = {
            "id": 5,
            "created_ts": datetime.now(),
            "updated_ts": datetime.now()
        }
        assert base.build_from_dict(test_record)
        assert 5 == base.id
        assert isinstance(base.created_ts, datetime)
        assert isinstance(base.updated_ts, datetime)

    def test__json(self):
        """
        :method: Base().json()
        :@todo: This can be expanded more to handle the api argument.
        """
        base = Base()
        base.field_map = BASE_MAP
        base.setup()
        base.id = 5
        base.created_ts = datetime.now()
        base.updated_ts = datetime.now()
        base_json = base.json()
        assert json.dumps(base_json)

    def test___gen_insert_sql(self):
        """Check that we create a correct SQL statement for an insert.
        :method: Base()._gen_insert_sql
        """
        base = Base(None, None)
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        result = base._gen_insert_sql()
        assert len(result) == 127
        expected = 'INSERT INTO `base` (`created_ts`, `updated_ts`) VALUES ('
        assert result[:56] == expected

    def test____gen_iodku_sql(self):
        """Check that we create a correct SQL statement for an insert.
        :method: Base()._gen_iodku_sql
        """
        base = Base(None, None)
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        base.id = 5
        result = base._gen_iodku_sql()
        assert 314 == len(result)

    def test____gen_delete_sql(self):
        """Check that we create a correct SQL statement for a delete.
        :method: Base()._gen_delete_sql
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        base.id = 5
        result = base._gen_delete_sql()
        expected = "DELETE FROM `base` WHERE `id` = 5;"
        assert expected == result

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

    def test___gen_get_by_name_sql(self):
        """
        :method: Base()._gen_get_by_name_sql
        """
        base = Base()
        base.table_name = "base"
        base.field_map = BASE_MAP
        base.setup()
        expected_res = '\n            SELECT *\n            FROM `base`\n            WHERE `name` '
        expected_res += '= "hello-world";'
        assert expected_res == base._gen_get_by_name_sql("hello-world")

    def test___gen_get_by_unique_key_sql(self):
        """
        :method: Base()._gen_get_by_unique_key_sql()
        """
        new_map = BASE_MAP
        EXTRAS = {
            "image_id": {
                "name": "image_id",
                "type": "int",
                "api_writeable": True,
                "api_searchable": True,
            },
            "image_build_id": {
                "name": "image_build_id",
                "type": "int",
                "api_writeable": True,
                "api_searchable": True,
            },
            "tag": {
                "name": "tag",
                "type": "str",
                "api_writeable": True,
                "api_searchable": True,
            }
        }
        new_map.update(EXTRAS)
        base = Base()
        base.table_name = "base"
        base.field_map = new_map
        base.field_meta = {
            "unique_key": ["image_id", "image_build_id"]
        }
        fields = {
            "image_id": 5,
            "image_build_id": 10,
            "tag": "latest"
        }

        with raises(AttributeError):
            base._gen_get_by_unique_key_sql(fields)
        base.field_meta = {
            "unique_key": ["image_id", "image_build_id", "tag"]
        }
        expected = """
            SELECT *
            FROM base
            WHERE
                `image_id` = 5 AND `image_build_id` = 10 AND `tag` = "latest"
            LIMIT 1;
        """

        result = base._gen_get_by_unique_key_sql(fields)
        assert expected == result
        BASE_MAP.pop("image_id")
        BASE_MAP.pop("image_build_id")
        BASE_MAP.pop("tag")

    def test___gen_get_by_fields_sql(self):
        """
        :method: Base()._gen_get_by_fields_sql
        """
        SCAN_MAP = {
            "image_id": {
                "name": "image_id",
                "type": "int",
                "api_searchable": True
            },
            "image_build_id": {
                "name": "image_build_id",
                "type": "int",
                "api_searchable": True
            }
        }
        new_map = BASE_MAP
        new_map.update(SCAN_MAP)
        fields = [
            {
                "field": "image_id",
                "value": 1,
                "op": "eq"
            },
            {
                "field": "image_build_id",
                "value": 1,
                "op": "eq"
            }
        ]
        base = Base()
        base.table_name = "base"
        base.field_map = new_map
        base.setup()
        result = base._gen_get_by_fields_sql(fields)
        expected = "`image_id` = 1 AND `image_build_id` = 1"
        assert expected == result
        BASE_MAP.pop("image_id")
        BASE_MAP.pop("image_build_id")

    def test___gen_get_last_sql(self):
        """
        :method: Base()._gen_get_last_sql
        """
        base = Base()
        base.table_name = "base"
        result = base._gen_get_last_sql()
        expected = "\n            SELECT *\n            FROM base\n            ORDER BY "
        expected += "created_ts DESC\n            LIMIT 1"
        assert expected == result

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
            "value": None,
            "op": "eq"
        }
        assert "NULL" == base._sql_field_value(field_map_info, field_data)
        field_data = {
            "field": "image_build_id",
            "value": 1,
            "op": "eq"
        }
        assert 1 == base._sql_field_value(field_map_info, field_data)

        field_map_info = {
            "name": "name",
            "type": "str",
        }
        field_data = {
            "field": "name",
            "value": "hello",
            "op": "eq"
        }
        assert '"hello"' == base._sql_field_value(field_map_info, field_data)

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
        assert expected_res == base._sql_insert_values_santized({})

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

    def test__check_required_class_vars(self):
        """
        :method: Base().check_required_class_vars
        """
        base = Base()
        with raises(AttributeError):
            base.check_required_class_vars()

        base = Base(db.Conn(), db.Cursor())
        assert base.check_required_class_vars()

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

    def test___set_types(self):
        """
        :method: Base()._set_types()
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
        base._set_types()
        assert set_detaults
        assert base.new

    def test___xlate_field_type(self):
        """
        :method: Base()._xlate_field_type
        """
        base = Base()
        "INTEGER" == base._xlate_field_type("int")
        "DATETIME" == base._xlate_field_type("datetime")
        "DATETIME" == base._xlate_field_type("datetime")
        "VARCHAR(200)" == base._xlate_field_type("str")
        "TEXT" == base._xlate_field_type("text")
        "TINYINT(1)" == base._xlate_field_type("bool")
        "DECIMAL(10, 5)" == base._xlate_field_type("float")
        "TEXT" == base._xlate_field_type("list")
        "JSON" == base._xlate_field_type("json")

    def test___is_model_json(self):
        """
        :method: Base()._is_model_json
        """
        base = Base()
        assert not base._is_model_json()
        base.field_map = {
            "json_field": {
                "name": json,
                "type": "json"
            }
        }
        assert base._is_model_json()

    def test____get_datetime(self):
        """
        :method: Base()._get_date_time
        """
        base = Base()
        longtime = "2023-10-11 14:21:14 +00:00"
        assert isinstance(base._get_datetime(longtime), datetime)
        short_time = "2023-10-11 14:21:14"
        assert isinstance(base._get_datetime(short_time), datetime)
        assert not base._get_datetime("nothing")


# End File: cver/tests/unit/api/models/test_base.py
