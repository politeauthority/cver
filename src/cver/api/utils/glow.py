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
    "HOST": "",
    "PORT": "",
    "USER": "",
    "PASS": "",
    "NAME": "",
}

global options
options = {}

global general
general = {
    "LOG_LEVEL": "INFO",
    "VERSION": "0.0.1",
    "CVER_BUILD": os.environ.get("CVER_BUILD"),
    "CVER_ENV": os.environ.get("CVER_ENV")
}

# End File: cver/src/cver/api/utils/glow.py
