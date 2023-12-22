"""
    Cver Client
    Utils
    Config
        Determines the configuration of the Cver Client.

"""
import os
import logging

import yaml

from cver.shared.utils import misc


class Config:

    def __init__(self):
        """Initialize configuration
        :unit-test: TestClientUtilsConfig::test__validate_config
        """
        self.config_file = "/Users/alix/.cver/config"
        self.use_local_config = False
        self.local_config_name = None
        self.local_config = {}
        self.config = {
            "api_url": None,
            "api_key": None,
            "client_id": None,
            "api_host_name": None
        }

    def get(
            self,
            client_id: str = None,
            api_key: str = None,
            api_url: str = None,
            config: str = None
    ) -> dict:
        """Get the configuration to use.
        The current priority:
            - manual args sent to the cleint
            - a configuration yaml file
            - environment vars
        """
        if config:
            self.local_config_name = config
        if self.get_manual_arg_config(client_id, api_key, api_url):
            pass
        elif self.read_local_config():
            pass
        elif self.get_env_config():
            pass
        self.validate_config()
        return self.config

    def get_manual_arg_config(
            self,
            client_id: str = None,
            api_key: str = None,
            api_url: str = None
    ) -> dict:
        """Get the manual args supplied.
        :unit-test: TestClientUtilsConfig::test__get_manual_arg_config
        """
        if not client_id or not api_key or not api_url:
            return {}
        self.config["api_url"] = api_url
        self.config["api_key"] = api_key
        self.config["client_id"] = client_id
        return self.config

    def read_local_config(self) -> bool:
        """Read the local configiuration yaml file."""
        self.check_use_local_config()
        if not self.use_local_config:
            return self.use_local_config
        self.config = self.get_local_server_config()
        return self.use_local_config

    def check_use_local_config(self):
        """Check if we use the the Cver config file. We'll check if the dir and file exists,
        loading the config and checking if the file wants us to use the config.
        """
        if not os.path.exists(self.config_file):
            # logging.debug("Config path does not exist: %s" % self.config_file)
            return False
        with open(self.config_file, "r") as file:
            self.local_config = yaml.safe_load(file)

        self.use_local_config = misc.get_dict_path(self.local_config, "cver-api.use-config-file")
        return self.use_local_config

    def get_local_server_config(self) -> dict:
        """Get the server configuration from the yaml config file."""
        if self.local_config_name:
            server_config_name = self.local_config_name
        else:
            server_config_name = misc.get_dict_path(self.local_config, "cver-api.default-server")
        if not server_config_name:
            self.use_config = False
            return False
        server_config = self.local_config["cver-api"]["servers"][server_config_name]
        self.config["api_url"] = server_config["api-url"]
        self.config["api_key"] = server_config["api-key"]
        self.config["client_id"] = server_config["client-id"]
        if "api-host" in server_config:
            self.config["api_host_name"] = server_config["api-host"]
        return self.config

    def get_env_config(self) -> dict:
        """Get the Client configuration from environment vars."""
        self.config["api_url"] = os.environ.get("CVER_API_URL")
        self.config["api_key"] = os.environ.get("CVER_API_KEY")
        self.config["client_id"] = os.environ.get("CVER_CLIENT_ID")
        return self.config

    def validate_config(self) -> bool:
        """Validate configuration.
        :unit-test: TestClientUtilsConfig::test__validate_config
        """
        errors = []
        if not self.config["api_url"] or not isinstance(self.config["api_url"], str):
            errors.append("invalid api url")
        if not self.config["api_key"] or not isinstance(self.config["api_key"], str):
            errors.append("invalid api key")
        if not self.config["client_id"] or not isinstance(self.config["client_id"], str):
            errors.append("invalid client_id")
        if errors:
            logging.critical("Cver Client has the following config issues: %s" % ", ".join(errors))
            return False
        return True


# End File: cver/src/cver/cver_client/config.py
