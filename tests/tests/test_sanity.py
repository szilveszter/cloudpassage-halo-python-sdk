import cloudpassage
import json
import os
import pytest

sanity = cloudpassage.sanity


class TestFn:
    def test_servergroup_create_validate(self):
        rejected = False
        arguments = {"firewall_policy_id": unicode("12345"),
                     "linux_firewall_policy_id": None,
                     "windows_firewall_policy_id": None,
                     "policy_ids": ['12345'],
                     "windows_policy_ids": ['12345'],
                     "fim_policy_ids": ['12345'],
                     "linux_fim_policy_ids": ['12345'],
                     "windows_fim_policy_ids": ['12345'],
                     "lids_policy_ids": ['12345'],
                     "tag": None,
                     "name": "HelloWorld",
                     "special_events_policy": None,
                     "alert_profiles": "FAILURE"}
        try:
            sanity.validate_servergroup_create_args(arguments)
        except TypeError:
            rejected = True
        assert rejected

    def test_servergroup_update_validate(self):
        accepted = True
        arguments = {"firewall_policy_id": unicode("12345"),
                     "linux_firewall_policy_id": None,
                     "windows_firewall_policy_id": None,
                     "policy_ids": ['12345'],
                     "windows_policy_ids": ['12345'],
                     "fim_policy_ids": ['12345'],
                     "linux_fim_policy_ids": ['12345'],
                     "windows_fim_policy_ids": ['12345'],
                     "lids_policy_ids": ['12345'],
                     "tag": None,
                     "name": "HelloWorld",
                     "special_events_policy": None,
                     "alert_profiles": ['12345']}
        try:
            sanity.validate_servergroup_update_args(arguments)
        except:
            accepted = False
        assert accepted
