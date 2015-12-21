'''
docstring
'''

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

    def endpoint(self):  # pylint: disable=no-self-use,missing-docstring
        return "/v1/%s" % ConfigurationPolicy.policies

    def pagination_key(self):  # pylint: disable=no-self-use,missing-docstring
        return ConfigurationPolicy.policies

    def policy_key(self):  # pylint: disable=no-self-use,missing-docstring
        return ConfigurationPolicy.policy
