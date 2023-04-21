""" Test Model Base

"""

from cver.api.models.base import Base


class TestBase:

	def test____init__(self):
		"""Test the Base Model's initialization.
		:method: Base().__init__
		"""
		base = Base()
		assert hasattr(base, "table_name")
		assert hasattr(base, "backend")
		assert hasattr(base, "field_map")

	def test____repr__(self):
		"""Test the Base Model's representation.
		:method: Base().__repr__
		"""
		base = Base()
		assert str(base) == "<Base>"

	def test___sql_fields_sanitized(self):
		"""Test the Base Model's representation.
		:method: Base()._sql_fields_sanitized
		"""
		base = Base()
		assert base._sql_fields_sanitized({}) == ""
		base.total_map = {
            "id": {
                "name": "id",
                "type": "int",
                "primary": True,
            }
        }
		assert base._sql_fields_sanitized({}) == "`id`"

# End File: cver/tests/unit/api/models/test_base.py
