from http_helper import HttpHelper
import urlparse
import sanity
import fn
from exceptions import CloudPassageAuthentication
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageValidation
from exceptions import CloudPassageCollision
from exceptions import CloudPassageInternalError
from exceptions import CloudPassageResourceExistence
from exceptions import CloudPassageGeneral


class ServerGroup:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all groups for an account

        This is represented as a list of dictionaries

        This will only return a maximum of 20 pages, which amounts to
        200 groups.  If you have more than that, you should consider
        using the SDK within a multi-threaded application so you don't
        spend the rest of your life waiting on a list of groups.
        """

        session = self.session
        max_pages = 20
        key = "groups"
        endpoint = "/v1/groups"
        request = HttpHelper(session)
        groups = request.get_paginated(endpoint, key, max_pages)
        return(groups)

    def list_members(self, group_id):
        """Returns a list of all servers which are members of group_id"""

        session = self.session
        endpoint = "/v1/groups/%s/servers" % group_id
        request = HttpHelper(session)
        response = request.get(endpoint)
        servers = response["servers"]
        return(servers)

    def create(self, group_name, **kwargs):
        """Creates a ServerGroup.  Requires a group name, other
        things via kwargs.

        Optional kwargs and expected daya types:
        name                         -- unicode
        firewall_policy_id           -- unicode
                                     (deprecated- use linux_firewall_policy_id)
        linux_firewall_policy_id     -- unicode
        windows_firewall_policy_id   -- unicode
        policy_ids                   -- list
        windows_policy_ids           -- list
        fim_policy_ids               -- list
        linux_fim_policy_ids         -- list
        windows_fim_policy_ids       -- list
        lids_policy_ids              -- list
        tag                          -- unicode
        events_policy                -- unicode
        alert_profiles               -- list
        """

        session = self.session
        endpoint = "/v1/groups"
        group_data = {"name": group_name, "policy_ids": [], "tag": None}
        try:
            sanity.validate_servergroup_create_args(kwargs)
        except TypeError as e:
            raise CloudPassageValidation(e)
        body = {"group": fn.merge_dicts(group_data, kwargs)}
        request = HttpHelper(session)
        try:
            response = request.post(endpoint, body)
        except post.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        return(response)

    def describe(self, group_id):
        """Describe a ServerGroup, referenced by ID

        Returns a dictionary object
        """

        session = self.session
        endpoint = "/v1/groups/%s" % group_id
        request = HttpHelper(session)
        response = request.get(endpoint)
        group = response["group"]
        return(group)

    def update(self, groupId, **kwargs):
        """Updates a ServerGroup.  Requires a group ID, other
        things via kwargs.

        Optional kwargs and expected daya types:
        name                         -- unicode
        firewall_policy_id           -- unicode
                                     (deprecated- use linux_firewall_policy_id)
        linux_firewall_policy_id     -- unicode
        windows_firewall_policy_id   -- unicode
        policy_ids                   -- list
        windows_policy_ids           -- list
        fim_policy_ids               -- list
        linux_fim_policy_ids         -- list
        windows_fim_policy_ids       -- list
        lids_policy_ids              -- list
        tag                          -- unicode
        events_policy                -- unicode
        alert_profiles               -- list
        """

        endpoint = "/v1/groups/%s" % groupId
        response = None
        groupData = {}
        try:
            sanity.validate_servergroup_update_args(kwargs)
        except TypeError as e:
            raise CloudPassageValidation(e)
        body = {"group": fn.merge_dicts(groupData, kwargs)}
        request = HttpHelper(session)
        try:
            response = request.put(endpoint, body)
        except put.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        except put.CloudPassageValdiation as e:
            raise CloudPassageValidation(e.msg)
        return(response)
