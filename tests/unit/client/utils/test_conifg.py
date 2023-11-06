"""
    Cver Client Unit Test
    Config
    Source: cver/src/cver/cver_client/utils/config.py

"""
from cver.client.utils.config import Config


class TestClientUtilsConfig:

    def test____init__(self):
        """
        :method: Config().__init__()
        """
        config = Config()
        assert hasattr(config, "config_file")

# End File: cver/tests/unit/cver_client/utils/test__config.py
