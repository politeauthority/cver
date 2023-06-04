#!/bin/sh -l
# Cver Api Entry Point
set -e
echo "Cver Api Starting"
# python3 /app/cver/migrate/migrate.py
# echo "Migrations Completed"
cd /app/cver/api
gunicorn app:app --bind 0.0.0.0:80
