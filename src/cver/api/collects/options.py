"""
    Cver Api
    Collection - Options

"""
from cver.api.collects.base import Base
from cver.api.models.option import Option


class Options(Base):

    collection_name = "options"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Options, self).__init__(conn, cursor)
        self.table_name = Option().table_name
        self.collect_model = Option
        self.field_map = self.collect_model().field_map

    def load_options(self) -> dict:
        """Loads all options as dictionary keyed by the Option name."""
        sql = """SELECT * FROM `options`;"""
        self.cursor.execute(sql)
        raws = self.cursor.fetchall()
        options = self.build_from_lists(raws)
        ret = {}
        for option in options:
            ret[option.name] = option
        return ret

# End File: cver/src/api/collects/options.py
