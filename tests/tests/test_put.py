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
put = imp.load_module('put', file, filename, data)

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

class TestPut:
    def test_put_bad_url(self):
        url = "/v1/barf"
        put_data = {"whatevs": "becausenobodycares"}
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = put.Put(session)
        try:
            json_response = req.put(url, put_data)
        except put.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_post_bad_payload(self):
        rejected = False
        url = "/v1/groups"
        put_data = {"whatevs": "becausenobodycares"}
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = put.Put(session)
        try:
            json_response = req.put(url, put_data)
        except put.CloudPassageResourceExistence:
            rejected = True
        assert rejected

