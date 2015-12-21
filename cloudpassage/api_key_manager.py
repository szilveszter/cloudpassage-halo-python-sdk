"""CloudPassage Api Key Manager"""

import os
import yaml
import cloudpassage.sanity as sanity


class ApiKeyManager(object):
    """Retrieves API keys from file or environment.

    If instantiated with no arguments, it will return credentials from
    environment variables.  If there are no credentials set in environment
    variables, it will look to /etc/cloudpassage.yaml.

    If there is no api_hostname specified in the selected configuration
    source, it defaults to api.cloudpassage.com.


    Environment variables::
        HALO_API_KEY
        HALO_API_SECRET_KEY
        HALO_API_HOSTNAME


    Yaml file structure::
        defaults:
            key_id:
            secret_key:
            api_hostname:

    Keyword args:
        config_file (str): full path to yaml config file

    Attributes:
        api_hostname: Hostname of api endpoint. \
        Defaults to api.cloudpassage.com
        key_id: API key ID
        secret_key: API key secret

    """

    def __init__(self, **kwargs):
        self.api_hostname = "api.cloudpassage.com"
        self.key_id = None
        self.secret_key = None
        self.config_file = None

        if "config_file" in kwargs:
            self.config_file = kwargs["config_file"]
        else:
            self.config_file = "/etc/cloudpassage.yaml"

        env_variables = {"key_id": os.getenv("HALO_API_KEY"),
                         "secret_key": os.getenv("HALO_API_SECRET_KEY"),
                         "api_hostname": os.getenv("HALO_API_HOSTNAME")}
        if self.env_vars_are_set(env_variables):
            self.key_id = env_variables["key_id"]
            self.secret_key = env_variables["secret_key"]
            if sanity.validate_api_hostname(env_variables["api_hostname"]):
                self.api_hostname = env_variables["api_hostname"]
            return
        else:
            with open(self.config_file) as y_config_file:
                session_yaml = yaml.load(y_config_file)["defaults"]
            self.key_id = session_yaml["key_id"]
            self.secret_key = session_yaml["secret_key"]
            if sanity.validate_api_hostname(session_yaml["api_hostname"]):
                self.api_hostname = session_yaml["api_hostname"]
            return

    def env_vars_are_set(self, env_vars):  # pylint: disable=no-self-use
        """Determine if environment vars are correctly set"""
        vars_are_set = True
        if env_vars["key_id"] is None or env_vars["secret_key"] is None:
            vars_are_set = False
        return vars_are_set
