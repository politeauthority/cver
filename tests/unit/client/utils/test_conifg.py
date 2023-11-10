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
        assert hasattr(config, "use_local_config")
        assert hasattr(config, "local_config")
        assert hasattr(config, "config")

    def test__get_manual_arg_config(self):
        """
        :method: Config().get_manual_arg_config()
        """
        config = Config()
        generated = config.get_manual_arg_config(
            client_id="client id",
            api_key="api key",
            api_url="api url")
        assert isinstance(generated, dict)
        assert "client id" == generated["client_id"]
        assert "api key" == generated["api_key"]
        assert "api url" == generated["api_url"]

    def test__validate_config(self):
        """
        :method: Config().validate_config()
        """
        config = Config()
        config.config["api_url"] = None
        assert not config.validate_config()
        config.config["api_url"] = "Url"
        config.config["api_key"] = "Key"
        config.config["client_id"] = "Client ID"
        assert config.validate_config()

# End File: cver/tests/unit/cver_client/utils/test__config.py
