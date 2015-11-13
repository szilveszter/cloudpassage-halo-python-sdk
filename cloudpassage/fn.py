#!/usr/bin/env python
# Some basic data handling functions
from exceptions import CloudPassageValidation
from exceptions import CloudPassageInternalError
from exceptions import CloudPassageAuthentication
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageResourceExistence
from exceptions import CloudPassageCollision
from exceptions import CloudPassageGeneral


def merge_dicts(first, second):
    final = first.copy()
    final.update(second)
    return(final)


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
