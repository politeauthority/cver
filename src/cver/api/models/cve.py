"""Cve Model

"""
from cver.shared.models.cve import FIELD_MAP
from cver.api.models.base import Base
from cver.api.utils import xlate


class Cve(Base):

    model_name = "cve"

    def __init__(self, conn=None, cursor=None):
        """Create the Cve instance."""
        super(Cve, self).__init__(conn, cursor)
        self.table_name = "cves"
        self.field_map = FIELD_MAP
        self.setup()

    def get_by_number(self, number: str):
        """Get a Cve model by it's cve number, like """
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                `number`="%s"; """ % (
            self.table_name,
            xlate.sql_safe(number))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False

        self.build_from_list(raw)
        return True


# End File: cver/src/shared/modles/cve.py
