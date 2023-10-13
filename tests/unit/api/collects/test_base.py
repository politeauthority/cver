"""
    Cver - Test - Unit
    Collects - Base

"""
# from datetime import datetime

from cver.api.collects.base import Base as CollectBase
# from cver.api.models.base import Base as ModelBase
from cver.api.collects.api_keys import ApiKeys
from cver_test_tools.fixtures import db


class TestApiCollectsBase:

    def test____init__(self):
        """
        :method: Base().__init__()
        """
        base = CollectBase()
        assert hasattr(base, "conn")
        assert hasattr(base, "cursor")
        assert hasattr(base, "table_name")
        assert hasattr(base, "collect_model")

    # def test__get_by_ids(self):
    #     FIELD_MAP = {
    #         "id": {
    #             "name": "id",
    #             "type": "int",
    #             "primary": True,
    #         },
    #         "created_ts": {
    #             "name": "created_ts",
    #             "type": "datetime",
    #         },
    #         "name": {
    #             "name": "name",
    #             "type": "str",
    #         }
    #     }
    #     cursor = db.Cursor()
    #     cursor.result_to_return = [
    #         [1, datetime.now(), "hello"],
    #         [40, datetime.now(), "a second"],
    #         [3, datetime.now(), "the thirds"],
    #     ]
    #     model = ModelBase(db.Conn(), db.Cursor())
    #     model.table_name = "bases"
    #     model.field_map = FIELD_MAP
    #     collect = CollectBase(db.Conn(), cursor)
    #     collect.collect_model = ModelBase
    #     entities = collect.get_by_ids([1, 40, 3])
    #     import ipdb; ipdb.set_trace()

    def test___generate_paginated_sql(self):
        """
        :method: Base()._generate_paginated_sql()
        """
        base = ApiKeys(db.conn, db.cursor)
        result = base._generate_paginated_sql(page=1, where_and=[], order_by={}, limit=20)
        expected = "\n            SELECT *\n            FROM `api_keys`\n            \n            "
        expected += "ORDER BY `created_ts` DESC\n            LIMIT 20 OFFSET 0;"
        assert expected == result

        where_and = {
            "field": "user_id",
            "value": 1,
            "op": "="
        }

        result = base._generate_paginated_sql(page=1, where_and=[where_and], order_by={}, limit=20)
        expected = "\n            SELECT *\n            FROM `api_keys`\n            WHERE "
        expected += "`user_id` = 1\n            ORDER BY `created_ts` DESC\n            LIMIT 20 "
        expected += "OFFSET 0;"
        assert expected == result

    def test___pagination_offset(self):
        """
        :method: Base()._pagination_offset()
        """
        base = CollectBase()
        assert 0 == base._pagination_offset(1, 20)
        assert 20 == base._pagination_offset(2, 20)

    def test___edit_pagination_sql_for_info(self):
        """
        :method: Base()._edit_pagination_sql_for_info()
        """
        base = CollectBase()
        sql = """SELECT * FROM `table` WHERE name LIKE "%thing%" LIMIT 20;"""
        result = base._edit_pagination_sql_for_info(sql)
        expected = """SELECT COUNT(*) FROM `table` WHERE name LIKE "%thing%";"""
        assert expected == result

    def test___pagination_where_and(self):
        """
        :method: Base()._pagination_where_and()
        """
        base = CollectBase()
        where_and = [
            {
                "field": "name",
                "value": "test",
                "op": "="
            }
        ]
        result = base._pagination_where_and(where_and)
        expected = 'WHERE `name` = "test"'
        assert expected == result

    def test__int_list_to_sql(self):
        """
        :method: Base()._int_list_to_sql()
        """
        base = CollectBase()
        assert "1,2,3" == base._int_list_to_sql([1, 2, 3])

    def test___pagination_order(self):
        """
        :method: Base()._pagination_order()
        """
        base = CollectBase()
        result = base._pagination_order()
        expected = "ORDER BY `created_ts` DESC"
        assert expected == result

    def test___get_previous_page(self):
        """
        :method: Base()._get_previous_page()
        """
        base = CollectBase()
        assert not base._get_previous_page(1)
        assert 4 == base._get_previous_page(5)

    def test___get_next_page(self):
        """
        :method: Base()._get_next_page()
        """
        base = CollectBase()
        assert not base._get_next_page(1, 1)
        assert 2 == base._get_next_page(1, 20)

    def test___gen_sql_get_last(self):
        """
        :method: Base()._gen_sql_get_last()
        """
        base = CollectBase()
        base.table_name = "base"
        result = base._gen_sql_get_last(20)
        expected = "\n            SELECT *\n            FROM `base`\n            "
        expected += "ORDER BY created_ts DESC\n            LIMIT 20;"
        assert expected == result

    def test___gen_get_by_ids_sql(self):
        """
        :method: Base()._gen_get_by_ids_sql()
        """
        base = CollectBase()
        base.table_name = "base"
        result = base._gen_get_by_ids_sql([5, 10, 12])
        expected = "\n            SELECT *\n            FROM base\n            "
        expected += "WHERE id IN (10,12,5);"
        assert expected == result


# End File: cver/tests/unit/api/collects/test_base.py
