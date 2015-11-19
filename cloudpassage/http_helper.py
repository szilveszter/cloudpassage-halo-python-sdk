import fn
import json
import requests
import urlparse


class HttpHelper:
    from exceptions import CloudPassageAuthentication
    from exceptions import CloudPassageAuthorization
    from exceptions import CloudPassageValidation
    from exceptions import CloudPassageCollision
    from exceptions import CloudPassageInternalError
    from exceptions import CloudPassageResourceExistence
    from exceptions import CloudPassageGeneral

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
        response = requests.get(endpoint, headers=headers)
        success, exc = fn.parse_status(endpoint, response.status_code,
                                       response.text)
        if success is True:
            return(response.json())
        # If we get a 401, it could be an expired key.  We retry once.
        if response.status_code == 401:
            self.connection.authenticate_client()
            headers = self.connection.build_header()
            response = requests.get(endpoint, headers=headers)
            success, exc = fn.parse_status(endpoint, response.status_code,
                                           response.text)
            if success is True:
                return(response.json())
        raise exc

    def get_paginated(self, endpoint, key, max_pages):
        """This method returns a concatenated list of objects
        from the Halo API.

        It's really a wrapper for the get() method.  Pass in the
        path as with the get() method, and a maxpages number.
        Maxpages is expected to be an integer between 2 and 100

        endpoint  -- Path for initial query
        key       -- The key in the response containing the objects
                     of interest.  For instance, the /v1/events endpoint
                     will have the "events" key, which contains a list
                     of dictionary objects representing Halo events.
        maxpages  -- This is a number from 2-100.  More than 100 pages
                     can take quite a while to return, so beyond that
                     you should consider using this SDK as a component
                     in  multi-threaded tool.
        """

        exception = fn.verify_pages(max_pages)
        if exception:
            raise exception
        more_pages = True
        response_accumulator = []
        pages_parsed = 0
        while more_pages:
            page = self.get(endpoint)
            if key not in page:
                fail_msg = ("Requested key %s not found in page %s"
                            % (key, endpoint))
                raise self.CloudPassageValidation(fail_msg)
            for k in page[key]:
                response_accumulator.append(k)
            pages_parsed += 1
            # If we hit our limit for parsed pages, return out!
            if pages_parsed >= max_pages:
                return response_accumulator
            if "pagination" in page:
                if "next" in page["pagination"]:
                    nextpage = page["pagination"]["next"]
                    endpoint = str(urlparse.urlsplit(nextpage)[2] + "?" +
                                   urlparse.urlsplit(nextpage)[3])
                else:
                    more_pages = False
            else:
                more_pages = False
        return response_accumulator

    def post(self, path, reqbody):
        """This method performs a POST against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.
        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        response = requests.post(endpoint, headers=headers,
                                 data=json.dumps(reqbody))
        success, exc = fn.parse_status(endpoint,
                                       response.status_code, response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.post(endpoint, headers=headers,
                                         data=json.dumps(reqbody))
                success, exc = fn.parse_status(endpoint, response.status_code,
                                               response.text)
                if success is True:
                    return(response.json())
            raise exc
        else:
            return(response.json())

    def put(self, path, reqbody):
        """This method performs a PUT against Halo's API.

        As with the GET method, it will attempt to (re)authenticate
        the session if the key is expired or has not yet been retrieved.

        Also like the GET method, it is not intended for direct use (though
        we won't stop you).  If you need something that the SDK doesn't
        already provide, please reach out to toolbox@cloudpassage.com and
        let us get an enhancement request submitted for you.
        """

        if self.connection.auth_token is None:
            self.connection.authenticate_client()
        prefix = self.connection.build_endpoint_prefix()
        endpoint = prefix + path
        headers = self.connection.build_header()
        response = requests.put(endpoint, headers=headers,
                                data=json.dumps(reqbody))
        success, exc = fn.parse_status(endpoint, response.status_code,
                                       response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.put(endpoint, headers=headers,
                                        data=json.dumps(reqbody))
                success, exc = fn.parse_status(endpoint, response.status_code,
                                               response.text)
                if success is True:
                    return(response.json())
            raise exc
        else:
            # Sometimes we don't get json back...
            try:
                return_value = response.json()
            except:
                return_value = response.text
            return(return_value)

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
        response = requests.delete(endpoint, headers=headers)
        success, exc = fn.parse_status(endpoint, response.status_code,
                                       response.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if response.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                response = requests.delete(endpoint, headers=headers)
                success, exc = fn.parse_status(endpoint, response.status_code,
                                               response.text)
                if success is True:
                    return(response.json())
            raise exc
        else:
            # Sometimes we don't get json back...
            try:
                return_value = response.json()
            except:
                return_value = response.text
            return(return_value)
