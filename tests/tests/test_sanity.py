import pytest
import pep8
import imp
import json
import os

module_path = os.path.abspath('../cloudpassage')

file_location = os.path.abspath('../cloudpassage/sanity.py')
this_file = os.path.abspath(__file__)

file, filename, data = imp.find_module('sanity', [module_path])
fn = imp.load_module('sanity', file, filename, data)


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
            fn.validate_servergroup_create_args(arguments)
        except TypeError:
            rejected = True
        assert rejected

    def test_servergroup_update_validate(self):
        accepted = True
        arguments = {"firewall_policy_id": None}
        try:
            fn.validate_servergroup_update_args(arguments)
        except:
            accepted = False
        assert accepted
