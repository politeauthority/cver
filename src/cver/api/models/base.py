"""Base Model v. 0.2.0
Parent class for all models to inherit, providing methods for creating tables, inserting, updating,
selecting and deleting data.

The Base Model SQL driver can work with both SQLite3 and MySQL database.
    self.backend = "sqlite" for SQLite3
    self.backend = "mysql" for MySQL

Testing:
    Unit test file  cver/tests/unit/api/models/test_base.py
    Unit tested     38/46

"""
from datetime import datetime
import json
import logging

import arrow
from pymysql.err import ProgrammingError, IntegrityError

from cver.shared.utils import xlate
from cver.shared.utils import date_utils
from cver.api.utils import glow


class Base:

    def __init__(self, conn=None, cursor=None):
        """Base model constructor
        :unit-test: TestApiModelBase::test____init__
        """
        self._establish_db(conn, cursor)
        self.backed_iodku = True
        self.backend = "mysql"

        self.table_name = None
        self.entity_name = None
        self.field_map = {}
        self.field_meta = {}
        self.immutable = False
        self.insert_iodku = False
        self.id = None
        self.setup()

    def __repr__(self):
        """Base model representation
        :unit-test: TestApiModelBase::test____repr__
        """
        if self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def __desc__(self) -> None:
        """Describes the fields and values of class.
        :unit-test: TestApiModelBase::test____repr__
        """
        for field_id, field in self.field_map.items():
            print("%s: %s" % (field["name"], getattr(self, field["name"])))

    def connect(self, conn, cursor) -> bool:
        """Quick bootstrap method to connect the model to the database connection.
        :unit-test: TestApiModelBase::test__connect
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
        """Create a table based SQL on the self.table_name, and self.field_map.
        :unit-test: TestApiModelBase::test__create_table_sql
        """
        if not self.table_name:
            raise AttributeError('Model table name not set, (self.table_name)')
        sql = "CREATE TABLE IF NOT EXISTS %s \n(%s)" % (
            self.table_name,
            self._generate_create_table_feilds())
        return sql

    def setup(self) -> bool:
        """Set up model class vars, sets class var defaults, and corrects types where possible.
        :unit-test: TestApiModelBase::test__setup
        """
        self._set_defaults()
        self._set_types()
        return True

    def save(self) -> bool:
        """Saves a model instance in the model table.
        :unit-test: TestApiModelBase::test__save
        """
        self.setup()
        self.check_required_class_vars()

        if self._is_model_json():
            return self.insert()
        if not self.id:
            if self.backed_iodku and self.insert_iodku:
                return self.iodku()
            else:
                return self.insert()
        if not self.id:
            logging.error("Save failed, missing %s.id or where list" % __class__.__name_)
            raise AttributeError("Save failed, missing %s.id or where list" % __class__.__name_)
        update_sql = self._gen_update_sql(["id", "created_ts"])
        try:
            self.cursor.execute(update_sql)
        except IntegrityError as e:
            logging.error("Mysql Integrity Error for %s: %s" % (self, e))
            return False
        self.conn.commit()
        return True

    def insert(self):
        """Insert a new record of the model.
        :unit-test: TestApiModelBase::test__insert
        """
        sql = self._gen_insert_sql()
        try:
            logging.info("\n\nINSERT\n%s\n\n" % sql)
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
        :unit-test: TestApiModelBase::test__iodku
        """
        sql = self._gen_iodku_sql()
        logging.info("\n\nIODKU\n%s\n\n" % sql)
        self.cursor.execute(sql)
        self.conn.commit()
        self.id = self.cursor.lastrowid
        return True

    def delete(self) -> bool:
        """Delete a model item.
        :unit-test: TestApiModelBase::test__delete()
        """
        sql = self._gen_delete_sql()
        self.cursor.execute(sql)
        self.conn.commit()
        return True

    def get_by_id(self, model_id: int = None) -> bool:
        """Get a single model object from db based on an object ID.
        :unit-test: TestApiModelBase::test__get_by_id()
        """
        if model_id:
            self.id = model_id

        if not self.id:
            raise AttributeError('%s is missing an ID attribute.' % __class__.__name__)

        if not model_id:
            raise AttributeError('%s is missing an ID attribute.' % __class__.__name__)

        if not isinstance(model_id, int):
            raise AttributeError('%s ID attribute must be int ' % __class__.__name__)

        sql = self._gen_get_by_id_sql()
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False

        self.build_from_list(raw)

        return True

    def get_by_name(self, name: str) -> bool:
        """Get a model by name, if the model has a name field.
        :unit-test: TestApiModelBase::test__get_by_name()
        """
        if "name" not in self.field_map:
            raise AttributeError('%s does not have a `name` attribute.' % __class__.__name__)
        sql = self._gen_get_by_name_sql(name)

        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_unique_key(self, fields: dict) -> bool:
        """Get a model by it's unique keys.
        :param fields: A dict of key values, corresponding to models unique keys.
            {
                "field": "value",
                "value": "A Cool Name",
            }
        :unit-test: TestApiModelBase::test__get_by_unique_key
        """
        if not self.field_meta:
            return False
        sql = self._gen_get_by_unique_key_sql(fields)
        logging.info("\n\n%s\n\n" % sql)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

    def get_by_field(self, field: str, value: str) -> bool:
        """Get a model by specific, if the model has a name field."""
        if field not in self.field_map:
            raise AttributeError('%s missing Attribute "%s"' % (self, field))
        field = {
            "field": field,
            "value": value,
            "op": "eq"
        }
        sql = self._gen_get_by_field_sql(field=field)
        # logging.info(sql)
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
        sql_fields = self._gen_get_by_fields_sql(fields)
        sql = """
            SELECT *
            FROM %s
            WHERE %s
            LIMIT 1;""" % (self.table_name, sql_fields)

        logging.info("\nGET BY FIELDS\n%s\n" % sql)

        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

    def get_last(self) -> bool:
        """Get the last created model."""
        sql = self._gen_get_last_sql()

        self.cursor.execute(sql)
        run_raw = self.cursor.fetchone()
        if not run_raw:
            return False
        self.build_from_list(run_raw)
        return True

    def get_field(self, field_name: str):
        """Get the details on a model field from the field map.
        :unit-test: TestApiModelBase::test__get_field
        """
        for field_name, field in self.field_map.items():
            if field["name"] == field_name:
                return field
        return None

    def build_from_list(self, raw: list) -> bool:
        """Build a model from an ordered list, converting data types to their desired type where
        possible.
        :@todo: Simplify this method, it's too big.
        :param raw: The raw data from the database to be converted to model data.
        :unit-test: TestApiModelBase::test__build_from_list
        """
        if len(self.field_map) != len(raw):
            msg = "BUILD FROM LIST Model: %s field_map: %s, record: %s \n" % (
                self,
                len(self.field_map),
                len(raw))
            msg += "Model Fields: %s\n" % (self.field_map.keys())
            msg += "Field Map: %s\n" % str(self.field_map)
            msg += "Raw Record: %s\n" % str(raw)
            msg += "Maybe .setup() has not been run"
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

            elif field["type"] == "json":
                json_value = json.loads(field_value)
                setattr(self, field_name, json_value)

            # Handle all other field types without any translation.
            else:
                setattr(self, field_name, field_value)

            count += 1

        return True

    def build_from_dict(self, raw: dict) -> bool:
        """Builds a model by a dictionary. This is expected to be used mostly from a client making
        a request from a web api.
        :unit-test: TestApiModelBase::test__build_from_dict
        """
        for field, value in raw.items():
            if not hasattr(self, field):
                continue

            if self.field_map[field]["type"] == "datetime":
                if isinstance(value, str):
                    value = date_utils.date_from_json(value)
            setattr(self, field, value)

        return True

    def json(self, get_api: bool = False) -> dict:
        """Create a JSON friendly output of the model, converting types to friendlies. If get_api
        is specified and a model doesnt have api_display=False, it will export in the output.
        :unit-test: TestApiModelBase::test__json
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

    def _gen_insert_sql(self, skip_fields: list = ["id"]) -> tuple:
        """Generate the insert SQL statement.
        :unit-test: TestApiModelBase::test___gen_insert_sql
        """
        # import ipdb; ipdb.set_trace()
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

    def _gen_delete_sql(self) -> str:
        """Generate the SQL for deleting a record.
        :unit-test: TestApiModelBase::test___gen_delete_sql
        """
        if not self.id:
            raise AttributeError('%s missing Attribute "id"' % self)
        return """DELETE FROM `%s` WHERE `id` = %s;""" % (self.table_name, xlate.sql_safe(self.id))

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
        :unit-test: TestApiModelBase::test___gen_get_by_id_sql
        """
        sql = """
            SELECT *
            FROM `%(table)s`
            WHERE `id` = %(model_id)s;""" % {
            "table": self.table_name,
            "model_id": xlate.sql_safe(self.id)
        }
        return sql

    def _gen_get_by_name_sql(self, name) -> str:
        """
        :unit-test: TestApiModelBase::test___gen_get_by_name_sql
        """
        sql = """
            SELECT *
            FROM `%s`
            WHERE `name` = "%s";""" % (self.table_name, xlate.sql_safe(name))
        return sql

    def _gen_get_by_unique_key_sql(self, fields: dict) -> str:
        """Generate a  SQL statement to get a model by it's unique keys.
        :param fields: list of dict
            fields
            {
                "field": "value",
                "another_field: "another value"
            }
        :unit-test: TestApiModelBase::test___gen_get_by_unique_key_sql
        """
        unique_key_fields = self.field_meta["unique_key"]
        if len(fields) != len(unique_key_fields):
            log_warn = "_gen_get_by_unique_key_sql\tModel: %s Submitted fields: %s - unique key: %s"
            log_warn = log_warn % (self, fields, unique_key_fields)
            logging.warning(log_warn)
            attr_error = "%s has a unique key number %s, %s fields were submitted. Check"
            attr_error += "above for submitted values"
            attr_error = attr_error % (
                self,
                len(unique_key_fields),
                len(fields)
            )
            raise AttributeError(attr_error)

        for field_name, field_value in fields.items():
            if field_name not in unique_key_fields:
                raise AttributeError("%s does not have a unique key of %s" % (self, field_name))

        prep_gen_fields = []
        for field_name, field_value in fields.items():
            the_field = {
                "field": field_name,
                "value": field_value,
                "op": "eq"
            }
            prep_gen_fields.append(the_field)
        fields_sql = self._gen_get_by_fields_sql(prep_gen_fields)
        sql = """
            SELECT *
            FROM %s
            WHERE
                %s
            LIMIT 1;
        """ % (self.table_name, fields_sql)
        return sql

    def _gen_get_by_field_sql(self, field) -> str:
        """
        :unit-test: TestApiModelBase::test___gen_get_by_field_sql
        """
        field_sql = self._gen_get_by_fields_sql(fields=[field])
        sql = """
            SELECT *
            FROM %s
            WHERE
                %s
            LIMIT 1;
        """ % (self.table_name, field_sql)
        return sql

    def _gen_get_by_fields_sql(self, fields: list) -> str:
        """Generate a str for one or many search fields.
        :param fields: list of dict
            fields
            [
                {
                    "field": "name",
                    "value": "A Cool Name",
                    "op": "eq"
                }
            ]
        :returns: `slug_name` = "admin"
        :unit-test: TestApiModelBase::test___gen_get_by_fields_sql
        """
        sql_fields = ""
        for field in fields:
            field_name = "`%s`" % field["field"]

            if not field["value"]:
                operation = "IS"
            # elif field["type"] == "list":
            #     operation = "IN"
            elif field["op"] == "eq":
                operation = "="
            else:
                logging.error("Unanticipated operation value: %s for model: %s" % (
                    field["op"],
                    self))
            value = self._sql_field_value(self.field_map[field["field"]], field)
            sql_fields += '%s %s %s AND ' % (
                field_name,
                operation,
                value)
        sql_fields = sql_fields[:-5]
        return sql_fields

    def _gen_get_last_sql(self) -> str:
        """Generate the last created row SQL.
        :unit-test: TestApiModelBase::test___gen_get_last_sql
        """
        sql = """
            SELECT *
            FROM %s
            ORDER BY created_ts DESC
            LIMIT 1""" % (self.table_name)
        return sql

    def _sql_field_value(self, field_map_info: dict, field_data: dict):
        """Get the correctly typed value for a field, santized and ready for use in SQL.
        :unit-test: TestApiModelBase::test___sql_field_value
        """
        if field_data["value"] is None:
            return "NULL"

        # Handle ints
        if field_map_info["type"] == "int":
            value = xlate.sql_safe(field_data["value"])

        # Handle bools
        elif field_map_info["type"] == "bool":
            if field_data["value"] == True:
                value = 1
            elif field_data["value"] == False:
                value = 0
            else:
                logging.error("Unanticipated bool value: %s for model: %s" % (
                    field_data["value"],
                    self))
                return False

        # Handle lists
        elif field_map_info["type"] == "list":
            value = '("%s")' % xlate.sql_safe(field_data["value"])

        # Handle str and everything else
        else:
            value = '"%s"' % xlate.sql_safe(field_data["value"])

        return value

    def _sql_fields_sanitized(self, skip_fields: dict) -> str:
        """Get all class table column fields in a comma separated list for sql cmds. Returns a value
            like: `id`, `created_ts`, `update_ts`, `name`, `vendor`.
        :unit-test: TestApiModelBase::test___sql_fields_sanitized
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
        :unit-test: TestApiModelBase::test___sql_insert_values_santized
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
        :unit-test: TestApiModelBase::test___sql_update_fields_values_santized
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
        :unit-test: None
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

    def _get_sql_value_santized_typed(self, field: dict, value) -> str:
        """Convert values to a safe santized value based on it's type.
        :unit-test: TestApiModelBase::test___get_sql_value_santized_typed
        """
        # Handle converting int value
        if field["type"] == "int":

            value = int(value)
            value = xlate.sql_safe(value)

        # Handle converting a list value
        elif field["type"] == "list":
            if not isinstance(value, list) and value.isdigit():
                value = str(value)
            value = '"%s"' % xlate.sql_safe(xlate.convert_list_to_str(value))

        # Handle converting a bool
        elif field["type"] == "bool":
            value = xlate.sql_safe(xlate.convert_bool_to_int(value))

        elif field["type"] == "str":
            value = str(value)
            if value and len(value) > 200:
                value = value[:200]
                logging.warning("Truncating value for %s in field: %s" % (self, field["name"]))
            value = '"%s"' % xlate.sql_safe(value)

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
        :unit-test: TestBase::test__check_required_class_vars
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
        :unit-test: TestApiModelBase::test___set_defaults
        """
        self.field_list = []
        # import ipdb; ipdb.set_trace()
        for field_name, field in self.field_map.items():
            field_name = field['name']
            self.field_list.append(field_name)

            default = None
            if 'default' in field:
                default = field['default']

            # Sets all class field vars with defaults.
            field_value = getattr(self, field_name, None)
            if field_value:
                continue

            if field["type"] == "bool":
                if field_value == False:
                    setattr(self, field_name, False)
                elif field_value:
                    setattr(self, field_name, True)
                else:
                    setattr(self, field_name, default)
            elif field["type"] == "list":
                setattr(self, field_name, [])
            elif not field_value:
                setattr(self, field_name, default)

        return True

    def _set_types(self) -> bool:
        """Set the types of class table field vars and corrects their types where possible.
        :unit-test: TestApiModelBase::test___set_types
        """
        for field_name, field in self.field_map.items():
            class_var_name = field['name']

            class_var_value = getattr(self, class_var_name)
            if class_var_value is None:
                continue

            if field['type'] == 'int' and type(class_var_value) is not int:
                converted_value = xlate.convert_any_to_int(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'bool':
                converted_value = xlate.convert_int_to_bool(class_var_value)
                setattr(self, class_var_name, converted_value)
                continue

            if field['type'] == 'datetime' and type(class_var_value) is not datetime:
                setattr(
                    self,
                    class_var_name,
                    self._get_datetime(class_var_value))
                continue

    def _generate_create_table_feilds(self) -> str:
        """Generates all fields column create sql statements.
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
        :unit-test: TestApiModelBase.test___xlate_field_type
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

    def _is_model_json(self) -> bool:
        """Check if a model contains a JSON field type, if it does, return True.
        :unit-test: TestApiModelBase:test___is_model_json
        """
        for field_name, field_info in self.field_map.items():
            if field_info["type"] == "json":
                return True
        return False

    def _get_datetime(self, date_string: str) -> datetime:
        """Attempt to get a Python native datetime from a date string.
        :unit-test: TestApiModelBase:test____get_datetime
        """
        if len(date_string) == 26:
            try:
                parse_format = "YYYY-MM-DD HH:mm:ss ZZ"
                parsed_date = arrow.get(date_string, parse_format)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s with with format: %s" % (
                    date_string,
                    parse_format))
        elif len(date_string) == 19:
            try:
                parse_format = "YYYY-MM-DD HH:mm:ss"
                parsed_date = arrow.get(date_string, parse_format)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s with format: %s " % (
                    date_string,
                    parse_format))
        else:
            try:
                parsed_date = arrow.get(date_string)
                return parsed_date.datetime
            except arrow.parser.ParserMatchError:
                logging.error("Couldnt parse date str: %s" % date_string)
                return None
            except arrow.parser.ParserError:
                logging.error("Couldnt parse date str: %s" % date_string)
                return None

# End File: cver/src/cver/api/models/base.py
