"""
    Cver Test Unit
    Api Util: Sql Tools
    Source: src/cver/api/utils/sql_tools.py

"""

from cver.api.utils import sql_tools


class TestApiUtilsSqlTools:

    def test__sql_safe(self):
        """Test that we get a safe SQL result back
        :method: sql_tools.sql_safe
        """
        field = "my field"
        assert "my field" == sql_tools.sql_safe(field)

# End File: cver/tests/api/utils/test__sql_tools.py
