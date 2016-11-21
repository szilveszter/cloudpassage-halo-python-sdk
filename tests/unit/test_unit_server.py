import cloudpassage
import os


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

    def test_validate_bad_list(self):
        search_criteria_list = ["ephemeral", "cats", "!!!LOSER"]
        server_object = cloudpassage.Server(None)
        platform = server_object.validate_platform(search_criteria_list)
        kb = server_object.validate_kb_id(search_criteria_list)
        cve = server_object.validate_cve_id(search_criteria_list)
        assert platform is False
        assert kb is False
        assert cve is False
