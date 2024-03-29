"""
    Cver Test Unit
    Api Util: Api Utils
    Source: src/cver/api/utils/api_util.py

"""
from cver.api.utils import api_util


class TestApiUtilApiUtil:

    def test___get_search_field_args(self):
        """Get search field arguments from a url query string.
        :method: api_util._get_search_field_args()
        """
        assert {} == api_util._get_search_field_args({})
        payload = {
            "name": "hello-world",
            "page": 2
        }
        expected = {
            "name": {
                "field": "name",
                "value": "hello-world",
                "op": "="
            }
        }
        assert expected == api_util._get_search_field_args(payload)

    def test___post_search_field_args(self):
        """Get search field arguments from a request.
        :method: api_util._post_search_field_args()
        """
        assert {} == api_util._post_search_field_args({})
        payload = {
            "fields": {
                "sync_enabled": True
            }
        }
        expected = {
            "sync_enabled": {
                "field": "sync_enabled",
                "value": True,
                "op": "="
            }
        }
        assert expected == api_util._post_search_field_args(payload)

    def test___post_search_order_args(self):
        """Get the order segment of a search
        :method: api_util._post_search_order_args()
        """
        assert {} == api_util._post_search_order_args({})
        payload = {
            "order_by": {
                "field": "id",
                "direction": "desc"
            }
        }
        expected = {
            "field": "id",
            "direction": "desc"
        }
        assert expected == api_util._post_search_order_args(payload)

    def test___post_search_limit_args(self):
        """Get limit arg from a request.
        :method: api_util._post_search_limit_args()
        """
        assert not api_util._post_search_limit_args({})
        payload = {
            "limit": 5
        }
        assert 5 == api_util._post_search_limit_args(payload)

# End File: cver/tests/api/utils/test_api_utils.py
