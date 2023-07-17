"""
    Cver Client
    Ingest - K8s

"""
from cver.cver_client import CverClient


class IngestK8s(CverClient):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(IngestK8s, self).__init__()

    def image(self, cluster_id: int, image: str) -> bool:
        """Submit a k8s image to /ingest-k8s/image endpoint."""
        data = {
            "cluster_id": cluster_id,
            "image": image
        }
        response = self.make_request("/ingest-k8s/image", method="POST", payload=data)
        return response

# End File: cver/src/cver_client/ingest/k8s.py
