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
http_helper = imp.load_module('http_helper', file, filename, data)

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
    def test_get_404(self):
        endpoint = "/v1/barf"
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.get(endpoint)
        except http_helper.http_helper.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_get_rekey(self):
        endpoint = "/v1/servers"
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        json_response = req.get(endpoint)
        assert "servers" in json_response


class TestGetPaginated:
    def test_get_paginated_404(self):
        endpoint = "/v1/barf"
        key = "barfs"
        pages = 5
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except http_helper.http_helper.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_get_paginated_rekey(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_events_99(self):
        endpoint = "/v1/events"
        key = "events"
        pages = 5
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        json_response = req.get_paginated(endpoint, key, pages)
        assert "id" in json_response[0]

    def test_get_paginated_toomany(self):
        rejected = False
        endpoint = "/v1/events"
        key = "events"
        pages = 101
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except http_helper.http_helper.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_get_paginated_badkey(self):
        rejected = False
        endpoint = "/v1/events"
        key = "badkey"
        pages = 2
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.get_paginated(endpoint, key, pages)
        except http_helper.http_helper.CloudPassageValidation:
            rejected = True
        assert rejected


class TestPost:
    def test_post_404(self):
        endpoint = "/v1/barf"
        post_data = {"whatevs": "becausenobodycares"}
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.post(endpoint, post_data)
        except http_helper.http_helper.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_post_bad_payload(self):
        rejected = False
        endpoint = "/v1/groups"
        post_data = {"whatevs": "becausenobodycares"}
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.post(endpoint, post_data)
        except http_helper.http_helper.CloudPassageValidation:
            rejected = True
        assert rejected


class TestPut:
    def test_put_bad_endpoint(self):
        endpoint = "/v1/barf"
        put_data = {"whatevs": "becausenobodycares"}
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.put(endpoint, put_data)
        except http_helper.http_helper.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_post_bad_payload(self):
        rejected = False
        endpoint = "/v1/groups"
        put_data = {"whatevs": "becausenobodycares"}
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.put(endpoint, put_data)
        except http_helper.http_helper.CloudPassageResourceExistence:
            rejected = True
        assert rejected


class TestDelete:
    def test_delete_404(self):
        endpoint = "/v1/barf"
        pathfailed = False
        session = halo.HaloSession(key_id, secret_key)
        session.authenticate_client()
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.delete(endpoint)
        except http_helper.http_helper.CloudPassageResourceExistence:
            pathfailed = True
        assert pathfailed

    def test_delete_rekey(self):
        delfailed = False
        endpoint = "/v1/servers/123455432"
        session = halo.HaloSession(key_id, secret_key)
        session.auth_token = "abc123"
        req = http_helper.HttpHelper(session)
        try:
            json_response = req.delete(endpoint)
        except http_helper.http_helper.CloudPassageResourceExistence:
            delfailed = True
        assert delfailed
