"""SyetemAnnouncement class"""


from cloudpassage.http_helper import HttpHelper


class SystemAnnouncement(object):
    """Initializing the SystemAnnouncement class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

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
        return announcement_list
