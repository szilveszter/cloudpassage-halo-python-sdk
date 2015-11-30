import fn
from http_helper import HttpHelper


class LidsPolicy:
    from exceptions import CloudPassageValidation
    from exceptions import CloudPassageResourceExistence

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all LIDS policies"""

        request = HttpHelper(self.session)
        endpoint = "/v1/lids_policies"
        key = "lids_policies"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, lids_policy_id):
        """Returns the body of the LIDS policy indicated by lids_policy_id.

        If used with update(), make sure to enclose like so:
        {"lids_policy": lids_policy_body}
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/lids_policies/%s" % lids_policy_id
        response = request.get(endpoint)
        result = response["lids_policy"]
        return(result)

    def create(self, lids_policy_body):
        """Creates a LIDS policy from JSON document.

        Returns the ID of the new policy
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/lids_policies/"
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(lids_policy_body)
        request_body = fn.policy_to_dict(lids_policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "LIDS":
            error_message = "Policy type is not LIDS"
            raise CloudPassageValidation(error_message)
        else:
            response = request.post(endpoint, request_body)
            lids_policy_id = response["lids_policy"]["id"]
            return(lids_policy_id)

    def delete(self, lids_policy_id):
        """Delete a LIDS policy by ID"""

        request = HttpHelper(self.session)
        endpoint = "/v1/lids_policies/%s" % lids_policy_id
        response = request.delete(endpoint)
        return(None)

    def update(self, lids_policy_body):
        """Update a LIDS policy.  Success returns None"""

        request = HttpHelper(self.session)
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(lids_policy_body)
        request_body = fn.policy_to_dict(lids_policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "LIDS":
            error_message = "Policy type is not LIDS"
            raise self.CloudPassageValidation(error_message)
        else:
            lids_policy_id = request_body["lids_policy"]["id"]
            endpoint = "/v1/lids_policies/%s" % lids_policy_id
            response = request.put(endpoint, request_body)
            return(None)
