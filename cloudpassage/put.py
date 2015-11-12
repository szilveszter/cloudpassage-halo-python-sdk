import fn
import json
import requests

class Put:
    def __init__(self, connection):
        self.connection = connection

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
        if self.connection.auth_token == None:
            self.connection.authenticate_client()
        prefix = self.connection.build_url_prefix()
        url = prefix + path
        headers = self.connection.build_header()
        resp = requests.put(url, headers=headers, data=json.dumps(reqbody))
        success, exc = fn.parse_status(url, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.put(url, headers=headers,
                                    data=json.dumps(reqbody))
                success, exc = fn.parse_status(url, resp.status_code, resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
            return(resp.json())
