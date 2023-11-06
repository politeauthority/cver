"""
    Cver Test Regression
    CverClient - Collections - ImageBuildWaitings
    Source: src/cver/cver_client/collections/image_build_waitings.py

"""

from cver.client.collections.image_build_waitings import ImageBuildWaitings


class TestCverClientCollectionsImageBuildWaitings:

    def test__get(self):
        """Test that we can login to the Cver Api and that we store the token locally in a temp
        file.
        """
        ibws = ImageBuildWaitings().get()
        assert isinstance(ibws, list)

# End File: cver/tests/regression/cver_client/collections/test_image_build_waitings.py
