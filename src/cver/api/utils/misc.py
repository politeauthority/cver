"""Misc Server

"""
import codecs
import pickle
import os

from cver.shared.utils import log
from cver.api.collects.options import Options
from cver.api.utils import db
from cver.api.utils import glow


def get_option_value(option_name: str, default=None):
    """Get just the value of an Option, with an optional default if supplied."""
    option = glow.options.get(option_name)
    if not option:
        return default
    return option.value


def get_pignus_path() -> str:
    """Get the path to the Pignus repository through the PIGNUS_PATH environment var."""
    pignus_path = os.environ.get("PIGNUS_PATH")
    if not pignus_path:
        log.error("Could not determine Pignus path, please set PIGNUS_PATH enviornment var")
        return False
    return pignus_path


def get_pignus_migrations_path() -> str:
    """Get the Pignus migrations through  the PIGNUS_MIGRATIONS_PATH environment var."""
    pignus_path = os.environ.get("PIGNUS_MIGRATIONS_PATH", "/app/migrations")
    if not pignus_path:
        log.error(
            "Could not determine Pignus mgrations path, please set PIGNUS_MIGRATIONS_PATH "
            "enviornment var")
        return False
    return pignus_path


def set_db():
    conn, cursor = db.connect_mysql(glow.server["DATABASE"])
    glow.db["conn"] = conn
    glow.db["cursor"] = cursor
    glow.options = Options(conn, cursor).load_options()
    return True


def pickle_in(data) -> str:
    """Takes a native Python object and pickles the data, then base64 encodes it to make it more
    portable.
    """
    picked_data = pickle.dumps(data)
    encoded_data = codecs.encode(picked_data, "base64").decode()
    return encoded_data


def pickle_out(data):
    """Takes input data and attemps to decode a base64 value, then load that value as a native
    Python object back out.
    @todo: Catch the exceptions better here.
    """
    if not data:
        log.warning("Cannot pickle out None")
        return None

    # Decode the value from base64
    encode_data = data.encode()
    try:
        bas64_decoded_out = codecs.decode(encode_data, 'base64')
    except Exception as e:
        log.error("Cannot pickle out: %s.\n%s" % (data, e), exception=e)
        return None

    the_object = pickle.loads(bas64_decoded_out)
    return the_object


# End File: cver/src/api/utils/misc.py
