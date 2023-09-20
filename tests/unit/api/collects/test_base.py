"""
    Cver - Test - Unit
    Collects - Base

"""
from cver.api.collects.base import Base
from cver.api.collects.api_keys import ApiKeys
from cver_test_tools.fixtures import db


class TestApiCollectsBase:

    def test____init__(self):
        """
        :method: Base().__init__()
        """
        base = Base()
        assert hasattr(base, "conn")
        assert hasattr(base, "cursor")
        assert hasattr(base, "table_name")
        assert hasattr(base, "collect_model")

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

# End File: cver/tests/unit/api/collects/test_base.py
