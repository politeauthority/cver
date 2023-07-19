"""Base Model v. 0.2.0
Parent class for all models to inherit, providing methods for creating tables, inserting, updating,
selecting and deleting data.

The Base Model SQL driver can work with both SQLite3 and MySQL database.
    self.backend = "sqlite" for SQLite3
    self.backend = "mysql" for MySQL

Testing:
    Unit test file  cver/tests/unit/api/models/test_base.py
    Unit tested     11/37

"""
from datetime import datetime
import json
import logging

import arrow
from pymysql.err import ProgrammingError

from cver.shared.utils import xlate
from cver.api.utils import date_utils
from cver.api.utils import glow


class Base:

    def __init__(self, conn=None, cursor=None):
        """Base model constructor
        :unit-test: TestBase::test____init__
        """
        self._establish_db(conn, cursor)
        self.backed_iodku = True
        self.backend = "mysql"

        self.table_name = None
        self.entity_name = None
        self.field_map = {}
        self.immutable = False
        self.id = None
        self.setup()

    def __repr__(self):
        """Base model representation
        :unit-test: TestBase::test____repr__
        """
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def __desc__(self) -> None:
        """Describes the fields and values of class.
        :unit-test: TestBase::test____repr__
        """
        for field_id, field in self.field_map.items():
            print("%s: %s" % (field["name"], getattr(self, field["name"])))

    def connect(self, conn, cursor) -> bool:
        """Quick bootstrap method to connect the model to the database connection.
        :unit-test: TestBase::test__connect
        """
        self.conn = conn
        self.cursor = cursor
        return True

    def create_table(self) -> bool:
        """Create a table based on the self.table_name, and self.field_map."""
        if not self.table_name:
            raise AttributeError('Model table name not set, (self.table_name)')
        sql = self.create_table_sql()
        logging.info('Creating table: %s' % self.table_name)
        self.cursor.execute(sql)
        return True

    def create_table_sql(self) -> bool:
        """Create a table based SQL on the self.table_name, and self.field_map."""
        if not self.table_name:
            raise AttributeError('Model table name not set, (self.table_name)')
        sql = "CREATE TABLE IF NOT EXISTS %s \n(%s)" % (
            self.table_name,
            self._generate_create_table_feilds())
        return sql

    def setup(self) -> bool:
        """Set up model class vars, sets class var defaults, and corrects types where possible.
        :unit-test: TestBase::test__setup
        """
        self._set_defaults()
        self._set_types()
        return True

    def save(self) -> bool:
        """Saves a model instance in the model table."""
        self.setup()
        self.check_required_class_vars()
        if self.backed_iodku and not self.id:
            return self.iodku()
        if not self.id:
            logging.error("Save failed, missing %s.id or where list" % __class__.__name_)
            raise AttributeError("Save failed, missing %s.id or where list" % __class__.__name_)
        update_sql = self._gen_update_sql(["id", "created_ts"])
        self.cursor.execute(update_sql)
        self.conn.commit()
        return True

    def delete(self) -> bool:
        """Delete a model item."""
        sql = """DELETE FROM `%s` WHERE `id` = %s """ % (self.table_name, self.id)
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def get_field(self, field_name: str):
        """Get the details on a model field from the field map.
        :unit-test: test__get_field
        """
        for field_name, field in self.field_map.items():
            if field["name"] == field_name:
                return field
        return None

    def get_by_id(self, model_id: int = None) -> bool:
        """Get a single model object from db based on an object ID."""
        if model_id:
            self.id = model_id

        if not self.id:
            raise AttributeError('%s is missing an ID attribute.' % __class__.__name__)

        sql = self._gen_get_by_id_sql()
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False

        self.build_from_list(raw)

        return True

    def get_by_name(self, name: str) -> bool:
        """Get a model by name, if the model has a name field."""
        found_name_field = False
        for field_name, field in self.field_map.items():
            if field["name"] == "name":
                found_name_field = True
                break

        if not found_name_field:
            logging.warning("Entity does not have a get by name method.")
            return False

        sql = """
            SELECT *
            FROM `%s`
            WHERE `name` = "%s"; """ % (self.table_name, xlate.sql_safe(name))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_field(self, field: str, value: str) -> bool:
        """Get a model by specific, if the model has a name field."""
        found_field = False
        for field_name, field_info in self.field_map.items():
            if field_name == field:
                found_field = True
                break

        if not found_field:
            logging.warning("Entity does not have a %s field." % field)
            return False

        sql = """
            SELECT *
            FROM `%s`
            WHERE `%s` = "%s"; """ % (
            self.table_name,
            xlate.sql_safe(field),
            xlate.sql_safe(value))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_fields(self, fields: list) -> bool:
        """Get a model by a field, or fields.
        :todo: Eventually this needs to support more operators than just eq
        :param fields: list of dict
            fields
            [
                {
                    "field": "name",
                    "value": "A Cool Name",
                    "op": "eq"
                }
            ]
        :unit-test: None
        """
        sql_fields = ""
        for field in fields:
            sql_fields += '`%s`="%s",' % (
                xlate.sql_safe(field["field"]),
                xlate.sql_safe(field["value"]))
        sql_fields = sql_fields[:-1]
        sql = """
            SELECT *
            FROM %s
            WHERE %s
            LIMIT 1;""" % (self.table_name, sql_fields)
        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

    def get_last(self) -> bool:
        """Get the last created model."""
        sql = """
            SELECT *
            FROM %s
            ORDER BY created_ts DESC
            LIMIT 1""" % (self.table_name)

        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

    def build_from_list(self, raw: list) -> bool:
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        :param raw: The raw data from the database to be converted to model data.
        """
        if len(self.field_map) != len(raw):
            msg = "BUILD FROM LIST Model: %s field_map: %s, record: %s \n" % (
                self,
                len(self.field_map),
                len(raw))
            msg += "Field Map: %s \n" % str(self.field_map)
            msg += "Raw Record: %s \n" % str(raw)
            logging.error(msg)
            raise AttributeError(msg)

        count = 0
        for field_name, field in self.field_map.items():
            field_name = field['name']
            field_value = raw[count]

            # Handle the bool field type.
            if field['type'] == 'bool':
                if field_value == 1:
                    setattr(self, field_name, True)
                elif field_value == 0:
                    setattr(self, field_name, False)
                else:
                    setattr(self, field_name, None)

            # Handle the datetime field type.
            elif field['type'] == 'datetime':
                if field_value:
                    setattr(self, field_name, arrow.get(field_value).datetime)
                else:
                    setattr(self, field_name, None)

            # Handle the list field type.
            elif field['type'] == 'list':
                if field_value:
                    if "," in field_value:
                        val = field_value.split(',')
                    else:
                        val = [field_value]
                    setattr(self, field_name, val)
                else:
                    setattr(self, field_name, None)

            # Handle all other field types without any translation.
            else:
                setattr(self, field_name, field_value)

            count += 1

        return True

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        """
        for field, value in raw.items():
            if not hasattr(self, field):
                continue
            for field_map_field in self.field_map:
                if field_map_field["name"] == field:
                    field_map = field_map_field
                    break

            if field_map["type"] == "datetime":
                if isinstance(value, str):
                    value = date_utils.date_from_json(value)
            setattr(self, field, value)

        return True

    def json(self, get_api: bool = False) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. If get_api
        is specified and a model doesnt have api_display=False, it will export in the output.
        """
        json_out = {}
        for field_name, field in self.field_map.items():
            if get_api and "api_display" in field and not field["api_display"]:
                continue
            value = getattr(self, field["name"])
            if field["type"] == "datetime":
                value = date_utils.json_date(value)
            json_out[field["name"]] = value
        return json_out

    def describe(self) -> bool:
        """Debug tool for describing an model instance, printing all its fields to the console."""
        for field in self.field_map:
            print("%s\t\t\t%s" % (field["name"], getattr(self, field["name"])))
        return True

    def insert(self):
        """Insert a new record of the model."""
        sql = self._gen_insert_sql()
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except ProgrammingError as e:
            logging.critical(sql)
            logging.critical("Caught ProgrammingError exception:", e)
            exit(1)
        self.id = self.cursor.lastrowid
        return True

    def iodku(self) -> bool:
        """Runs an insert on duplicate key update query against the database, setting the id of
        the item as it's class var id.
        """
        sql = self._gen_iodku_sql()
        self.cursor.execute(sql)
        self.conn.commit()
        self.id = self.cursor.lastrowid
        return True

    def _gen_insert_sql(self, skip_fields: list = ["id"]) -> tuple:
        """Generate the insert SQL statement."""
        insert_sql = "INSERT INTO `%s` (%s) VALUES (%s)" % (
            self.table_name,
            self._sql_fields_sanitized(skip_fields=skip_fields),
            self._sql_insert_values_santized(skip_fields=skip_fields)
        )
        return insert_sql

    def _gen_iodku_sql(self, skip_fields: dict = {"id": {"name": "id"}}) -> str:
        """Generate the model values to send to the sql engine interpreter as a tuple."""
        if self.backend == "sqlite":
            # @note: this is missing.
            return None
        elif self.backend == "mysql":
            sql_args = {
                "table_name": self.table_name,
                "fields": self._sql_fields_sanitized(skip_fields),
                "values": self._sql_insert_values_santized(skip_fields),
                "fields_values": self._sql_update_fields_values_santized(skip_fields)
            }
            iodku_sql = """
                INSERT INTO `%(table_name)s`
                (%(fields)s)
                VALUES (%(values)s)
                ON DUPLICATE KEY UPDATE %(fields_values)s;""" % sql_args
            # logging.info("IODKU")
            # logging.info(iodku_sql)
        return iodku_sql

    def _gen_update_sql(self, skip_fields: list) -> tuple:
        """Generate the update SQL statement."""
        sql_args = {
            "table_name": self.table_name,
            "fields_values": self._sql_update_fields_values_santized(skip_fields),
            "where": "`id` = %s" % self.id
        }
        update_sql = """
            UPDATE `%(table_name)s`
            SET
            %(fields_values)s
            WHERE
            %(where)s;""" % sql_args
        return update_sql

    def _gen_get_by_id_sql(self) -> str:
        """Generates the get by_id sql.
        :unit-test: test___gen_get_by_id_sql
        """
        sql = """
            SELECT *
            FROM `%(table)s`
            WHERE `id` = %(model_id)s;""" % {
            "table": self.table_name,
            "model_id": xlate.sql_safe(self.id)
        }
        return sql

    def _sql_fields_sanitized(self, skip_fields: dict) -> str:
        """Get all class table column fields in a comma separated list for sql cmds. Returns a value
            like: `id`, `created_ts`, `update_ts`, `name`, `vendor`.
        :unit-test: test___sql_fields_sanitized
        """
        field_sql = ""
        for field_name, field in self.field_map.items():
            # Skip fields we don't want included in db writes
            if field['name'] in skip_fields:
                continue
            field_sql += "`%s`, " % field['name']
        return field_sql[:-2]

    def _sql_insert_values_santized(self, skip_fields: dict = None) -> str:
        """Creates the values portion of a query with the actual values sanitized.
        example: "2021-12-12", "a string", 1.
        :unit-test: test___sql_insert_values_santized
        """
        if not skip_fields:
            skip_fields = {}
        sql_values = ""
        for field_name, field in self.field_map.items():
            if field["name"] in skip_fields:
                continue
            value = self._get_sql_value_santized(field)
            sql_values += "%s, " % value
        return sql_values[:-2]

    def _sql_update_fields_values_santized(self, skip_fields: dict = None) -> str:
        """Generate the models SET sql statements, ie: SET key = value, other_key = other_value.
        :unit-test: test___sql_update_fields_values_santized
        """
        set_sql = ""
        for field_name, field in self.field_map.items():
            if field['name'] in skip_fields:
                continue

            value = self._get_sql_value_santized(field)
            set_sql += "`%s`=%s, " % (xlate.sql_safe(field["name"]), value)
        if not set_sql:
            return ""
        return set_sql[:-2]

    def _get_sql_value_santized(self, field: dict) -> str:
        """Get the sanitized value of a given field.
        """
        value = self.sql_value_override_for_model(field)

        if field["name"] == "created_ts" and not value:
            value = date_utils.now()

        if field["name"] == "updated_ts" and not value:
            value = date_utils.now()

        if value is None or value == []:
            value = "NULL"
            return value

        value = self._get_sql_value_santized_typed(field, value)

        return value

    def _get_sql_value_santized_typed(self, field, value) -> str:
        """Convert values to a safe santized value based on it's type."""
        # Handle converting int value
        if field["type"] == "int":
            value = xlate.sql_safe(value)

        # Handle converting a list value
        elif field["type"] == "list":
            if not isinstance(value, list) and value.isdigit():
                value = str(value)
            value = '"%s"' % xlate.sql_safe(xlate.convert_list_to_str(value))

        # Handle converting a bool
        elif field["type"] == "bool":
            value = xlate.sql_safe(xlate.convert_bool_to_int(value))

        # Handle converting a json value
        elif field["type"] == "json":
            logging.info("Creating JSON sql")
            value = json.dumps(value)
            value = f"'{value}'"

        # Handle converting anything else
        else:
            value = '"%s"' % xlate.sql_safe(value)

        return value

    def sql_value_override_for_model(self, field: dict) -> str:
        """Override the SQL value for a field before it's stored into the database."""
        return getattr(self, field["name"])

    def check_required_class_vars(self, extra_class_vars: list = []) -> bool:
        """Quick class var checks to make sure the required class vars are set before proceeding
           with an operation.

        """
        if not self.conn:
            raise AttributeError('Missing self.conn')

        if not self.cursor:
            raise AttributeError('Missing self.cursor')

        for class_var in extra_class_vars:
            if not getattr(self, class_var):
                raise AttributeError('Missing self.%s' % class_var)

        return True

    def _set_defaults(self) -> bool:
        """Set the defaults for the class field vars and populates the self.field_list var
        containing all table field names.
        :unit-test: test___set_defaults
        """
        self.field_list = []
        for field_name, field in self.field_map.items():
            field_name = field['name']
            self.field_list.append(field_name)

            default = None
            if 'default' in field:
                default = field['default']

            if field["type"] == "list":
                default = []

            # Sets all class field vars with defaults.
            field_value = getattr(self, field_name, None)
            if field["type"] == "bool":
                if field_value == False:
                    setattr(self, field_name, False)
                elif field_value:
                    setattr(self, field_name, True)
                else:
                    setattr(self, field_name, default)
            elif not field_value:
                setattr(self, field_name, default)

        return True

    def _set_types(self) -> bool:
        """Set the types of class table field vars and corrects their types where possible
        :unit-test: test___set_types
        """
        for field_name, field in self.field_map.items():
            class_var_name = field['name']

            class_var_value = getattr(self, class_var_name)
            if class_var_value is None:
                continue

            if field['type'] == 'int' and type(class_var_value) != int:
                converted_value = xlate.convert_any_to_int(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'bool':
                converted_value = xlate.convert_int_to_bool(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'datetime' and type(class_var_value) != datetime:
                setattr(
                    self,
                    class_var_name,
                    arrow.get(class_var_value).datetime)
                continue

    def _convert_ints(self, name: str, value) -> bool:
        """Attempts to convert ints to a usable value or raises an AttributeError.
        :unit-test: test___convert_ints
        """
        if isinstance(value, int):
            return value
        if isinstance(value, str) and value.isdigit():
            logging.warning('Class %s field %s value %s is not int, changed to int.' % (
                __class__.__name__, name, value))
            return int(value)
        raise AttributeError('Class %s field %s value %s is not int.' % (
            __class__.__name__, name, value))

    def _generate_create_table_feilds(self) -> str:
        """Generates all fields column create sql statements.
           :unit-test: test___generate_create_table_feilds
        """
        field_sql = ""
        field_num = len(self.field_map)
        c = 1
        for field_name, field in self.field_map.items():
            if field["type"] == "unique_key":
                continue
            primary_stmt = ''
            if 'primary' in field and field['primary']:
                primary_stmt = ' PRIMARY KEY'
                if self.backend == "mysql":
                    primary_stmt += ' AUTO_INCREMENT'
            if "extra" in field:
                primary_stmt = " %s" % field["extra"]

            not_null_stmt = ''
            if 'not_null' in field and field['not_null']:
                not_null_stmt = ' NOT NULL'

            default_stmt = ''
            if 'default' in field and field['default']:
                if field['type'] == "str":
                    default_stmt = ' DEFAULT "%s"' % field['default']
                elif field["type"] == "list":
                    default_stmt = ' DEFAULT "%s"' % ",".join(field['default'])
                else:
                    default_stmt = ' DEFAULT %s' % field['default']

            field_line = "`%(name)s` %(type)s%(primary_stmt)s%(not_null_stmt)s%(default_stmt)s," % {
                'name': field['name'],
                'type': self._xlate_field_type(field['type']),
                'primary_stmt': primary_stmt,
                'not_null_stmt': not_null_stmt,
                'default_stmt': default_stmt
            }
            field_sql += field_line

            if c == field_num:
                field_sql = field_sql[:-1]
            field_sql += "\n"
            c += 1

        for field_name, field in self.field_map.items():
            if field["type"] == "unique_key":
                field_sql += "UNIQUE KEY %s (%s)" % (field["name"], ",".join(field["fields"]))
        field_sql = field_sql[:-1]
        return field_sql

    def _xlate_field_type(self, field_type: str) -> str:
        """Translates field types into sql lite column types.
           @todo: create better class var for xlate map.
           :unit-test: test
        """
        if self.backend == "mysql":
            if field_type == 'int':
                return 'INTEGER'
            elif field_type == 'datetime':
                return 'DATETIME'
            elif field_type[:3] == 'str':
                return 'VARCHAR(200)'
            elif field_type == 'text':
                return "TEXT"
            elif field_type == 'bool':
                return 'TINYINT(1)'
            elif field_type == 'float':
                return 'DECIMAL(10, 5)'
            elif field_type == 'list':
                return "TEXT"
            elif field_type == "json":
                return "JSON"
            else:
                raise AttributeError(f'Unknown data type: "{field_type}"')

    def _establish_db(self, conn, cursor) -> bool:
        self.conn = conn
        if not self.conn and "conn" in glow.db:
            self.conn = glow.db["conn"]
        self.cursor = cursor
        if not self.cursor and "cursor" in glow.db:
            self.cursor = glow.db["cursor"]
        return True

# End File: gather/src/api/models/base.py
