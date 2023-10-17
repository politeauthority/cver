"""
    Cver Client
    Create Users Example
    Using the CverClient, we'll create a new User and ApiKey for that User.

"""
import logging

from cver.cver_client.models.user import User
from cver.cver_client.models.api_key import ApiKey


def create_user():
    user = User()
    user.name = "Alix"
    user.email = "alix@politeauthority.io"
    user.role_id = 1
    saved = user.save()
    if not saved:
        logging.error("Failed to create user.")
        exit(1)

    api_key = ApiKey()
    api_key.user_id = 3
    api_key.save()

    print(f"Created {user}")
    print(f"\tClient ID:\t{api_key.client_id}")
    print(f"\tApi Key:\t{api_key.key}")


if __name__ == "__main__":
    create_user()

# End File: cver/examples/create_user.py
