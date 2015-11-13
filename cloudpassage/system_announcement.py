from http_helper import HttpHelper
import urlparse


class SystemAnnouncement:
    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all system announcements
        """

        session = self.session
        endpoint = "/v1/system_announcements"
        request = HttpHelper(session)
        response = request.get(endpoint)
        announcement_list = response["announcements"]
        return(announcement_list)
