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
api_port = session_info.api_port


class TestIntegrationAlertProfiles:
    def create_alert_profile_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key,
                                           api_host=api_hostname,
                                           api_port=api_port)
        return cloudpassage.AlertProfile(session)

    def test_instantiation(self):
        assert self.create_alert_profile_obj()

    def test_list_all(self):
        """This gets a list of alert profiles from the Halo API.  It will
        fail if there are no alert profiles configured for your account."""
        profile = self.create_alert_profile_obj()
        profile_list = profile.list_all()
        assert "id" in profile_list[0]

    def test_create(self):
        rejected = False
        profile = self.create_alert_profile_obj()
        try:
            profile.create("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_update(self):
        rejected = False
        profile = self.create_alert_profile_obj()
        try:
            profile.update("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_describe(self):
        rejected = False
        profile = self.create_alert_profile_obj()
        try:
            profile.describe("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_delete(self):
        rejected = False
        profile = self.create_alert_profile_obj()
        try:
            profile.delete("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected
