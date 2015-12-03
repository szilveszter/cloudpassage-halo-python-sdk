import cloudpassage
import json
import os
import pytest

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestAlertProfiles:
    def create_alert_profile_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return cloudpassage.AlertProfile(session)

    def test_instantiation(self):
        assert self.create_alert_profile_obj()

    def test_list_all(self):
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
