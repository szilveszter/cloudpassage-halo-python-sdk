import cloudpassage
import pytest
import pep8
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/system_announcement.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestSystemAnnouncement:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.SystemAnnouncement(session)

    def test_list_all(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        announcement = cloudpassage.SystemAnnouncement(session)
        announcement_list = announcement.list_all()
        assert "announcement" in announcement_list[0]
