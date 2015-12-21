"""General utilities"""


import json
import datetime
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.exceptions import CloudPassageInternalError
from cloudpassage.exceptions import CloudPassageAuthentication
from cloudpassage.exceptions import CloudPassageAuthorization
from cloudpassage.exceptions import CloudPassageResourceExistence
from cloudpassage.exceptions import CloudPassageGeneral


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
    # if type(policy) is str:
    if isinstance(policy, str):
        working_pol = json.loads(policy)
    elif isinstance(policy, dict):
        working_pol = policy.copy()
    else:
        print "Policy type must be str or dict!"
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
    return return_body


def sanitize_url_params(params):
    """Sanitize URL arguments for the Halo API

    In most cases, the Halo API will only honor the last value
    in URL arguments when multiple arguments have the same key.
    For instance: Requests builds URL arguments from a list a little
    strangely:
    {key:[val1, val2]}
    becomes key=val1&key=val2
    and not key=val1,val2.  If we let a
    list type object slide through, only val2 will be evaluated, and
    val1 is ignored by the Halo API.

    """
    params_working = params.copy()
    for key, value in params_working.items():
        if isinstance(value, list):
            value_corrected = ",".join(value)
            params[key] = value_corrected
        if isinstance(value, datetime.datetime):
            value_corrected = datetime_to_8601(value)
            params[key] = value_corrected
    return params


def policy_to_dict(policy):
    """Ensures that policy is a dictionary object"""
    if isinstance(policy, dict):
        return policy
    else:
        return json.loads(policy)


def merge_dicts(first, second):
    """Merges dictionaries"""
    final = first.copy()
    final.update(second)
    return final


def verify_pages(max_pages):
    """Verify the user isn't trying to pull too many pages in one query"""
    exc = None
    if type(max_pages) is not int:
        fail_msg = "Type wrong for max_pages.  Should be int."
        exc = CloudPassageValidation(fail_msg)
    if max_pages > 100:
        fail_msg = "You're asking for too many pages.  100 max."
        exc = CloudPassageValidation(fail_msg)
    return exc


def parse_status(url, resp_code, resp_text):
    """Parse status from HTTP response"""
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
    return success, exc


def time_string_now():
    """Returns an ISO 8601 formatted string for now, in UTC

    Returns:
        str: ISO 8601 formatted string

    """

    now = datetime.datetime.utcnow()
    return datetime_to_8601(now)


# There should be a built-in function for coverting to 8601.
def datetime_to_8601(original_time):
    """Converts a datetime object to ISO 8601 formatted string.

    Args:
        dt (datetime.datetime): Datetime-type object

    Returns:
        str: ISO 8610 formatted string

    """

    time_split = (original_time.year, original_time.month, original_time.day,
                  original_time.hour, original_time.minute,
                  original_time.second, original_time.microsecond)
    return "%04d-%02d-%02dT%02d:%02d:%02d.%06dZ" % time_split
