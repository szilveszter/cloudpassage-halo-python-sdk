'''docstring'''

from cloudpassage.policy import Policy


class AlertProfile(Policy):
    """Initializing the AlertProfile class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "alert_profile"
    policies = "alert_profiles"

    def endpoint(self):  # pylint: disable=no-self-use,missing-docstring
        return "/v1/%s" % AlertProfile.policies

    def pagination_key(self):  # pylint: disable=no-self-use,missing-docstring
        return AlertProfile.policies

    def create(self, unimportant):
        raise NotImplementedError

    def delete(self, unimportant):
        raise NotImplementedError

    def describe(self, unimportant):
        raise NotImplementedError

    def update(self, unimportant):
        raise NotImplementedError
