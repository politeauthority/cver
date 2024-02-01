#!/bin/sh -l
# Cver Engine Entrypoint
set -e
echo "Cver Engine Starting"
# dockerd --log-level fatal &
#service docker start
echo "Alix - Docker Started"
echo "Starting Engine"
echo $@
/usr/bin/timeout ${TIMEOUT_SECONDS} python3 /app/cver/engine/engine.py $@

# End File: cver/docker/cver-engine/scripts/entrypoint.sh
