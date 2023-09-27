"""
    Cver Test Tools
    Fixture: DB
    Mock a db connection.

"""
import logging

conn = True
cursor = None


class Conn:

    def commit(self):
        return True


class Cursor:

    def __init__(self, one=None, two=None):
        self.lastrowid = 1
        return None

    def execute(self, sql: str) -> bool:
        logging.debug("Would have executed: %s" % sql)
        return True

    def commit(self):
        return True

# End File: cver/tests/cver-test-tools/fixtures/db.py
