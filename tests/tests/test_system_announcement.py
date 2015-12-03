import cloudpassage
import json
import os
import pytest

module_path = os.path.abspath('../')

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestSystemAnnouncement:
    def create_announcement(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return(cloudpassage.SystemAnnouncement(session))

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.SystemAnnouncement(session)

    def test_list_all(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        announcement = cloudpassage.SystemAnnouncement(session)
        announcement_list = announcement.list_all()
        assert "announcement" in announcement_list[0]
