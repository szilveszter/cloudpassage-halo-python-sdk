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
        search_criteria = {"state": "CATS",
                           "cve": "KB-2014-0001",
                           "kb": "CATS",
                           "missing_kb": "CATS-kb990099",
                           "platform": "CATS"}
        s = cloudpassage.Server(None)
        valid = s.validate_server_search_criteria(search_criteria)
        assert valid is False

    def test_validate_bad_list(self):
        search_criteria_list = ["ephemeral", "cats", "!!!LOSER"]
        server_object = cloudpassage.Server(None)
        state = server_object.validate_server_state(search_criteria_list)
        platform = server_object.validate_platform(search_criteria_list)
        kb = server_object.validate_kb_id(search_criteria_list)
        cve = server_object.validate_cve_id(search_criteria_list)
        assert state is False
        assert platform is False
        assert kb is False
        assert cve is False
