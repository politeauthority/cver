"""
    Cver Client Unit Test
    Client Collection: Base
    Source: cver/src/cver/cver_client/collections/client_collections_base.py

"""

# from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


# class TestClientCollectionBase:

#     def test____init__(self):
#         """
#         :method: ClientCollectionsBase().__init__
#         """
#         collect_base = ClientCollectionsBase()
#         assert hasattr(collect_base, "response_last")

#     def test___prepare_search(self):
#         """
#         :method: ClientCollectionsBase()._prepare_search
#         """
#         collect_base = ClientCollectionsBase()
#         args = {
#             "fields": {
#                 "waiting_for": {
#                     "value": "scan"
#                 },
#                 "fail_count": {
#                     "op": "lt",
#                     "value": 1
#                 }
#             },
#             "order_by": {
#                 "field": "id",
#                 "direction": "ASC"
#             },
#             "limit": 5
#         }
#         result = collect_base._prepare_search(args)
#         import ipdb; ipdb.set_trace()

# End File: cver/tests/cver_client/collections/test_client_collections_base.py
