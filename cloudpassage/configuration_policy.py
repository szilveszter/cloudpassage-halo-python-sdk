"""ConfigurationPolicy class"""

from cloudpassage.policy import Policy


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

    def endpoint(self):  # pylint: disable=no-self-use
        """Defines endpoint for API requests"""
        return "/v1/%s" % ConfigurationPolicy.policies

    def pagination_key(self):  # pylint: disable=no-self-use
        """Defines the pagination key for parsing paged results"""
        return ConfigurationPolicy.policies

    def policy_key(self):  # pylint: disable=no-self-use
        """Defines the key used to pull the policy from the json document"""
        return ConfigurationPolicy.policy
