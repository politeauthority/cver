"""
    Cver - Test - Regression
    Cli
    Cver

"""
from cver.cli import Cver

from cver_test_tools.fixtures.arg_parse import ArgParse


class TestCliCver:

    def test____init__(self):
        """
        """
        argz = ArgParse()
        argz.verb = "get"
        argz.noun = "info"
        cli = Cver(argz)
        assert isinstance(cli.args, ArgParse)

    def test__get_info(self):
        """Test get info. """
        argz = ArgParse()
        # argz.verb = "get"
        # argz.noun = "info"
        cli = Cver(argz)
        assert cli.get_info()

# End File: cver/tests/regression/clii/test_cli___init__py
