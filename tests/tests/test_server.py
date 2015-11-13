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
server = imp.load_module('server', file,
                         filename, data)


class TestServer:
    def test_instantiation(self):
        session = halo.HaloSession(key_id, secret_key)
        assert server.Server(session)
