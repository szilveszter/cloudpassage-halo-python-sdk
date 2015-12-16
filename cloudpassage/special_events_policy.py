'''docstring'''


from cloudpassage.policy import Policy


class SpecialEventsPolicy(Policy):
    """Initializing the SpecialEventsPolicy class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "special_events_policy"
    policies = "special_events_policies"

    def endpoint(self):  # pylint: disable=no-self-use,missing-docstring
        return "/v1/%s" % SpecialEventsPolicy.policies

    def pagination_key(self):  # pylint: disable=no-self-use,missing-docstring
        return SpecialEventsPolicy.policies

    def create(self, unimportant):
        raise NotImplementedError

    def delete(self, unimportant):
        raise NotImplementedError

    def describe(self, unimportant):
        raise NotImplementedError

    def update(self, unimportant):
        raise NotImplementedError
