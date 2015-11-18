import pytest
import pep8
import imp
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/server.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)
server = imp.load_module('server', file, filename, data)
server_group = imp.load_module('server_group', file, filename, data)
cp = imp.load_module('cloudpassage', file, filename, data)


class TestServer:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert server.Server(session)

    def test_get_server_details(self):
        session = halo.HaloSession(key_id, secret_key)
        s = server.Server(session)
        s_group = server_group.ServerGroup(session)
        server_group_list = s_group.list_all()
        target_group = None
        for group in server_group_list:
            if group["server_counts"]["active"] != 0:
                target_group = group["id"]
                break
        assert target_group is not None
        target_server_id = s_group.list_members(target_group)[0]["id"]
        assert "id" in s.describe(target_server_id)

    def test_get_server_details_404(self):
        rejected = False
        session = halo.HaloSession(key_id, secret_key)
        request = server.Server(session)
        bad_server_id = "123456789"
        try:
            request.describe(bad_server_id)
        except request.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_retire_server_404(self):
        rejected = False
        session = halo.HaloSession(key_id, secret_key)
        request = server.Server(session)
        server_id = "12345"
        try:
            result = request.retire(server_id)
        except server.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_command_details_404(self):
        rejected = False
        session = halo.HaloSession(key_id, secret_key)
        request = server.Server(session)
        server_id = "12345"
        command_id = "56789"
        try:
            result = request.command_details(server_id, command_id)
        except server.CloudPassageResourceExistence:
            rejected = True
        assert rejected
