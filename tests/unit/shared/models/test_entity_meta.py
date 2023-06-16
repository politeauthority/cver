"""
    Cver Test Unit
    Shared Model: EntityMeta

"""

from cver.shared.models.entity_meta import FIELD_MAP

FIELD_DETAILS = ["name", "type", "primary", "default", "extra", "api_display", "api_writeable",
                 "api_searchable"]


class TestSharedModelEntityMeta:

    def test__FIELD_MAP(self):
        """Test the EntityMeta Model's initialization.
        :data: EntityMeta.FIELD_MAP
        """
        assert isinstance(FIELD_MAP, dict)

# End File: cver/tests/unit/shared/models/test_entity_meta.py
