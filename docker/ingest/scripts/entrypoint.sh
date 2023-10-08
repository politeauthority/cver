#!/bin/sh -l
# Cver Ingest Entrypoint
set -e
echo "Cver Ingest Starting"
/usr/bin/timeout ${TIMEOUT_SECONDS} python3 /app/cver/ingest/ingest.py
