import cloudpassage
import pytest
import pep8
import json
import os

file_location = os.path.abspath('../cloudpassage/sanity.py')
this_file = os.path.abspath(__file__)
sanity = cloudpassage.sanity


class TestFn:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

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
