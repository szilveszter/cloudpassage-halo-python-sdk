import fn
from http_helper import HttpHelper
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence


class ConfigurationPolicy:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all configuration policies"""

        request = HttpHelper(self.session)
        endpoint = "/v1/policies"
        key = "policies"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, policy_id):
        """Returns the body of the policy indicated by policy_id.

        If used with update(), make sure to enclose like so:
        {"policy": policy_body}
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/policies/%s" % policy_id
        response = request.get(endpoint)
        result = response["policy"]
        return(result)

    def create(self, policy_body):
        """Creates a CSM policy from JSON document.

        Returns the ID of the new policy
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/policies/"
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(policy_body)
        request_body = fn.policy_to_dict(policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "CSM":
            error_message = "Policy type is not CSM"
            raise CloudPassageValidation(error_message)
        else:
            response = request.post(endpoint, request_body)
            policy_id = response["policy"]["id"]
            return(policy_id)

    def delete(self, policy_id):
        """Delete a CSM policy by ID"""

        request = HttpHelper(self.session)
        endpoint = "/v1/policies/%s" % policy_id
        response = request.delete(endpoint)
        return(None)

    def update(self, policy_body):
        """Update a CSM policy.  Success returns None"""

        request = HttpHelper(self.session)
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(policy_body)
        request_body = fn.policy_to_dict(policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "CSM":
            error_message = "Policy type is not CSM"
            raise self.CloudPassageValidation(error_message)
        else:
            policy_id = request_body["policy"]["id"]
            endpoint = "/v1/policies/%s" % policy_id
            response = request.put(endpoint, request_body)
            return(None)
