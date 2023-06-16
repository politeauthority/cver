#!/usr/bin/env python3

from setuptools import setup

setup(
    name="cver",
    description="Cver",
    version="0.0.1",
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
        "cver.cver_client",
        "cver.cver_client.collections",
        "cver.cver_client.models",
        "cver.ingest",
        "cver.migrate",
        "cver.migrate.data",
        "cver.shared",
        "cver.shared.models",
        "cver.shared.utils",
    ],
)
