#!/usr/bin/env python
# Some basic data handling functions
import json
from exceptions import CloudPassageValidation
from exceptions import CloudPassageInternalError
from exceptions import CloudPassageAuthentication
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageResourceExistence
from exceptions import CloudPassageCollision
from exceptions import CloudPassageGeneral


def determine_policy_metadata(policy):
    """Accepts string or dict.  Returns dict of policy
    type, name, and target platform.

    If string, attempts to convert to dict to parse.
    Possible return values for policy_type:
    CSM      -- Configuration Security Monitoring
    FIM      -- File Integrity Monitoring
    LIDS     -- Log Intrusion Detection System
    Firewall -- Firewall Policy
    None     -- Unable to determine poolicy type

    Possible return values for target_platform:
    Windows
    Linux
    None

    Example:
    determine_policy_type(string_from_file)
    {"policy_type": "CSM",
     "policy_name": "Test policy",
     "target_platform": "Windows"}

    """

    return_body = {"policy_type": None,
                   "policy_name": None,
                   "target_platform": None}
    if type(policy) is str:
        working_pol = json.loads(policy)
    elif type(policy) is dict:
        working_pol = policy.copy()
    else:
        print("Policy type must be str or dict!")
    try:
        derived_type = working_pol.items()[0][0]
        if derived_type == "fim_policy":
            return_body["policy_type"] = "FIM"
        if derived_type == "policy":
            return_body["policy_type"] = "CSM"
        if derived_type == "lids_policy":
            return_body["policy_type"] = "LIDS"
        if derived_type == "firewall_policy":
            return_body["policy_type"] = "Firewall"
    except:
        pass
    try:
        return_body["policy_name"] = working_pol.items()[0][1]["name"]
    except:
        pass
    try:
        derived_platform = working_pol.items()[0][1]["platform"]
        if derived_platform == 'linux':
            return_body["target_platform"] = 'Linux'
        elif derived_platform == 'windows':
            return_body["target_platform"] = 'Windows'
    except:
        pass
    return(return_body)


def policy_to_dict(policy):
    if type(policy) is dict:
        return policy
    else:
        return(json.loads(policy))


def merge_dicts(first, second):
    final = first.copy()
    final.update(second)
    return(final)


def verify_pages(max_pages):
    exc = None
    if type(max_pages) is not int:
        fail_msg = "Type wrong for max_pages.  Should be int."
        exc = CloudPassageValidation(fail_msg)
    if max_pages > 100:
        fail_msg = "You're asking for too many pages.  100 max."
        exc = CloudPassageValidation(fail_msg)
    return exc


def parse_status(url, resp_code, resp_text):
    success = True
    exc = None
    if resp_code not in [200, 201, 202, 204]:
        success = False
        if resp_code == 500:
            exc = CloudPassageInternalError(resp_text)
        elif resp_code == 400:
            exc = CloudPassageValidation(resp_text)
        elif resp_code == 401:
            exc = CloudPassageAuthentication(resp_text)
        elif resp_code == 404:
            exc = CloudPassageResourceExistence(url)
        elif resp_code == 403:
            exc = CloudPassageAuthorization(resp_text)
        elif resp_code == 422:
            exc = CloudPassageValidation(resp_text)
        else:
            exc = CloudPassageGeneral(resp_text)
    return(success, exc)
