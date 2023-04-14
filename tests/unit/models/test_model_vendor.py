""" Test Model Vendor

"""

from cver.api.models.vendor import Vendor


class TestVendor:

	def test____init__(self):
		"""Test the Vendor Model's initialization.
		:method: Vendor().__init__
		"""
		vendor = Vendor()
		assert hasattr(vendor, "name")
		assert hasattr(vendor, "slug_name")

	def test____repr__(self):
		"""Test the Vendor Model's representation.
		:method: Vendor().__repr__
		"""
		vendor = Vendor()
		assert str(vendor) == "<Vendor>"


# End File: cver/tests/api/models/test_vendor.py
