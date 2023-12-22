"""
    Rescue - User

"""
import logging

import arrow

from cver.api.models.user import User
from cver.api.models.api_key import ApiKey
from cver.api.utils import auth
from cver.api.utils import db


def create_rescue_user_key():
    """Create Rescue User and Api Key."""
    db.connect()
    user = User()
    if not user.get_by_name("admin"):
        logging.info("Could not find a user named admin. We need to create one")
    expire_at = (arrow.utcnow().shift(hours=4)).datetime
    plaintext_api_key = auth.generate_api_key()
    api_key = ApiKey()
    api_key.user_id = user.id
    api_key.client_id = auth.generate_client_id()
    api_key.key = auth.generate_hash(plaintext_api_key)
    api_key.expiration_date = expire_at
    api_key.save()
    print("Api Key")
    print("\tUser ID: %s" % user.id)
    print("\tClient ID: %s" % api_key.client_id)
    print("\tApi Key: %s" % plaintext_api_key)
    print("Warning! Key will expire in 4 hours!")
    return True


if __name__ == "__main__":
    create_rescue_user_key()

# End File: cver/src/cver/rescue/rescue_user.py
