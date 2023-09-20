"""
    Cver - Test - Unit
    CTRL Collection Base

"""
from cver.api.collects.api_keys import ApiKeys
from cver.api.collects.cluster_images import ClusterImages
from cver.api.collects.images import Images
from cver.api.controllers.ctrl_collections import ctrl_collection_base

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
        "api_searchable": True,
    },
    "client_id": {
        "name": "client_id",
        "type": "str",
        "extra": "UNIQUE",
        "api_searchable": True
    },
    "key": {
        "name": "key",
        "type": "str",
        "api_display": False
    },
}


class TestCtrlCollectionBase:

    def test__get_where_and(self):
        """
        :method: ctrl_collection_base._get_object_type
        """
        raw_args = {
            "client_id": 1
        }
        result = ctrl_collection_base._get_where_and(raw_args, FIELD_MAP)
        assert result == [{'field': 'client_id', 'value': 1, 'op': '='}]

    def test___get_object_type(self):
        """
        :method: ctrl_collection_base._get_object_type
        """
        assert ctrl_collection_base._get_object_type(ApiKeys) == "api-key"
        assert ctrl_collection_base._get_object_type(ClusterImages) == "cluster-image"
        assert ctrl_collection_base._get_object_type(Images) == "image"

    def test___get_api_hidden_fields(self):
        """
        :method: ctrl_collection_base._get_api_hidden_fields
        """

        assert ctrl_collection_base._get_api_hidden_fields(FIELD_MAP) == ["key"]


# End File: cver/tests/unit/api/collections/controllers/test_ctrl_collection_base.py
