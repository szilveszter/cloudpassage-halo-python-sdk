#!/usr/bin/env python

import sys
import time
import json
import urllib
import urllib2
import requests
import sanity
import fn
import base64
import threading
import datetime
from exceptions import CloudPassageAuthentication as exc_cp_authe
from exceptions import CloudPassageAuthorization as exc_cp_authz
from exceptions import CloudPassageValidation as exc_cp_val
from exceptions import CloudPassageCollision as exc_cp_coll
from exceptions import CloudPassageInternalError as exc_cp_internal
from exceptions import CloudPassageResourceExistence as exc_cp_exist
from exceptions import CloudPassageGeneral as exc_cp_general

class HaloSession:
    def __init__(self, apikey, apisecret, **kwargs):
        """ Create a Halo API connection object.

        On instantiation, it will attempt to authenticate
        against the Halo API using the apikey and apisecret
        provided, together with any overrides passed in through
        kwargs.

        Arguments:
        apikey     -- API key
        apisecret  -- API key secret

        Keyword arguments:
        api_host   -- Override the API endpoint hostname.
                      Defaults to api.cloudpassage.com.
        api_port   -- Override the API HTTPS port
                      Defaults to 443.
        proxy_host -- Hostname or IP address of proxy
        proxy_port -- Port for proxy.  Ignored if proxy_host is not set
        user_agent -- Override for UserAgent string.  We set this so that
                      we can see what tools are being used in the field and
                      set our development focus accordingly.  To override
                      the default, feel free to pass this kwarg in.
        """

        self.auth_url = 'oauth/access_token'
        self.api_host = 'api.cloudpassage.com'
        self.api_port = 443
        self.user_agent = 'CloudPassage Halo Python SDK v1.0'
        self.key_id = apikey
        self.secret = apisecret
        self.auth_token = None
        self.auth_scope = None
        self.proxy_host = None
        self.proxy_port = None
        self.lock = threading.RLock()
        self.api_count = 0
        self.api_time = 0.0
        # Override defaults for proxy
        if "proxy_host" in kwargs:
            self.proxy_host = kwargs["proxy_host"]
            if "proxy_port" in kwargs:
                self.proxy_port = kwargs["proxy_port"]
        # Override defaults for api host and port
        if "api_host" in kwargs:
            self.api_host = kwargs["api_host"]
        if "api_port" in kwargs:
            self.api_port = kwargs["api_port"]
        if "user_agent" in kwargs:
            self.user_agent = kwargs["user_agent"]

    def build_proxy_struct(host, port):
        """This builds a structure describing the environment's HTTP
        proxy requirements.

        It returns a dictionary object that can be passed to the
        requests module.
        """

        ret_struct = { "https": ""}
        if port is not None:
            ret_struct["https"] = "http://" + str(host) + ":" + str(port)
        else:
            ret_struct["https"] = "http://" + str(host) + ":8080"
        return(ret_struct)

    def get_auth_token(self, url, headers):
        """This method takes url and header info, and returns the
        oauth token and scope.

        url     -- Full URL, including schema.
            Ex: https://api.cloudpassage.com:443/oauth/access_token?grant_type=client_credentials"
        headers -- Dictionary, containing header with encoded
                   credentials.
            Ex: {"Authorization": str("Basic " + encoded)}
        """

        token = None
        scope = None
        resp = requests.post(url, headers=headers)
        if resp.status_code == 200:
            auth_resp_json = resp.json()
            token = auth_resp_json["access_token"]
            scope = auth_resp_json["scope"]
        if resp.status_code == 401:
            token = "BAD"
        return(token, scope)

    def authenticate_client(self):
        """This method attempts to set an OAuth token

        Call this method and it will use the API key and secret
        as well as the proxy settings (if used) to authenticate
        this HaloSession instance.

        """

        success = False
        #prefix = "https://" + self.api_host + ":" + str(self.api_port)
        prefix = self.build_url_prefix()
        url = prefix + "/oauth/access_token?grant_type=client_credentials"
        combined = self.key_id + ':' + self.secret
        encoded = base64.b64encode(combined)
        headers = {"Authorization": str("Basic " + encoded)}
        max_tries = 5
        for i in range(max_tries):
            token, scope = self.get_auth_token(url, headers)
            if token == "BAD":
                # Add message for IP restrictions
                exc_msg = "Invalid credentials- unable to obtain session token."
                raise exc_cp_authe(exc_msg)
            if token is not None:
                self.auth_token = token
                self.auth_scope = scope
                success = True
                break
            else:
                time.sleep(1)
        return(success)

    def build_url_prefix(self):
        """This constructs everything to the left of the file path in the URL.

        """

        prefix = "https://" + self.api_host + ":" + str(self.api_port)
        return(prefix)

    def build_header(self):
        """This constructs the auth header, required for all API interaction.

        """

        authstring = "Bearer "+ self.auth_token
        header = {"Authorization": authstring,
                  "Content-Type": "application/json",
                  "User-Agent": self.user_agent}

        return(header)

    def delete(self, path):
        """This method performs a DELETE against Halo's API.

        It will attempt to authenticate using the credentials (required
        to instantiate the object) if the session has either:
        1) Not been authenticated yet
        2) OAuth Token has expired

        This is a primary method, meaning it reaches out directly to the Halo
        API, and should only be utilized by secondary methods with a more
        specific purpose, like deleting server groups.  If you're
        using this method because the SDK doesn't provide a more specific
        method, please reach out to toolbox@cloudpassage.com so we can get
        an enhancement request in place for you.
        """

        if self.auth_token == None:
            self.authenticate_client()
        prefix = self.build_url_prefix()
        url = prefix + path
        headers = self.build_header()
        resp = requests.delete(url, headers=headers)
        if resp.status_code not in [200, 204]:
            if resp.status_code == 500:
                raise exc_cp_internal(resp.text)
            elif resp.status_code == 404:
                raise exc_cp_exist(url, resp.text)
            elif resp.status_code == 403:
                raise exc_cp_authz(resp.text)
            elif resp.status_code == 401:
                self.authenticate_client()
                headers = self.build_header()
                resp = requests.delete(url, headers=headers)
                if resp.status_code not in [200, 204]:
                    raise exc_cp_authz(resp.text)
            else:
                raise exc_cp_general(resp.text)
        return(resp.json())

    def get(self, path):
        """This method performs a GET against Halo's API.

        It will attempt to authenticate using the credentials (required
        to instantiate the object) if the session has either:
        1) Not been authenticated yet
        2) OAuth Token has expired

        This is a primary method, meaning it reaches out directly to the Halo
        API, and should only be utilized by secondary methods with a more
        specific purpose, like gathering events from /v1/events.  If you're
        using this method because the SDK doesn't provide a more specific
        method, please reach out to toolbox@cloudpassage.com so we can get
        an enhancement request in place for you.
        """

        if self.auth_token == None:
            self.authenticate_client()
        prefix = self.build_url_prefix()
        url = prefix + path
        headers = self.build_header()
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            if resp.status_code == 500:
                raise exc_cp_internal(resp.text)
            elif resp.status_code == 404:
                raise exc_cp_exist(url)
            elif resp.status_code == 403:
                raise exc_cp_authz(resp.text)
            elif resp.status_code == 401:
                self.authenticate_client()
                headers = self.build_header()
                resp = requests.get(url, headers=headers)
                if resp.status_code != 200:
                    raise exc_cp_authz(resp.text)
            else:
                raise exc_cp_general(resp.text)
        return(resp.json())

    def post(self, path, reqbody):
        """This method performs a POST against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.
        """

        ret_body = None
        if self.auth_token == None:
            self.authenticate_client()
        prefix = self.build_url_prefix()
        url = prefix + path
        headers = self.build_header()
        resp = requests.post(url, headers=headers, data=json.dumps(reqbody))
        if resp.status_code == 201:
            ret_body = resp.json()
        elif resp.status_code == 202:
            ret_body = resp.json()
        elif resp.status_code == 204:
            ret_body = {"status": "success"}
        elif resp.status_code == 400:
            raise exc_cp_val(resp.text)
        elif resp.status_code == 401:
            self.authenticate_client()
            headers = self.build_header()
            resp = requests.post(url, headers=headers, data=json.dumps(reqbody))
            if resp.status_code not in [200, 202, 204]:
                raise exc_cp_authz(resp.text)
            elif resp.status_code == 204:
                ret_body = {"status": "success"}
            else:
                ret_body = resp.json()
        elif resp.status_code == 403:
            raise exc_cp_authz(resp.text)
        elif resp.status_code == 404:
            raise exc_cp_exist(url, resp.text)
        elif resp.status_code == 422:
            raise exc_cp_val(resp.text)
        elif resp.status_code == 500:
            raise exc_cp_internal(resp.text)
        else:
            raise exc_cp_general(resp.text)
        return(ret_body)

    def put(self, path, reqbody):
        """This method performs a PUT against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.
        """

        ret_body = None
        if self.auth_token == None:
            self.authenticate_client()
        prefix = self.build_url_prefix()
        url = prefix + path
        headers = self.build_header()
        resp = requests.put(url, headers=headers, data=json.dumps(reqbody))
        if resp.status_code == 201:
            ret_body = resp.json()
        elif resp.status_code == 202:
            ret_body = resp.json()
        elif resp.status_code == 204:
            ret_body = {"status": "success"}
        elif resp.status_code == 400:
            raise exc_cp_val(resp.text)
        elif resp.status_code == 401:
            self.authenticate_client()
            headers = self.build_header()
            resp = requests.post(url, headers=headers, data=json.dumps(reqbody))
            if resp.status_code not in [200, 202, 204]:
                raise exc_cp_authz(resp.text)
            elif resp.status_code == 204:
                ret_body = {"status": "success"}
            else:
                ret_body = resp.json()
        elif resp.status_code == 403:
            raise exc_cp_authz(resp.text)
        elif resp.status_code == 404:
            raise exc_cp_exist(resp.url)
        elif resp.status_code == 422:
            raise exc_cp_val(resp.text)
        elif resp.status_code == 500:
            raise exc_cp_internal(resp.text)
        else:
            raise exc_cp_general(resp.text)
        return(ret_body)


# Class with calls to CloudPassage API
class HALO:

    def __init__(self):
        self.auth_url = 'oauth/access_token'
        self.auth_args = {'grant_type': 'client_credentials'}
        self.base_url = 'https://api.cloudpassage.com'
        self.api_ver = 'v1'
        self.port = 443
        self.key_id = None
        self.secret = None
        self.authToken = None
        self.authTokenScope = None
        self.lock = threading.RLock()
        self.api_count = 0
        self.api_time = 0.0

    # Dump debug info
    def dumpToken(self, token, expires):
        if (token):
            print "AuthToken=%s" % token
        if (expires):
            print "Expires in %s minutes" % (expires / 60)

    def getHttpStatus(self, code):
        if (code == 200):
            return "OK" 	# should never be passed in, only errors
        elif (code == 401):
            return "Unauthorized"
        elif (code == 403):
            return "Forbidden"
        elif (code == 404):
            return "Not found"
        elif (code == 422):
            return "Validation failed"
        elif (code == 500):
            return "Internal server error"
        elif (code == 502):
            return "Gateway error"
        else:
            return "Unknown code [%d]" % code

    def addAuth(self, req, kid, sec):
        combined = kid + ":" + sec
        encoded = base64.b64encode(combined)
        req.add_header("Authorization", "Basic " + encoded)

    def getAuthToken(self, url, args, kid, sec):
        req = urllib2.Request(url)
        self.addAuth(req, kid, sec)
        # print >> sys.stderr, "getAuthToken: key=%s secret=%s" % (kid, sec)
        # createPasswordMgr(url, kid, sec)
        if (args):
            args = urllib.urlencode(args)
        try:
            fh = urllib2.urlopen(req, args)
            return fh.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            elif hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to authorize [%s] at '%s'" % (
                    msg, url)
                data = e.read()
                if data:
                    print >> sys.stderr, "Extra data: %s" % data
                print >> sys.stderr, "Likely cause: incorrect API keys, id=%s" % kid
            else:
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return None

    def getInitialLink(self, fromDate, events_per_page):
        url = "%s:%d/%s/events?per_page=%d" % (self.base_url,
                                               self.port,
                                               self.api_ver,
                                               events_per_page)
        if (fromDate):
            url += "&since=" + fromDate
        return url

    def getEventBatch(self, url):
        return self.doGetRequest(url, self.authToken)

    def logTime(self, start_time, end_time):
        delta = end_time - start_time
        with self.lock:
            self.api_count += 1
            self.api_time += delta.total_seconds()

    def getTimeLog(self):
        tuple = None
        with self.lock:
            tuple = (self.api_count, self.api_time)
        return tuple

    def doGetRequest(self, url, token):
        req = urllib2.Request(url)
        req.add_header("Authorization", "Bearer " + token)
        try:
            start_time = datetime.datetime.now()
            fh = urllib2.urlopen(req)
            data = fh.read()
            contentType = fh.info().getheader('Content-type')
            (mimetype, encoding) = contentType.split("charset=")
            # print >> sys.stderr, "Type=%s  Encoding=%s" % (mimetype, encoding)
            translatedData = data.decode(encoding, 'ignore').encode('utf-8')
            results = (translatedData, False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
                if (e.reason == "Unauthorized"):
                    authError = True
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to fetch events [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            else:
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doPutRequest(self, url, token, putData):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url, data=putData)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: 'PUT'
        try:
            start_time = datetime.datetime.now()
            fh = opener.open(req)
            results = (fh.read(), False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doPostRequest(self, url, token, putData):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url, data=putData)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        try:
            start_time = datetime.datetime.now()
            fh = opener.open(req)
            results = (fh.read(), False)
            end_time = datetime.datetime.now()
            self.logTime(start_time, end_time)
            return results
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401) or (e.code == 403):
                    authError = True
                print >> sys.stderr, "Error response: %s" % e.read()
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def doDeleteRequest(self, url, token):
        opener = urllib2.build_opener(urllib2.HTTPHandler)
        req = urllib2.Request(url)
        req.add_header("Authorization", "Bearer " + token)
        req.add_header("Content-Type", "application/json")
        req.get_method = lambda: 'DELETE'
        try:
            fh = opener.open(req)
            return (fh.read(), False)
        except IOError, e:
            authError = False
            if hasattr(e, 'reason'):
                print >> sys.stderr, "Failed to connect [%s] to '%s'" % (
                    e.reason, url)
            if hasattr(e, 'code'):
                msg = self.getHttpStatus(e.code)
                print >> sys.stderr, "Failed to make request: [%s] from '%s'" % (
                    msg, url)
                if (e.code == 401):
                    authError = True
            if (not hasattr(e, 'reason')) and (not hasattr(e, 'code')):
                print >> sys.stderr, "Unknown error fetching '%s'" % url
            return (None, authError)

    def authenticateClient(self):
        url = "%s:%d/%s" % (self.base_url, self.port, self.auth_url)
        self.token = None
        response = self.getAuthToken(
            url, self.auth_args, self.key_id, self.secret)
        if (response):
            authRespObj = json.loads(response)
            if ('access_token' in authRespObj):
                self.authToken = authRespObj['access_token']
            if ('expires_in' in authRespObj):
                self.expires = authRespObj['expires_in']
            if ('scope' in authRespObj):
                self.authTokenScope = authRespObj['scope']
        # dumpToken(token,expires)
        return self.authToken

    def getServerList(self):
        url = "%s:%d/%s/servers" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getServerDetails(self,serverId):
        url = "%s:%d/%s/servers/%s" % (self.base_url,
                                     self.port,
                                     self.api_ver,
                                     serverId)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getServerGroupList(self):
        url = "%s:%d/%s/groups" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getServersInGroup(self, groupID):
        url = "%s:%d/%s/groups/%s/servers" % (self.base_url,
                                              self.port,
                                              self.api_ver,
                                              groupID)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getFirewallPolicyList(self):
        url = "%s:%d/%s/firewall_policies/" % (self.base_url,
                                               self.port,
                                               self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getFirewallPolicyDetails(self, policyID):
        url = "%s:%d/%s/firewall_policies/%s" % (self.base_url,
                                                 self.port,
                                                 self.api_ver,
                                                 policyID)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def moveServerToGroup(self, serverID, groupID):
        url = "%s:%d/%s/servers/%s" % (self.base_url,
                                       self.port,
                                       self.api_ver,
                                       serverID)
        reqData = {"server": {"group_id": groupID}}
        jsonData = json.dumps(reqData)
        # print "move: %s" % jsonData
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createServerGroup(self, groupName, **kwargs):
        url = "%s:%d/%s/groups" % (self.base_url, self.port, self.api_ver)
        groupData = {"name": groupName, "policy_ids": [], "tag": None}
        sanity.validate_servergroup_create_args(kwargs)
        reqData = {"group": fn.merge_dicts(groupData, kwargs)}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def updateServerGroup(self, groupId, **kwargs):
        url = "%s:%d/%s/groups/%s" % (self.base_url, self.port,
                                      self.api_ver, groupId)
        groupData = {}
        sanity.validate_servergroup_update_args(kwargs)
        reqData = {"group": fn.merge_dicts(groupData, kwargs)}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def updateServerGroup(self, groupId, **kwargs):
        url = "%s:%d/%s/groups/%s" % (self.base_url, self.port,
                                      self.api_ver, groupId)
        groupData = {}
        sanity.validate_servergroup_update_args(kwargs)
        reqData = {"group": fn.merge_dicts(groupData, kwargs)}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteServerGroup(self, group_id, **kwargs):
        if (("force" in kwargs) and (kwargs["force"] == True)):
            url = "%s:%d/%s/groups/%s%s" % (self.base_url,
                                            self.port,
                                            self.api_ver,
                                            group_id,
                                            "?move_to_parent=true")
        else:
            url = "%s:%d/%s/groups/%s" % (self.base_url,
                                          self.port,
                                          self.api_ver,
                                          group_id)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createFirewallPolicy(self, policyData):
        url = "%s:%d/%s/firewall_policies" % (self.base_url,
                                              self.port,
                                              self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listFirewallPolicies(self):
        url = "%s:%d/%s/firewall_policies" % (self.base_url,
                                              self.port,
                                              self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteFirewallPolicy(self, policyID):
        url = "%s:%d/%s/firewall_policies/%s" % (self.base_url,
                                                 self.port,
                                                 self.api_ver,
                                                 policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def assignFirewallPolicyToGroup(self, groupID, attrName, policyID):
        url = "%s:%d/%s/groups/%s" % (self.base_url,
                                      self.port,
                                      self.api_ver,
                                      groupID)
        reqData = {"group": {attrName: policyID}}
        jsonData = json.dumps(reqData)
        (data, authError) = self.doPutRequest(url, self.authToken, jsonData)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createConfigurationPolicy(self, policyData):
        url = "%s:%d/%s/policies" % (self.base_url, self.port, self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listConfigurationPolicies(self):
        url = "%s:%d/%s/policies" % (self.base_url, self.port, self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteConfigurationPolicy(self, policyID):
        url = "%s:%d/%s/policies/%s" % (self.base_url,
                                        self.port,
                                        self.api_ver,
                                        policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createFIMPolicy(self, policyData):
        url = "%s:%d/%s/fim_policies" % (self.base_url,
                                         self.port,
                                         self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listFIMPolicies(self):
        url = "%s:%d/%s/fim_policies" % (self.base_url,
                                         self.port,
                                         self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteFIMPolicy(self, policyID):
        url = "%s:%d/%s/fim_policies/%s" % (self.base_url,
                                            self.port,
                                            self.api_ver,
                                            policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def createLIDSPolicy(self, policyData):
        url = "%s:%d/%s/lids_policies" % (self.base_url,
                                          self.port, self.api_ver)
        jsonData = json.dumps(policyData)
        # print jsonData # for debugging
        (data, authError) = self.doPostRequest(url, self.authToken, jsonData)
        # print data
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def listLIDSPolicies(self):
        url = "%s:%d/%s/lids_policies" % (self.base_url,
                                          self.port,
                                          self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def deleteLIDSPolicy(self, policyID):
        url = "%s:%d/%s/lids_policies/%s" % (self.base_url,
                                             self.port,
                                             self.api_ver,
                                             policyID)
        (data, authError) = self.doDeleteRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def getAnnouncements(self):
        url = "%s:%d/%s/system_announcements" % (self.base_url,
                                                 self.port,
                                                 self.api_ver)
        (data, authError) = self.doGetRequest(url, self.authToken)
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)

    def initiateScan(self, serverId, scan_type):
        url = "%s:%d/%s/servers/%s/scans" % (self.base_url,
                                             self.port,
                                             self.api_ver,
                                             serverId)
        module_ref = {"sca": "sca",
                      "csm": "sca",
                      "sva": "svm",
                      "svm": "svm",
                      "fim": "fim",
                      "sam": "sam"}
        module = module_ref.get(scan_type)
        if module == None:
            bad_scan_msg = "Invalid scan type: " + str(scan_type)
            return (None, bad_scan_msg)
        jsondata = {"scan": {"module": module}}
        (data, authError) = self.doPostRequest(url,
                                               self.authToken,
                                               json.dumps(jsondata))
        if (data):
            return (json.loads(data), authError)
        else:
            return (None, authError)
