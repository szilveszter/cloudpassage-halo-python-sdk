import cloudpassage
import os


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
api_port = session_info.api_port


class TestIntegrationLocalUserAccount:
    def build_local_user_account_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        local_user_account_obj = cloudpassage.LocalUserAccount(session)
        return(local_user_account_obj)

    def test_local_user_list(self):
        local_account = self.build_local_user_account_obj()
        result = local_account.list_all()
        assert "username" in result[0]

    def test_get_local_account_by_server_id(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_a = self.build_local_user_account_obj()
        result = local_a.list_all()
        assert result is not None

        target_server_id = result[0]["server_id"]
        local_a_srvs = local_a.list_all(server_id=target_server_id)
        assert local_a_srvs is not None

        for local_a_srv in local_a_srvs:
            assert local_a_srv["server_id"] == target_server_id

    def test_get_local_account_by_linux(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_a = self.build_local_user_account_obj()
        results = local_a.list_all(os_type="linux")
        assert results is not None

        for result in results:
            assert result["os_type"] == "linux"

    def test_get_local_account_by_group_id(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_a = self.build_local_user_account_obj()
        result = local_a.list_all()
        assert result is not None

        target_group_id = result[0]["group_id"]
        local_a_grps = local_a.list_all(group_id=target_group_id)
        assert local_a_grps is not None

        for local_a_grp in local_a_grps:
            assert local_a_grp["group_id"] == target_group_id
