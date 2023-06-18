"""
    Cver Test Unit
    Api Model: Software

"""

from cver.api.models.software import Software


class TestSoftware:

    def test____init__(self):
        """Test the Software Model's initialization.
        :method: Software().__init__
        """
        software = Software()
        assert hasattr(software, "name")
        assert hasattr(software, "slug_name")
        assert hasattr(software, "url_git")
        assert hasattr(software, "url_marketing")

    def test____repr__(self):
        """Test the model's representation.
        :method: Software().__repr__
        """
        model = Software()
        assert str(model) == "<Software>"

    # def test__build_from_list(self):
    #     """Test the model's representation.
    #     :method: Software().__repr__
    #     """
    #     model = Software()
    #     raw = [1, ]
    #     model.build_from_list()
    #     assert str(model) == "<Software>"


# End File: cver/tests/api/models/test_software.py
