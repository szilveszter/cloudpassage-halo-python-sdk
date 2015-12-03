from policy import Policy


class LidsPolicy(Policy):
    """Initializing the LidsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "lids_policy"
    policies = "lids_policies"

    def endpoint(self):
        return("/v1/%s" % LidsPolicy.policies)

    def pagination_key(self):
        return(LidsPolicy.policies)

    def policy_key(self):
        return(LidsPolicy.policy)
