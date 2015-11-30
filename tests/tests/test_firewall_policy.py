import cloudpassage
import pytest
import pep8
import imp
import json
import os

policy_file = os.path.abspath('./policies/firewall.json')

file_location = os.path.abspath('../cloudpassage/firewall_policy.py')
this_file = os.path.abspath(__file__)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestFirewallPolicy:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_instantiation(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        assert cloudpassage.FirewallPolicy(session)

    def create_firewall_policy_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        firewall_policy_object = cloudpassage.FirewallPolicy(session)
        return firewall_policy_object

    def test_firewall_policy_list_all(self):
        firewall_policy = self.create_firewall_policy_object()
        firewall_policy_list = firewall_policy.list_all()
        assert "id" in firewall_policy_list[0]

    def test_firewall_policy_describe(self):
        firewall_policy = self.create_firewall_policy_object()
        firewall_policy_list = firewall_policy.list_all()
        target_firewall_policy_id = firewall_policy_list[0]["id"]
        target_policy = firewall_policy.describe(target_firewall_policy_id)
        assert "id" in target_policy

    def test_firewall_policy_create_update_delete(self):
        firewall_policy = self.create_firewall_policy_object()
        with open(policy_file, 'r') as p_file:
            firewall_policy_body = p_file.read().replace('\n', '')
        new_policy_id = firewall_policy.create(firewall_policy_body)
        new_policy_name = "New Policy Name"
        firewall_policy.update(new_policy_id, name=new_policy_name)
        delete_success = firewall_policy.delete(new_policy_id)
