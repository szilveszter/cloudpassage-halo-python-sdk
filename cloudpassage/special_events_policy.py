from http_helper import HttpHelper
from policy import Policy
import urlparse


class SpecialEventsPolicy(Policy):

    policy = "special_events_policy"
    policies = "special_events_policies"

    def endpoint(self):
        return("/v1/%s" % SpecialEventsPolicy.policies)

    def pagination_key(self):
        return(SpecialEventsPolicy.policies)
