"""
    Cver Test Unit
    Api Model: Scanner
    Source: src/cver/api/model/scanner.py

"""

from cver.api.models.scanner import Scanner


class TestScanner:

    def test____init__(self):
        """Test the Scanner Model's initialization.
        :method: Scanner().__init__
        """
        image = Scanner()
        assert hasattr(image, "name")

    def test____repr__(self):
        """Test the model's representation.
        :method: Scanner().__repr__
        """
        model = Scanner()
        assert str(model) == "<Scanner>"


# End File: cver/tests/api/models/test_scanner.py
