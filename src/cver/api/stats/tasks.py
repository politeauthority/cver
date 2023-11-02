"""
    Cver Api
    Stats
    Tasks

"""

# from cver.api.collects.tasks import Tasks
from cver.api.utils import glow
from cver.shared.utils import misc


def get_task_totals():
    return {
        "lifetime": {
            "total": _task_totals(),
            "download": _task_totals("engine-download"),
            "scan": _task_totals("engine-scan")
        }
    }


def _task_totals(name: str = None):
    where = ""
    if name:
        where = 'WHERE name="%s"' % name
    sql = """
        SELECT distinct(`status`), count(*)
        FROM `tasks`
        %(where)s
        GROUP BY 1
    """ % {
        "where": where
    }
    glow.db["cursor"].execute(sql)
    result = glow.db["cursor"].fetchall()
    ret = {}
    for row in result:
        if row[0] == 1:
            ret["success"] = row[1]
        elif row[0] == 0:
            ret["failed"] = row[1]

    if "success" not in ret:
        ret["success"] = 0
    if "failed" not in ret:
        ret["failed"] = 0
    ret["total"] = ret["success"] + ret["failed"]
    ret["success_rate"] = "%s" % misc.percentize(ret["success"], ret["total"]) + "%"

    return ret


# End File: cver/src/api/stats/tasks.py
