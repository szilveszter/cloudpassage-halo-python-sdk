from http_helper import HttpHelper
import fn


class FimPolicy:

    def __init__(self, session):
        self.session = session
        return None

    def list_all(self):
        """Returns a list of all FIM policies"""

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies"
        key = "fim_policies"
        max_pages = 30
        response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def describe(self, fim_policy_id):
        """Returns the body of the policy indicated by policy_id.

        If used with update(), make sure to enclose like so:
        {"policy": policy_body}
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s" % fim_policy_id
        response = request.get(endpoint)
        result = response["fim_policy"]
        return(result)

    def create(self, fim_policy_body):
        """Creates a FIM policy from JSON document.

        Returns the ID of the new policy
        """

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/"
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(fim_policy_body)
        request_body = fn.policy_to_dict(fim_policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "FIM":
            error_message = "Policy type is not FIM"
            raise CloudPassageValidation(error_message)
        else:
            response = request.post(endpoint, request_body)
            policy_id = response["fim_policy"]["id"]
            return(policy_id)

    def delete(self, fim_policy_id):
        """Delete a FIM policy by ID"""

        request = HttpHelper(self.session)
        endpoint = "/v1/fim_policies/%s" % fim_policy_id
        response = request.delete(endpoint)
        return(None)

    def update(self, fim_policy_body):
        """Update a FIM policy.  Success returns None"""

        request = HttpHelper(self.session)
        # Make sure it's the right kind of policy
        policy_metadata = fn.determine_policy_metadata(fim_policy_body)
        request_body = fn.policy_to_dict(fim_policy_body)
        policy_type = policy_metadata["policy_type"]
        if policy_type is not "FIM":
            error_message = "Policy type is not FIM"
            raise self.CloudPassageValidation(error_message)
        else:
            fim_policy_id = request_body["fim_policy"]["id"]
            endpoint = "/v1/fim_policies/%s" % fim_policy_id
            response = request.put(endpoint, request_body)
            return(None)


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
