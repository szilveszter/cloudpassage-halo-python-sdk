'''
docstring
'''


import cloudpassage.utility as utility
from cloudpassage.http_helper import HttpHelper


class Event(object):
    """Initializing the Event class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        self.supported_search_fields = [
            "group_id",
            "server_id",
            "server_platform",
            "type",
            "since",
            "until",
            "pages"
        ]
        return None

    def list_all(self, pages, **kwargs):
        """Returns a list of all events.


        Default filter returns ALL events.  This is a very verbose \
        and time-consuming operation.

        Args:
            pages (int): Max number of pages (of ten items each) to retrieve

        Keyword Args:
            group_id (list or str): A list or comma-separated string \
            containing the group IDs to retrieve events for.
            server_id (list or str): A list or comma-separated string \
            containing the server IDs to retrieve events for.
            server_platform (str): (linux | windows)
            type (list or str): A list or comma-separated string containing \
            the event types to query for.  A complete list of event types is \
            available \
            `here: <https://support.cloudpassage.com/entries/23125117-Events\
            #event-types>`_
            since (str): ISO 8601 formatted string representing the starting \
            date and time for query
            until (str): ISO 8601 formatted string representing the ending \
            date and time for query

        Returns:
            list: List of dictionary objects describing servers

        """

        endpoint = "/v1/events"
        request_params_raw = {}
        key = "events"
        max_pages = pages
        request = HttpHelper(self.session)
        for param in self.supported_search_fields:
            if param in kwargs:
                request_params_raw[param] = kwargs[param]
        if request_params_raw != {}:
            request_params = utility.sanitize_url_params(request_params_raw)
            response = request.get_paginated(endpoint, key, max_pages,
                                             params=request_params)
        else:
            response = request.get_paginated(endpoint, key, max_pages)
        return response
