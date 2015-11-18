import pytest
import pep8
import imp
import json
import os

module_path = os.path.abspath('../')

file_location = os.path.abspath('../cloudpassage/scan.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

file, filename, data = imp.find_module('cloudpassage', [module_path])
cp = imp.load_module('cloudpassage', file, filename, data)
halo = imp.load_module('halo', file, filename, data)
scan = imp.load_module('scan', file, filename, data)
server_group = imp.load_module('server_group', file, filename, data)
server = imp.load_module('server', file, filename, data)


class TestScan:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert scan.Scan(session)

    def test_bad_scan_type(self):
        rejected = False
        session = halo.HaloSession(key_id, secret_key)
        scanner = scan.Scan(session)
        s_group = server_group.ServerGroup(session)
        scan_type = "barfola"
        server_id = s_group.list_all()[0]["id"]
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except scan.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_bad_server_id(self):
        rejected = False
        session = halo.HaloSession(key_id, secret_key)
        scanner = scan.Scan(session)
        scan_type = "svm"
        server_id = "ABC123"
        try:
            command = scanner.initiate_scan(server_id, scan_type)
        except scan.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    """These are integration tests, and require the completion of the
    server.Server module, to get a serverID for a target to initiate a
    scan against.

    def test_sv(self):
        session = halo.HaloSession(key_id, secret_key)
        s_group = server_group.ServerGroup(session)
        server_group_list = s_group.list_all()
        scanner = scan.Scan(session)
        command = scanner.initiate_scan(server_id, "sv")
        assert command["id"]

    def test_sca(self):
        sca_aliases = ["sca", "csm"]
        session = halo.HaloSession(key_id, secret_key)
        s_group = server_group.ServerGroup(session)
        server_group_list = s_group.list_all()
        scanner = scan.Scan(session)
        for alias in sca_aliases:
            command = scanner.initiate_scan(server_id, alias)
            assert command["id"]

    def test_fim(self):
        session = halo.HaloSession(key_id, secret_key)
        s_group = server_group.ServerGroup(session)
        server_id = s_group.list_all()[0]["id"]
        scanner = scan.Scan(session)
        command = scanner.initiate_scan(server_id, 'fim')
        assert command["id"]

    def test_svm(self):
        svm_aliases = ["svm", "sva"]
        session = halo.HaloSession(key_id, secret_key)
        s_group = server_group.ServerGroup(session)
        server_id = s_group.list_all()[0]["id"]
        scanner = scan.Scan(session)
        for alias in svm_aliases:
            command = scanner.initiate_scan(server_id, alias)
            assert command["id"]

    def test_sam(self):
        session = halo.HaloSession(key_id, secret_key)
        s_group = server_group.ServerGroup(session)
        server_id = s_group.list_all()[0]["id"]
        scanner = scan.Scan(session)
        command = scanner.initiate_scan(server_id, "sam")
        assert command["id"]
    """
