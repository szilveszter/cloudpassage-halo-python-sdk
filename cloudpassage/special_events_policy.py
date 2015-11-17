from http_helper import HttpHelper
import urlparse


class SpecialEventsPolicy:
    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all special events policies
        """

        session = self.session
        endpoint = "/v1/special_events_policies"
        request = HttpHelper(session)
        response = request.get(endpoint)
        special_events_policies = response["special_events_policies"]
        return(special_events_policies)
