"""
    Cver Test Unit
    Shared Model: Cluster

"""

from cver.shared.models.cluster import FIELD_MAP


FIELD_DETAILS = ["name", "type", "primary", "default", "extra", "api_display", "api_writeable",
                 "api_searchable"]


class TestSharedModelCluster:

    def test__FIELD_MAP(self):
        """Test the Cluster model's initialization.
        :data: cluster.FIELD_MAP
        """
        assert isinstance(FIELD_MAP, dict)
        for field_name, field in FIELD_MAP.items():
            assert isinstance(field_name, str)
            assert "name" in field
            for field_detail, field_detail_value in field.items():
                assert field_detail in FIELD_DETAILS


# End File: cver/tests/unit/shared/models/test_cluster.py
