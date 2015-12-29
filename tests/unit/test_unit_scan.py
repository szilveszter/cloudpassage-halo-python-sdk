import cloudpassage
import datetime
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


class TestUnitScan:
    def test_instantiation(self):
        assert cloudpassage.Scan(None)

    def test_scan_type_valid(self):
        valid_types = ["svm", "sva", "csm", "sca", "fim", "sam", "sv"]
        invalid_types = ["death_stare", "lids"]
        session = cloudpassage.HaloSession(key_id, secret_key)
        scanner = cloudpassage.Scan(session)
        for v in valid_types:
            assert scanner.scan_type_supported(v)
        for i in invalid_types:
            assert not scanner.scan_type_supported(i)


class TestUnitCveException:
    def test_instantiation(self):
        assert cloudpassage.CveException(None)
