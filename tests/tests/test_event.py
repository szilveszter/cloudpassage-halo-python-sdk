import cloudpassage
import datetime
import json
import os
import pytest

key_id = os.environ.get('HALO_KEY_ID')
secret_key = os.environ.get('HALO_SECRET_KEY')
bad_key = "abad53c"
api_hostname = os.environ.get('HALO_API_HOSTNAME')
proxy_host = '190.109.164.81'
proxy_port = '1080'


class TestEvent:
    def create_event_obj(self):
        session = cloudpassage.HaloSession(key_id, secret_key)
        return cloudpassage.Event(session)

    def test_instantiation(self):
        assert self.create_event_obj()

    def test_list_five_pages(self):
        event = self.create_event_obj()
        event_list = event.list_all(5)
        assert "id" in event_list[0]

    def test_too_big(self):
        rejected = False
        event = self.create_event_obj()
        try:
            event.list_all(101)
        except cloudpassage.CloudPassageValidation:
            rejected = True
        assert rejected

    def test_windows(self):
        rejected = False
        event = self.create_event_obj()
        event_list = event.list_all(2, server_platform="windows")
        assert "id" in event_list[0]

    def test_one_day_ago_until_now(self):
        event = self.create_event_obj()
        until = cloudpassage.utility.time_string_now()
        since = datetime.datetime.utcnow() - datetime.timedelta(days=1)
        event_list = event.list_all(10, since=since, until=until)
        assert "id" in event_list[0]
