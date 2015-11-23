import pytest
import pep8
import imp
import json
import os

module_path = os.path.abspath('../cloudpassage')
policy_path = os.path.abspath('./policies')
file_location = os.path.abspath('../cloudpassage/fn.py')
this_file = os.path.abspath(__file__)

file, filename, data = imp.find_module('exceptions', [module_path])
exceptions = imp.load_module('exceptions', file, filename, data)
file, filename, data = imp.find_module('fn', [module_path])
fn = imp.load_module('fn', file, filename, data)


class TestFn:
    def test_pep8(self):
        pep8style = pep8.StyleGuide(quiet=True)
        result = pep8style.check_files([file_location, this_file])
        assert result.total_errors == 0

    def test_merge_dicts(self):
        one = {"a": "Alpha",
               "b": "Bravo",
               "c": "Charlie"}
        two = {"c": "CharlieHorse",
               "d": "Delta",
               "e": "Echo"}
        merge_one = fn.merge_dicts(one, two)
        merge_two = fn.merge_dicts(two, one)
        assert merge_one["c"] == "CharlieHorse"
        assert merge_two["c"] == "Charlie"

    def test_parse_status200(self):
        resp_text = "Test text, yo."
        url = "https://whatever.because.none/its-not-critical"
        code_exc = {200: None,
                    201: None,
                    202: None,
                    204: None,
                    400: exceptions.CloudPassageValidation(resp_text),
                    401: exceptions.CloudPassageAuthentication(resp_text),
                    403: exceptions.CloudPassageAuthorization(resp_text),
                    404: exceptions.CloudPassageResourceExistence(resp_text),
                    422: exceptions.CloudPassageValidation(resp_text),
                    999999: exceptions.CloudPassageGeneral(resp_text)}
        code_succ = {200: True,
                     201: True,
                     202: True,
                     204: True,
                     400: False,
                     401: False,
                     403: False,
                     404: False,
                     422: False,
                     "ARBLEGARBLE": False}
        for r, o in code_exc.items():
            success, exc = fn.parse_status(url, r, resp_text)
            assert type(o) == type(exc)
        for r, o in code_succ.items():
            success, exc = fn.parse_status(url, r, resp_text)
            assert success == o

    def test_verify_pages(self):
        assert fn.verify_pages("cats") is not None
        assert fn.verify_pages(101) is not None

    def test_sanitize_url_params(self):
        params = {"states": ["deactivated", "missing"]}
        desired_params = {"states": "deactivated,missing"}
        actual_result = fn.sanitize_url_params(params)
        assert desired_params == actual_result

    def test_determine_policy_metadata(self):
        test_csm_lin = {"file": str(policy_path +
                        "/cis-benchmark-for-centos-7-v1.policy.json"),
                        "type": "CSM",
                        "platform": "Linux"}
        test_fim_lin = {"file": str(policy_path +
                        "/core-system-files-centos-v1.fim.json"),
                        "type": "FIM",
                        "platform": "Linux"}
        test_lids_lin = {"file": str(policy_path +
                         "/core-system-centos-v1-1.lids.json"),
                         "type": "LIDS",
                         "platform": "Linux"}
        test_firewall_lin = {"file": str(policy_path +
                             "/firewall.json"),
                             "type": "Firewall",
                             "platform": "Linux"}
        for policy in [test_csm_lin,
                       test_fim_lin,
                       test_lids_lin,
                       test_firewall_lin]:
            with open(policy["file"], 'r') as f:
                policy_string = f.read()
                policy_json = json.loads(policy_string)
            meta_from_str = fn.determine_policy_metadata(policy_string)
            meta_from_json = fn.determine_policy_metadata(policy_json)
            assert meta_from_str == meta_from_json
            assert meta_from_str["policy_type"] == policy["type"]
            assert meta_from_str["target_platform"] == policy["platform"]
