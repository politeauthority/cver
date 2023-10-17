"""
    Cver Client
    Create Users Example
    Using the CverClient, we'll create a new User and ApiKey for that User.

"""
import logging

from cver.cver_client.models.user import User
from cver.cver_client.models.api_key import ApiKey


def test():
    user = User()
    user.get_by_id(1)


if __name__ == "__main__":
    test()

# End File: cver/examples/create_user.py
