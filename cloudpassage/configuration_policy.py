from policy import Policy


class ConfigurationPolicy(Policy):
    """Initializing the ConfigurationPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "policy"
    policies = "policies"

    def endpoint(self):
        return("/v1/%s" % ConfigurationPolicy.policies)

    def pagination_key(self):
        return(ConfigurationPolicy.policies)

    def policy_key(self):
        return(ConfigurationPolicy.policy)
