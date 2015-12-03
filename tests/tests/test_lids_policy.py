import cloudpassage
import json
import os
import pytest

policy_file = os.path.abspath('./policies/' +
                              'core-system-centos-v1-1.lids.json')

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestLidsPolicy:
    def build_lids_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.LidsPolicy(session)
        return(return_obj)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.LidsPolicy(session)

    def test_list_all(self):
        request = self.build_lids_policy_object()
        response = request.list_all()
        assert "id" in response[0]

    def test_get_details(self):
        request = self.build_lids_policy_object()
        policy_list = request.list_all()
        target_policy_id = policy_list[0]["id"]
        target_policy_body = request.describe(target_policy_id)
        assert "id" in target_policy_body

    def test_lids_policy_create_delete(self):
        deleted = False
        policy_retrieved = {"lids_policy": None}
        request = self.build_lids_policy_object()
        newname = "Functional Test Name Change"
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        policy_id = request.create(policy_body)
        request.delete(policy_id)
        try:
            request.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted

    def test_lids_policy_create_update_delete(self):
        deleted = False
        policy_retrieved = {"lids_policy": None}
        request = self.build_lids_policy_object()
        newname = "Functional Test Name Change"
        with open(policy_file, 'r') as policy_file_object:
            policy_body = policy_file_object.read()
        policy_id = request.create(policy_body)
        policy_update = json.loads(policy_body)
        policy_update["lids_policy"]["name"] = newname
        policy_update["lids_policy"]["id"] = policy_id
        request.update(policy_update)
        request.delete(policy_id)
        try:
            request.describe(policy_id)
        except cloudpassage.CloudPassageResourceExistence:
            deleted = True
        assert deleted
