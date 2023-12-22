"""
    Cver Shared
    Utils
    Kubernetes
    Utilities for interacting with kubernetes

"""
import base64
import yaml


def create_secret(secret_name: str, data: dict) -> bool:
    secrets = {}
    for key, secret in data.items():
        secrets[key] = base64.b64encode(secret.encode("utf-8")).decode()

    yaml_secret = {
        "apiVersion": "v1",
        "data": secrets,
        "kind": "Secret",
        "metadata": {
            "name": secret_name
        },
        "type": "Opaque"
    }
    with open("secret-%s.yaml" % secret_name, "w") as file:
        yaml.dump(yaml_secret, file)
    return True

# End File: cver/src/cver/shared/utils/kubernetes.py
