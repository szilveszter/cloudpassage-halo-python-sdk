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


class TestIntegrationLocalUserGroup:
    def build_local_user_group_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port,
                                           integration_string="SDK-Smoke")
        local_user_group_obj = cloudpassage.LocalUserGroup(session)
        return(local_user_group_obj)

    def test_local_group_list(self):
        local_group = self.build_local_user_group_obj()
        result = local_group.list_all()
        assert "members" in result[0]

    def test_get_local_group_by_server_id(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_g = self.build_local_user_group_obj()
        result = local_g.list_all()
        assert result is not None

        target_server_id = result[0]["server_id"]
        local_g_srvs = local_g.list_all(server_id=target_server_id)
        assert local_g_srvs is not None

        for local_g_srv in local_g_srvs:
            assert local_g_srv["server_id"] == target_server_id

    def test_get_local_group_by_linux(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_g = self.build_local_user_group_obj()
        results = local_g.list_all(os_type="linux")
        assert results is not None

        for result in results:
            assert result["os_type"] == "linux"

    def test_get_local_group_by_group_id(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_g = self.build_local_user_group_obj()
        result = local_g.list_all()
        assert result is not None

        target_group_id = result[0]["group_id"]
        local_g_grps = local_g.list_all(group_id=target_group_id)
        assert local_g_grps is not None

        for local_g_grp in local_g_grps:
            assert local_g_grp["group_id"] == target_group_id

    def test_get_local_group_detail(self):
        """This test requires at least one active server in your Halo
        account.  If you have no active server, this test will fail.
        """
        local_g = self.build_local_user_group_obj()
        result = local_g.list_all()
        assert result is not None

        target_server_id = result[0]["server_id"]
        target_gid = result[0]["gid"]

        described_g = local_g.describe(target_server_id,
                                       target_gid)
        assert described_g[0]["gid"] == target_gid
        assert described_g[0]["server_id"] == target_server_id
