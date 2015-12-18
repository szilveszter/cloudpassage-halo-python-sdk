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


# This will make cleaning up easier...
content_prefix = '_SDK_test-'
content_name = str(content_prefix +
                   str(hashlib.md5(str(datetime.datetime.now())).hexdigest()))


class TestGet:
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
