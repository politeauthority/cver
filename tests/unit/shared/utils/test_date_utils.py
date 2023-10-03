"""
    Cver Test - Unit
    Cver Shared
    Utils
    Date Utils
    Tests File: cver/src/cver/shared/utils/date_utils.py

"""
from datetime import datetime

import arrow

from cver.shared.utils import date_utils


class TestSharedUtilsDateUtils:

    def test__now(self):
        """
        :method: date_util.now()
        """
        assert isinstance(date_utils.now(), datetime)

    def test__json_date(self):
        """
        :method: date_util.json_date()
        """
        assert isinstance(date_utils.json_date(arrow.utcnow().datetime), str)
        assert 26 == len(date_utils.json_date(arrow.utcnow().datetime))

    def test__json_date_now(self):
        """
        :method: date_util.json_date_now()
        """
        assert isinstance(date_utils.json_date_now(), str)
        assert 19 == len(date_utils.json_date_now())

    def test__human_date(self):
        """
        :method: date_util.human_date()
        """
        now = arrow.utcnow()
        assert "just now" == date_utils.human_date(now)
        assert "2 hours ago" == date_utils.human_date(now.shift(hours=-2))

    def test__get_as_utc(self):
        """
        :method: date_util.get_as_utc()
        """
        assert isinstance(date_utils.get_as_utc(datetime.now()), arrow.arrow.Arrow)

    def test__date_from_json(self):
        """
        :method: date_util.date_from_json()
        """
        date_str = "2023-09-29 21:30:45 +00:00"
        assert isinstance(date_utils.date_from_json(date_str), arrow.arrow.Arrow)

    def test__interval_ready(self):
        """
        :method: date_util.interval_ready()
        """
        five_hours_ago = arrow.utcnow()
        five_hours_ago = five_hours_ago.shift(hours=-5)
        assert date_utils.interval_ready(five_hours_ago.datetime, 2)
        assert not date_utils.interval_ready(five_hours_ago.datetime, 10)


# End File: cver/tests/unit/shared/utils/test_date_utils.py
