"""
    Cver - Test - Regression - Api
    Sets up required entities for teasting.
"""
import pytest

from cver.cver_client.models.image import Image


class TestSetupTests:

    @pytest.mark.first
    def test__setup_images(request):
        """Create the test Images that will be used in our tests."""
        global images
        image = Image()
        image.name = "test-image-1"
        image.save()
        # prepare something ahead of all tests
        # request.addfinalizer(finalizer_function)


# End File: cver/tests/regression/api/test_ctrl_index.py
