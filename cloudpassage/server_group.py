from http_helper import HttpHelper
import urlparse
import sanity
import fn


class ServerGroup:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all groups for an account

        This is represented as a list of dictionaries

        This handles pagination internally, so please
        be patient with high-volume requests.
        """

        session = self.session
        more_pages = True
        endpoint = "/v1/groups"
        groups = []
        request = HttpHelper(session)
        while more_pages:
            page = request.get(endpoint)
            for group in page["groups"]:
                groups.append(group)
            if "pagination" in page:
                if "next" in page["pagination"]:
                    endpoint = urlparse(page["pagination"]["next"]).path
            else:
                more_pages = False
        return(groups)

    def create(self, group_name, **kwargs):
        session = self.session
        endpoint = "/v1/groups"
        group_data = {"name": group_name, "policy_ids": [], "tag": None}
        sanity.validate_servergroup_create_args(kwargs)
        body = {"group": fn.merge_dicts(group_data, kwargs)}
        request = HttpHelper(session)
        try:
            response = request.post(endpoint, body)
        except post.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        return(response)
