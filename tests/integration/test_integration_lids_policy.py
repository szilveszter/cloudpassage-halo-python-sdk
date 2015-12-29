import cloudpassage
import json
import os
import pytest

policy_file_name = "core-system-centos-v1-1.lids.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname


class TestIntgrationLidsPolicy:
    def build_lids_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return_obj = cloudpassage.LidsPolicy(session)
        return(return_obj)

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.LidsPolicy(session)

    def test_list_all(self):
        """This test gets a list of LIDS policies from the Halo API.
        If you have no configuration policies in your account, it will fail
        """
        request = self.build_lids_policy_object()
        response = request.list_all()
        assert "id" in response[0]

    def test_get_details(self):
        """This test requires at least one LIDS policy in your account.  If
        you don't have one, this test will fail."""
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
