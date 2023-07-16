"""
    Cver Test Unit
    Shared Model: Cluster
    Source: cver/src/cver/shared/model/cluster_image.py
"""

from cver.shared.models.cluster_image import FIELD_MAP


FIELD_DETAILS = ["name", "type", "primary", "default", "extra", "api_display", "api_writeable",
                 "api_searchable"]


class TestSharedModelClusterImage:

    def test__FIELD_MAP(self):
        """Test the ClusterImage model's initialization.
        :data: cluster.FIELD_MAP
        """
        assert isinstance(FIELD_MAP, dict)
        for field_name, field in FIELD_MAP.items():
            assert isinstance(field_name, str)
            assert "name" in field
            for field_detail, field_detail_value in field.items():
                assert field_detail in FIELD_DETAILS


# End File: cver/tests/unit/shared/models/test_shared_model_cluster_image.py
