import cloudpassage
import json
import os
import pytest


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestUnitServer:
    def test_instantiation(self):
        assert cloudpassage.Server(None)

    def test_validate_server_search_criteria(self):
        search_criteria = {"state": ["deactivated", "missing"],
                           "cve": ["CVE-2014-0001"],
                           "kb": "kb22421121",
                           "missing_kb": "kb990099"}
        s = cloudpassage.Server(None)
        success = s.validate_server_search_criteria(search_criteria)
        assert success

    def test_validate_server_search_criteria_fail(self):
        search_criteria = {"state": ["deactivated", "missing"],
                           "cve": ["KB-2014-0001"],
                           "kb": "kb22421121",
                           "missing_kb": "kb990099"}
        s = cloudpassage.Server(None)
        valid = s.validate_server_search_criteria(search_criteria)
        assert valid is False
