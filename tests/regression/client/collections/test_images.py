"""
    Cver Test Regression
    CverClient - Collections - Images
    Source: src/cver/client/collections/images.py

"""

from cver.client.collections.images import Images
from cver.client.models.image import Image


class TestCverClientCollectionsImageBuildWaitings:

    def test__get(self):
        """Test that we can login to the Cver Api and that we store the token locally in a temp
        file.
        """
        images_col = Images()
        images = images_col.get()
        for image in images:
            assert isinstance(image, Image)

# End File: cver/tests/regression/client/collections/test_images.py
