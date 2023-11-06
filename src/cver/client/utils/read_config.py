"""
    Cver Client
    Utils
    Read Config

"""
import os
import logging

import yaml

from cver.shared.utils import misc


class ReadConfig:

    def __init__(self):
        self.config_file = "/Users/alix/.cver/config"
        self.use_config = False
        self.config = None

    def read(self):
        self.check_use_config()
        if not self.use_config:
            return self.use_config
        self.get_server_config()
        return self.use_config

    def check_use_config(self):
        """Check if we use the the Cver config file. We'll check if the dir and file exists,
        loading the config and checking if the file wants us to use the config.
        """
        if not os.path.exists(self.config_file):
            logging.debug("Config path does not exist: %s" % self.config_file)
            return False
        with open(self.config_file, "r") as file:
            self.config = yaml.safe_load(file)

        self.use_config = misc.get_dict_path(self.config, "cver-api.use-config-file")
        return self.use_config

    def get_server_config(self):
        server_config_name = misc.get_dict_path(self.config, "cver-api.default-server")
        if not server_config_name:
            self.use_config = False
            return False
        server_config = self.config["cver-api"]["servers"][server_config_name]
        return server_config

# End File: cver/src/cver/cver_client/read_config.py
