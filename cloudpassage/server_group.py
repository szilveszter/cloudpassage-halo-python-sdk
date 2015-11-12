import urlparse
import sanity
import delete
import post
import put
import get
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
        url = "/v1/groups"
        groups = []
        conn = get.Get(session)
        while more_pages:
            page = conn.get(url)
            for group in page["groups"]:
                groups.append(group)
            if "pagination" in page:
                if "next" in page["pagination"]:
                    url = urlparse(page["pagination"]["next"]).path
            else:
                more_pages = False
        return(groups)

    def create(self, group_name, **kwargs):
        session = self.session
        url = "/v1/groups"
        group_data = {"name": group_name, "policy_ids": [], "tag": None}
        sanity.validate_servergroup_create_args(kwargs)
        req_data = {"group": fn.merge_dicts(group_data, kwargs)}
        conn = post.Post(session)
        try:
            response = conn.post(url, req_data)
        except post.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        return(response)
