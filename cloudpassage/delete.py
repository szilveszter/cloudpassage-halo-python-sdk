import fn
import requests

class Delete:
    def __init__(self, connection):
        self.connection = connection

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

        if self.connection.auth_token == None:
            self.connection.authenticate_client()
        prefix = self.connection.build_url_prefix()
        url = prefix + path
        headers = self.connection.build_header()
        resp = requests.delete(url, headers=headers)
        success, exc = fn.parse_status(url, resp.status_code, resp.text)
        if success is False:
            # If we get a 401, it could be an expired key.  We retry once.
            if resp.status_code == 401:
                self.connection.authenticate_client()
                headers = self.connection.build_header()
                resp = requests.delete(url, headers=headers)
                success, exc = fn.parse_status(url, resp.status_code, resp.text)
                if success is True:
                    return(resp.json())
            raise exc
        else:
            return(resp.json())
