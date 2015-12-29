import cloudpassage
import datetime
import json
import os


policy_file_name = "core-system-files-centos-v1.fim.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestUnitFimPolicy:
    def test_instantiation(self):
        assert cloudpassage.FimPolicy(None)


class TestUnitFimBaseline:
    def test_instantiation(self):
        assert cloudpassage.FimBaseline(None)
