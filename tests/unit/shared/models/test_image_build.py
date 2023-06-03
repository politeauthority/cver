"""
    Cver Test Unit
    Shared Model: ImageBuild

"""

from cver.shared.models.image_build import FIELD_MAP


FIELD_DETAILS = ["name", "type", "primary", "default", "extra", "api_writeable", "api_searchable"]


class TestSharedImageBuild:

    def test__FIELD_MAP(self):
        """Test the ImageBuild model's initialization.
        :data: image_build.FIELD_MAP
        """
        assert isinstance(FIELD_MAP, dict)
        for field_name, field in FIELD_MAP.items():
            assert isinstance(field_name, str)
            assert "name" in field
            for field_detail, field_detail_value in field.items():
                assert field_detail in FIELD_DETAILS


# End File: cver/tests/unit/shared/models/test_image_build.py
