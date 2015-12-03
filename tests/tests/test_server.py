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


class TestServer:
    def build_server_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        server_object = cloudpassage.Server(session)
        return(server_object)

    def build_server_group_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        server_group_object = cloudpassage.ServerGroup(session)
        return(server_group_object)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.Server(session)

    def test_get_server_details(self):
        s = self.build_server_object()
        s_group = self.build_server_group_object()
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
        request = self.build_server_object()
        bad_server_id = "123456789"
        try:
            request.describe(bad_server_id)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_retire_server_404(self):
        rejected = False
        request = self.build_server_object()
        server_id = "12345"
        try:
            result = request.retire(server_id)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_command_details_404(self):
        rejected = False
        request = self.build_server_object()
        server_id = "12345"
        command_id = "56789"
        try:
            result = request.command_details(server_id, command_id)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected

    def test_server_list(self):
        s = self.build_server_object()
        result = s.list_all()
        assert "id" in result[0]

    def test_server_list_inactive_test1(self):
        states = ["deactivated", "active"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert "id" in result[0]

    def test_server_list_inactive_test2(self):
        states = ["deactivated"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert "id" in result[0]

    def test_server_list_inactive_test3(self):
        states = ["missing", "deactivated"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert "id" in result[0]

    def test_server_list_inactive(self):
        states = ["deactivated", "missing"]
        s = self.build_server_object()
        result = s.list_all(state=states)
        assert "id" in result[0]

    def test_validate_server_search_criteria(self):
        search_criteria = {"state": ["deactivated", "missing"],
                           "cve": ["CVE-2014-0001"],
                           "kb": "kb22421121",
                           "missing_kb": "kb990099"}
        s = self.build_server_object()
        success = s.validate_server_search_criteria(search_criteria)
        assert success

    def test_validate_server_search_criteria_fail(self):
        search_criteria = {"state": ["deactivated", "missing"],
                           "cve": ["KB-2014-0001"],
                           "kb": "kb22421121",
                           "missing_kb": "kb990099"}
        s = self.build_server_object()
        valid = s.validate_server_search_criteria(search_criteria)
        assert valid is False
