import cloudpassage
import json
import os
import pytest

config_file_name = "portal.yaml.local"
policy_file_name = "cis-benchmark-for-centos-7-v1.policy.json"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestUnitConfigurationPolicy:
    def test_instantiation(self):
        session = cloudpassage.HaloSession(None, None)
        assert cloudpassage.ConfigurationPolicy(session)
