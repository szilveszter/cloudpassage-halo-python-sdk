import cloudpassage
import os

policy_file_name = "firewall.json"
config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)
policy_file = os.path.join(tests_dir, 'policies/', policy_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname

with open(policy_file, 'r') as p_file:
    firewall_policy_body = p_file.read().replace('\n', '')


class TestUnitFirewallPolicy:
    def test_instantiation(self):
        assert cloudpassage.FirewallPolicy(None)


class TestUnitFirewallRule:
    def test_instantiation(self):
        assert cloudpassage.FirewallRule(None)


class TestUnitFirewallZone:
    def test_instantiation(self):
        assert cloudpassage.FirewallZone(None)


class TestUnitFirewallService:
    def test_instantiation(self):
        assert cloudpassage.FirewallService(None)


class TestUnitFirewallInterface:
    def test_instantiation(self):
        assert cloudpassage.FirewallInterface(None)
