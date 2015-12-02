import fn
from policy import Policy
from http_helper import HttpHelper
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence


class ConfigurationPolicy(Policy):

    policy = "policy"
    policies = "policies"

    def endpoint(self):
        return("/v1/%s" % ConfigurationPolicy.policies)

    def pagination_key(self):
        return(ConfigurationPolicy.policies)

    def policy_key(self):
        return(ConfigurationPolicy.policy)
