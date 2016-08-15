"""AlertProfile class"""

import cloudpassage.sanity as sanity
from cloudpassage.policy import Policy
from cloudpassage.http_helper import HttpHelper
import cloudpassage.utility as utility


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

    @classmethod
    def endpoint(cls):
        """Defines endpoint for API requests"""
        return "/v1/%s" % AlertProfile.policies

    @classmethod
    def policy_key(cls):
        return AlertProfile.policy

    @classmethod
    def pagination_key(cls):
        """Defines the pagination key for parsing paged results"""
        return AlertProfile.policies
