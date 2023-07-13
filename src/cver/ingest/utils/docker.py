"""
Docker
"""
import subprocess


def get_local_images() -> list:
    """Gets all local docker images on a host, attempting to parse them into something useable.
    @todo: This is fragile, ideally should use the JSON formatter, and only get images pulled from a
    remote host.
    """
    # cmd = ["docker", "images", "--digests", "--format", "'{{json .}}'"]
    cmd = ["docker", "images", "--digests"]

    # Execute the command and capture the output
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = process.communicate()

    images = []
    line_no = 0
    for line in stdout.splitlines():
        line_no += 1
        if line_no == 1:
            continue
        # Do something with each line
        split = line.split(" ")
        parts = []
        for seg in split:
            if seg:
                parts.append(seg)

        image = {
            "name": parts[0],
            "tag": parts[1],
            "sha": parts[2]
        }
        images.append(image)
    return images

# End File: cver/src/ingest/utils/docker.py
