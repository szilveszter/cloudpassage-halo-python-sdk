import cloudpassage
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


class TestUnitSpecialEventsPolicy:
    def test_instantiation(self):
        assert cloudpassage.SpecialEventsPolicy(None)

    def test_create(self):
        rejected = False
        policy = cloudpassage.SpecialEventsPolicy(None)
        try:
            policy.create("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_update(self):
        rejected = False
        policy = cloudpassage.SpecialEventsPolicy(None)
        try:
            policy.update("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_describe(self):
        rejected = False
        policy = cloudpassage.SpecialEventsPolicy(None)
        try:
            policy.describe("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected

    def test_delete(self):
        rejected = False
        policy = cloudpassage.SpecialEventsPolicy(None)
        try:
            policy.delete("DoesNotEvenMatter")
        except NotImplementedError:
            rejected = True
        assert rejected
