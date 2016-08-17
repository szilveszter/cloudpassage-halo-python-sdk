"""CloudPassage init"""
import sys
from cloudpassage.alert_profile import AlertProfile  # noqa: F401
from cloudpassage.api_key_manager import ApiKeyManager  # noqa: F401
from cloudpassage.configuration_policy import ConfigurationPolicy  # noqa: F401
from cloudpassage.fim_policy import FimPolicy  # noqa: F401
from cloudpassage.fim_policy import FimBaseline  # noqa: F401
from cloudpassage.event import Event  # noqa: F401
from cloudpassage.exceptions import CloudPassageAuthentication  # noqa: F401
from cloudpassage.exceptions import CloudPassageAuthorization  # noqa: F401
from cloudpassage.exceptions import CloudPassageCollision  # noqa: F401
from cloudpassage.exceptions import CloudPassageGeneral  # noqa: F401
from cloudpassage.exceptions import CloudPassageInternalError  # noqa: F401
from cloudpassage.exceptions import CloudPassageResourceExistence  # noqa: F401
from cloudpassage.exceptions import CloudPassageValidation  # noqa: F401
from cloudpassage.firewall_policy import FirewallInterface  # noqa: F401
from cloudpassage.firewall_policy import FirewallPolicy  # noqa: F401
from cloudpassage.firewall_policy import FirewallRule  # noqa: F401
from cloudpassage.firewall_policy import FirewallService  # noqa: F401
from cloudpassage.firewall_policy import FirewallZone  # noqa: F401
from cloudpassage.halo import HaloSession  # noqa: F401
from cloudpassage.http_helper import HttpHelper  # noqa: F401
from cloudpassage.lids_policy import LidsPolicy  # noqa: F401
from cloudpassage.scan import CveException  # noqa: F401
from cloudpassage.scan import Scan  # noqa: F401
from cloudpassage.server import Server  # noqa: F401
from cloudpassage.server_group import ServerGroup  # noqa: F401
from cloudpassage.special_events_policy import SpecialEventsPolicy  # noqa: F401
from cloudpassage.system_announcement import SystemAnnouncement  # noqa: F401
import utility as init_util


target = "2.7.10"
installed = init_util.get_installed_python_version()
if init_util.verify_python_version(installed, target) is False:
    err_msg = "Please make sure your python veresion is at least %s" % target
    raise ImportError(err_msg)

__author__ = "CloudPassage"
__version__ = "0.99"
__license__ = "BSD"
