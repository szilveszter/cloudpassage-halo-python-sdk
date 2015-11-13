import fn
import json
import requests
from exceptions import CloudPassageAuthentication
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageValidation
from exceptions import CloudPassageCollision
from exceptions import CloudPassageInternalError
from exceptions import CloudPassageResourceExistence
from exceptions import CloudPassageGeneral


class HttpHelper:
    def __init__(self, connection):
        self.connection = connection

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

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        resp = requests.get(endpoint, headers=headers)
        success, exc = fn.parse_status(endpoint, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.get(endpoint, headers=headers)
                success, exc = fn.parse_status(endpoint, resp.status_code,
                                               resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
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
        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        resp = requests.post(endpoint, headers=headers, data=json.dumps(reqbody))
        success, exc = fn.parse_status(endpoint, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.post(endpoint, headers=headers,
                                     data=json.dumps(reqbody))
                success, exc = fn.parse_status(endpoint, resp.status_code,
                                               resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
            return(resp.json())

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
        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        resp = requests.put(endpoint, headers=headers, data=json.dumps(reqbody))
        success, exc = fn.parse_status(endpoint, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.put(endpoint, headers=headers,
                                    data=json.dumps(reqbody))
                success, exc = fn.parse_status(endpoint, resp.status_code,
                                               resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
            return(resp.json())

    def delete(self, path):
        """This method performs a Delete against Halo's API.

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

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        resp = requests.delete(endpoint, headers=headers)
        success, exc = fn.parse_status(endpoint, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.delete(endpoint, headers=headers)
                success, exc = fn.parse_status(endpoint, resp.status_code,
                                               resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
            return(resp.json())
