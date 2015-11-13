import pytest
import imp
import json
import os

module_path = os.path.abspath('../')

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)
configuration_policy = imp.load_module('configuration_policy', file,
                                       filename, data)


class TestConfigurationPolicy:
    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert configuration_policy.ConfigurationPolicy(session)
