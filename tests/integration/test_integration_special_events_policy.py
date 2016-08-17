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


class TestIntegrationSpecialEventsPolicy:
    def create_special_events_policy_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return cloudpassage.SpecialEventsPolicy(session)

    def test_instantiation(self):
        assert self.create_special_events_policy_obj()

    def test_list_all(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        se_policy = cloudpassage.SpecialEventsPolicy(session)
        se_policy_list = se_policy.list_all()
        assert "id" in se_policy_list[0]

    def test_describe(self):
        """This test gets the details of a special events policy in
        your Halo account.  If you don't have any special events policies
        configured, it will fail.
        """
        request = self.create_special_events_policy_obj()
        policy_list = request.list_all()
        target_policy_id = policy_list[0]["id"]
        target_policy_body = request.describe(target_policy_id)
        assert "id" in target_policy_body

    def test_create(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        policy = cloudpassage.SpecialEventsPolicy(session)
        try:
            policy.create("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_update(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        policy = cloudpassage.SpecialEventsPolicy(session)
        try:
            policy.update("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_delete(self):
        rejected = False
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        policy = cloudpassage.SpecialEventsPolicy(session)
        try:
            policy.delete("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected
