#!/bin/sh -l
# Cver Api Entry Point
set -e
echo "Cver Ingest Starting"
cd /app/cver/ingest
python3 ingest.py
