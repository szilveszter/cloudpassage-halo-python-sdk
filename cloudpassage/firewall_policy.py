from http_helper import HttpHelper
import fn


class FirewallPolicy:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all firewall policies"""

        request = HttpHelper(self.session)
        endpoint = "/v1/firewall_policies"
        key = "firewall_policies"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, firewall_policy_id):
        """Returns the body of the firewall policy indicated
        by firewall_policy_id.

        """

        request = HttpHelper(self.session)
        endpoint = "/v1/firewall_policies/%s" % firewall_policy_id
        response = request.get(endpoint)
        result = response["firewall_policy"]
        return(result)

    def create(self, policy_body):
        """Creates a firewall policy from JSON document.

        Returns the ID of the new policy
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/firewall_policies/"
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(policy_body)
        request_body = fn.policy_to_dict(policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "Firewall":
            error_message = "Policy type is not Firewall"
            raise CloudPassageValidation(error_message)
        else:
            response = request.post(endpoint, request_body)
            policy_id = response["firewall_policy"]["id"]
            return(policy_id)

    def delete(self, firewall_policy_id):
        """Delete a firewall policy by ID"""

        request = HttpHelper(self.session)
        endpoint = "/v1/firewall_policies/%s" % firewall_policy_id
        response = request.delete(endpoint)
        return(None)

    def update(self, firewall_policy_id, **kwargs):
        """Update a firewall policy.  Success returns None

        Allowed kwargs:
        name
        descripton
        """

        allowed_args = ["name", "description"]
        request = HttpHelper(self.session)
        request_body = {}
        for arg in allowed_args:
            if arg in kwargs:
                request_body[arg] = kwargs[arg]
        if request_body == {}:
            error_message = "No valid metadata fields detected."
            raise CloudPassageValidation(error_message)
        endpoint = "/v1/firewall_policies/%s" % firewall_policy_id
        response = request.put(endpoint, request_body)
        return(None)
