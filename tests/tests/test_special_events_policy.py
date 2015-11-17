import pytest
import imp
import pep8
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/special_events_policy.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)
special_events_policy = imp.load_module('special_events_policy', file,
                                        filename, data)


class TestSpecialEventsPolicy:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert special_events_policy.SpecialEventsPolicy(session)

    def test_list_all(self):
        session = halo.HaloSession(key_id, secret_key)
        se_policy = special_events_policy.SpecialEventsPolicy(session)
        se_policy_list = se_policy.list_all()
        assert "id" in se_policy_list[0]
