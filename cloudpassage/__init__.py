"""CloudPassage init"""
import sys
from cloudpassage.alert_profile import AlertProfile
from cloudpassage.api_key_manager import ApiKeyManager
from cloudpassage.configuration_policy import ConfigurationPolicy
from cloudpassage.fim_policy import FimPolicy
from cloudpassage.fim_policy import FimBaseline
from cloudpassage.event import Event
from cloudpassage.exceptions import CloudPassageAuthentication
from cloudpassage.exceptions import CloudPassageAuthorization
from cloudpassage.exceptions import CloudPassageCollision
from cloudpassage.exceptions import CloudPassageGeneral
from cloudpassage.exceptions import CloudPassageInternalError
from cloudpassage.exceptions import CloudPassageResourceExistence
from cloudpassage.exceptions import CloudPassageValidation
from cloudpassage.firewall_policy import FirewallInterface
from cloudpassage.firewall_policy import FirewallPolicy
from cloudpassage.firewall_policy import FirewallRule
from cloudpassage.firewall_policy import FirewallService
from cloudpassage.firewall_policy import FirewallZone
from cloudpassage.halo import HaloSession
from cloudpassage.http_helper import HttpHelper
from cloudpassage.lids_policy import LidsPolicy
from cloudpassage.scan import CveException
from cloudpassage.scan import Scan
from cloudpassage.server import Server
from cloudpassage.server_group import ServerGroup
from cloudpassage.special_events_policy import SpecialEventsPolicy
from cloudpassage.system_announcement import SystemAnnouncement


if sys.version_info < (2, 7, 10):
    raise ImportError("Please make sure your python veresion is \
                      greater than 2.7.10")


__author__ = "CloudPassage"
__version__ = "0.99"
__license__ = "BSD"
