import pytest
import pep8
import imp
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/server_group.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
ro_key_id = os.environ.get('RO_HALO_KEY_ID')
ro_secret_key = os.environ.get('RO_HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)
server_group = imp.load_module('ServerGroup', file, filename, data)
sanity = imp.load_module('sanity', file, filename, data)


class TestServerGroup:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert server_group.ServerGroup(session)

    def test_list_all(self):
        session = halo.HaloSession(key_id, secret_key)
        s_grp = server_group.ServerGroup(session)
        groups = s_grp.list_all()
        assert "id" in groups[0]

    def test_describe(self):
        session = halo.HaloSession(key_id, secret_key)
        s_grp = server_group.ServerGroup(session)
        groups = s_grp.list_all()
        target_group_id = groups[0]["id"]
        target_group_object = s_grp.describe(target_group_id)
        assert "id" in target_group_object

    def test_list_members(self):
        # Rolls through all server groups, confirms active server IDs
        confirmed = False
        session = halo.HaloSession(key_id, secret_key)
        s_grp = server_group.ServerGroup(session)
        groups = s_grp.list_all()
        num_members = 0
        for g in groups:
            target_group_id = g["id"]
            num_members = g["server_counts"]["active"]
            if num_members > 0:
                members = s_grp.list_members(target_group_id)
                assert members[0]["id"]
                confirmed = True
        # Confirm that we actually have a populated server group
        assert confirmed
