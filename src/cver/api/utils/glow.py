#!/usr/bin/env python
"""
    Cver Api
    Glow
    Global variables for the Cver Api.

"""
import os

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

global options
options = {}

global general
general = {
    "LOG_LEVEL": "INFO",
    "VERSION": "0.0.1",
    "CVER_BUILD": os.environ.get("CVER_BUILD"),
    "CVER_ENV": os.environ.get("CVER_ENV"),
    "CVER_JWT_EXPIRE_MINUTES": os.environ.get("CVER_JWT_EXPIRE_MINUTES", 60),
    "CVER_SECRET_KEY": os.environ.get("CVER_SECRET_KEY"),
}

# End File: cver/src/cver/api/utils/glow.py
