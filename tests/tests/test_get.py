import os
import imp
import pytest
import json
import datetime
import hashlib



module_path = os.path.abspath('../')
policy_path = os.path.abspath('./policies/')

file, filename, data = imp.find_module('cloudpassage', [module_path])
halo = imp.load_module('halo', file, filename, data)

# Temporary...
get = imp.load_module('get', file, filename, data)

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
ro_key_id = os.environ.get('RO_HALO_KEY_ID')
ro_secret_key = os.environ.get('RO_HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'

# This will make cleaning up easier...
content_prefix = '_SDK_test-'

content_name = content_prefix + str(hashlib.md5(str(datetime.datetime.now())).hexdigest())

class TestGet:
    def test_get_404(self):
        url = "/v1/barf"
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = get.Get(session)
        try:
            json_response = req.get(url)
        except get.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_get_rekey(self):
        url = "/v1/servers"
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = get.Get(session)
        json_response = req.get(url)
        assert "servers" in json_response

