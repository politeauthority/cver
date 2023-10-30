"""
    Cver Test Unit
    Api Util: Api Utils
    Source: src/cver/api/utils/api_util.py

"""
from cver.api.utils import api_util


class TestApiUtilApiUtil:

    def test___get_search_field_args(self):
        """
        """
        assert {} == api_util._get_search_field_args({})
        payload = {
            "fields": {
                "sync_enabled": True
            }
        }
        expected = {
            "fields": {
                "sync_enabled": {
                    "field": "sync_enabled",
                    "value": True,
                    "op": "="
                }
            }
        }
        assert expected == api_util._get_search_field_args(payload)