#!/bin/sh -l
# Cver Engine Entrypoint
set -e
echo "Cver Engine Starting"
/usr/bin/timeout ${TIMEOUT_SECONDS} python3 /app/cver/engine/engine.py
