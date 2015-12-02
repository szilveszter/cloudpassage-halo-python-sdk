from policy import Policy
from http_helper import HttpHelper
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence
import fn


class FimPolicy(Policy):

    policy = "fim_policy"
    policies = "fim_policies"

    def endpoint(self):
        return("/v1/%s" % FimPolicy.policies)

    def pagination_key(self):
        return(FimPolicy.policies)

    def policy_key(self):
        return(FimPolicy.policy)


class FimBaseline:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self, fim_policy_id):
        """Returns a list of all baselines for the indicated FIM policy"""

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines" % fim_policy_id
        key = "baselines"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, fim_policy_id, fim_baseline_id):
        """Returns the body of the baseline indicated by fim_baseline_id.

        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        response = request.get(endpoint)
        result = response["baseline"]
        return(result)

    def create(self, fim_policy_id, server_id, **kwargs):
        """Creates a FIM baseline

        kwargs:
        expires   -- Number of days from today, when baseline expires
        comment   -- Something meaningful in string form
        Returns the ID of the new baseline
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines" % fim_policy_id
        request_body = {"baseline": {"server_id": server_id,
                                     "expires": None,
                                     "comment": None}}
        if "expires" in kwargs:
            request_body["expires"] = kwargs["expires"]
        if "comment" in kwargs:
            request_body["comment"] = kwargs["comment"]
        response = request.post(endpoint, request_body)
        policy_id = response["baseline"]["id"]
        return(policy_id)

    def delete(self, fim_policy_id, fim_baseline_id):
        """Delete a FIM baseline by ID"""

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        response = request.delete(endpoint)
        return(None)

    def update(self, fim_policy_id, fim_baseline_id, server_id):
        """Update a FIM policy.  Success returns None"""

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s/baselines/%s" % (fim_policy_id,
                                                         fim_baseline_id)
        request_body = {"baseline": {"server_id": server_id}}
        response = request.put(endpoint, request_body)
        return(None)
