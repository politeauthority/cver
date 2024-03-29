#!/usr/bin/env python3

from setuptools import setup
from cver.api.version import version

setup(
    name="cver",
    description="Cver",
    version=version,
    author="Alix",
    author_email="alix@politeauthority.io",
    packages=[
        "cver.api",
        "cver.api.controllers",
        "cver.api.controllers.ctrl_collections",
        "cver.api.controllers.ctrl_models",
        "cver.api.collects",
        "cver.api.models",
        "cver.api.utils",
        "cver.api.stats",
        "cver.cli",
        "cver.cli.utils",
        "cver.client",
        "cver.client.collections",
        "cver.client.models",
        "cver.client.ingest",
        "cver.client.utils",
        "cver.engine",
        "cver.engine.utils",
        "cver.engine.modules",
        "cver.ingest",
        "cver.migrate",
        "cver.migrate.data",
        "cver.shared",
        "cver.shared.models",
        "cver.shared.utils",
    ],
)

# End File: cver/src/cver/setup.py
