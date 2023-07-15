#!/usr/bin/env python
"""
    Cver Api
    Glow
    Global variables for the Cver Api.

"""
import os

from cver.api.version import version

global db
db = {
    "conn": "",
    "cursor": "",
    "HOST": os.environ.get("CVER_DB_HOST"),
    "PORT": os.environ.get("CVER_DB_PORT"),
    "USER": os.environ.get("CVER_DB_USER"),
    "PASS": os.environ.get("CVER_DB_PASS"),
    "NAME": os.environ.get("CVER_DB_NAME"),
}

# Load Cver Options
global options
options = {}

# Collect General Details
global general
general = {
    "LOG_LEVEL": "INFO",
    "VERSION": version,
    "CVER_BUILD": os.environ.get("CVER_BUILD"),
    "CVER_BUILD_SHORT": "",
    "CVER_ENV": os.environ.get("CVER_ENV"),
    "CVER_JWT_EXPIRE_MINUTES": os.environ.get("CVER_JWT_EXPIRE_MINUTES", 60),
    "CVER_SECRET_KEY": os.environ.get("CVER_SECRET_KEY"),
    "CVER_TEST": os.environ.get("CVER_TEST", False),
}
if general["CVER_BUILD"]:
    general["CVER_BUILD_SHORT"] = general["CVER_BUILD"][:12]
if general["CVER_TEST"] == "true":
    general["CVER_TEST"] = True
else:
    general["CVER_TEST"] = False

# Store Current User Info
global user
user = None

global session
session = {
    "uuid": None
}

# End File: cver/src/cver/api/utils/glow.py
