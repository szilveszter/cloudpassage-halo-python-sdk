import cloudpassage
import json
import os
import pytest

sanity = cloudpassage.sanity


class TestFn:
    def test_servergroup_create_validate(self):
        rejected = False
        arguments = {"firewall_policy_id": unicode("helloworld"),
                     "linux_firewall_policy_id": unicode("helloworld"),
                     "windows_firewall_policy_id": unicode("helloworld"),
                     "policy_ids": ["helloworld"],
                     "windows_policy_ids": "THISFAILS"}
        try:
            sanity.validate_servergroup_create_args(arguments)
        except TypeError:
            rejected = True
        assert rejected

    def test_servergroup_update_validate(self):
        accepted = True
        arguments = {"firewall_policy_id": None}
        try:
            sanity.validate_servergroup_update_args(arguments)
        except:
            accepted = False
        assert accepted
