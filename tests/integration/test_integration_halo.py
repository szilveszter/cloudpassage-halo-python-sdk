import cloudpassage
import datetime
import hashlib
import json
import os
import pytest


config_file_name = "portal.yaml.local"
tests_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
config_file = os.path.join(tests_dir, "configs/", config_file_name)

session_info = cloudpassage.ApiKeyManager(config_file=config_file)
key_id = session_info.key_id
secret_key = session_info.secret_key
api_hostname = session_info.api_hostname
bad_key = "abad53c"
proxy_host = '190.109.164.81'
proxy_port = '1080'

# This will make cleaning up easier...
content_prefix = '_SDK_test-'

content_name = str(content_prefix +
                   str(hashlib.md5(str(datetime.datetime.now())).hexdigest()))


class TestIntegrationHaloSession:
    def create_halo_session_object(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return session

    def test_halosession_authentication(self):
        session = self.create_halo_session_object()
        session.authenticate_client()
        assert ((session.auth_token is not None) and
                (session.auth_scope is not None))

    def test_halosession_throws_auth_exception(self):
        session = cloudpassage.HaloSession(bad_key, secret_key)
        authfailed = False
        try:
            session.authenticate_client()
        except cloudpassage.CloudPassageAuthentication:
            authfailed = True
        assert authfailed
