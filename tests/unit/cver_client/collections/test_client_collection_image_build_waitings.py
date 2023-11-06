"""
    Cver Client Unit Test
    Client Collection: ImageBuildWaitings
    Source: cver/src/cver/cver_client/collections/image_build_waitings.py

"""

from cver.client.collections.image_build_waitings import ImageBuildWaitings


class TestClientCollectionImageBuildWaitings:

    def test____init__(self):
        """
        :method: TestClientCollectionImageBuildWaitings().__init__
        """
        collect = ImageBuildWaitings()
        assert hasattr(collect, "response_last")

    def test___prepare_search(self):
        """
        :method: ClientCollectionsBase()._prepare_search
        """
        collect_ibws = ImageBuildWaitings()
        args = {
            "fields": {
                "waiting_for": {
                    "value": "scan"
                },
                "fail_count": {
                    "op": "lt",
                    "value": 1
                }
            },
            "order_by": {
                "field": "id",
                "direction": "ASC"
            },
            "limit": 5
        }
        result = collect_ibws._prepare_search(args)
        assert isinstance(result, dict)
        assert isinstance(result["fields"], dict)
        assert isinstance(result["order_by"], dict)

# End File: cver/tests/cver_client/collections/test_image_build_waitings.py
