# """
#     Create Users for Regression Testing
# """
# # import logging
# import os

# import requests

# CVER_API_URL = os.environ.get("CVER_API_URL")
# CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
# CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")

# USERS = [
#     {
#         "name": "Test Admin",
#         "email": "test.admin@example.com",
#         "role_slug": "admin"
#     },
#     {
#         "name": "Test Role",
#         "email": "test.reader@example.com",
#         "role_slug": "reader"
#     },
#     {
#         "name": "Test Contributor",
#         "email": "test.contributor@example.com",
#         "role_slug": "contributor"
#     }
# ]


# class MakeTestUsers:

#     def __init__(self):
#         self.token = None

#     def run(self):
#         if not self.login():
#             # logging.error("Could't auth client-id: %s" % CVER_CLIENT_ID)
#             exit(1)

#         self.create_users()

#     def login(self) -> bool:
#         """Gets a JWT from the Cver api."""
#         request_args = {
#             "headers": {
#                 "client-id": CVER_CLIENT_ID,
#                 "x-api-key": CVER_API_KEY,
#                 "content-type": "application/json"
#             },
#             "method": "POST",
#             "url": "%s/auth" % CVER_API_URL,
#         }

#         response = requests.request(**request_args)
#         if response.status_code != 200:
#             print("ERROR: %s logging in" % response.status_code)
#             return False
#         response_json = response.json()
#         self.token = response_json["token"]
#         return True

#     def get_headers(self):
#         "Format headers for test requests with the current JWT."
#         return {
#             "token": self.token,
#             "content-type": "application/json"
#         }

#     def create_users(self):
#         for user in USERS:
#             self.create_user(user)

#     def create_user(self, user_dict: dict):
#         user = self.get_user_by_email(user_dict["email"])

#     def get_user_by_email(self, user_dict: dict):
#         request_args = {
#             "headers": self.get_headers(),
#             "method": "GET",
#             "url": "%s%s/user" % CVER_API_URL,
#             "params": {
#                 "email": user_dict["email"]
#             }
#         }
#         response_user = requests.request(**request_args)
#         print(response_user)
#         import ipdb; ipdb.set_trace()
