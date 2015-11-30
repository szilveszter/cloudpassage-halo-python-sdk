import os
import pep8
import pytest
import json
import datetime
import hashlib
import cloudpassage


policy_path = os.path.abspath('./policies/')

file_location = os.path.abspath('../cloudpassage/http_helper.py')
this_file = os.path.abspath(__file__)

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
content_name = str(content_prefix +
                   str(hashlib.md5(str(datetime.datetime.now())).hexdigest()))


class TestGet:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_get_404(self):
        endpoint = "/v1/barf"
        pathfailed = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.get(endpoint)
        except cloudpassage.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_get_rekey(self):
        endpoint = "/v1/servers"
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get(endpoint)
        assert "servers" in json_response


class TestGetPaginated:
    def test_get_paginated_404(self):
        endpoint = "/v1/barf"
        key = "barfs"
        pages = 5
        pathfailed = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except cloudpassage.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_get_paginated_rekey(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_events_99(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_toomany(self):
        rejected = False
        endpoint = "/v1/events"
        key = "events"
        pages = 101
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_get_paginated_badkey(self):
        rejected = False
        endpoint = "/v1/events"
        key = "badkey"
        pages = 2
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected


class TestPost:
    def test_post_404(self):
        endpoint = "/v1/barf"
        post_data = {"whatevs": "becausenobodycares"}
        pathfailed = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.post(endpoint, post_data)
        except cloudpassage.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_post_bad_payload(self):
        rejected = False
        endpoint = "/v1/groups"
        post_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.post(endpoint, post_data)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected


class TestPut:
    def test_put_bad_endpoint(self):
        endpoint = "/v1/barf"
        put_data = {"whatevs": "becausenobodycares"}
        pathfailed = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.put(endpoint, put_data)
        except cloudpassage.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_post_bad_payload(self):
        rejected = False
        endpoint = "/v1/groups"
        put_data = {"whatevs": "becausenobodycares"}
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.put(endpoint, put_data)
        except cloudpassage.CloudPassageResourceExistence:
            rejected = True
        assert rejected


class TestDelete:
    def test_delete_404(self):
        endpoint = "/v1/barf"
        pathfailed = False
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.delete(endpoint)
        except cloudpassage.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_delete_rekey(self):
        delfailed = False
        endpoint = "/v1/servers/123455432"
        session = cloudpassage.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = cloudpassage.HttpHelper(session)
        try:
            json_response = req.delete(endpoint)
        except cloudpassage.CloudPassageResourceExistence:
            delfailed = True
        assert delfailed
