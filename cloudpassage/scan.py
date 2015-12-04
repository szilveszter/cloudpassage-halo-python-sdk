from exceptions import CloudPassageValidation
from http_helper import HttpHelper
from policy import Policy


class Scan:
    """Initializing the Scan class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    def __init__(self, session):
        self.session = session
        self.supported_scans = {"sca": "sca",
                                "csm": "sca",
                                "svm": "svm",
                                "sva": "svm",
                                "sam": "sam",
                                "fim": "fim",
                                "sv": "sv"}
        self.supported_historical_scans = {"sca": "sca",
                                           "csm": "sca",
                                           "svm": "svm",
                                           "sva": "svm",
                                           "sam": "sam",
                                           "fim": "fim"}
        self.supported_scan_status = ["queued",
                                      "pending",
                                      "running",
                                      "completed_clean",
                                      "completed_with_errors",
                                      "failed"]
        return None

    def initiate_scan(self, server_id, scan_type):
        """Initiate a scan on a specific server.

        Args:
            server_id (str): ID of server to be scanned
            scan_type (str): Type of scan to be run.

          Valid scan types:
            sca  - Configuration scan
            csm  - Configuration scan (same as sca)
            svm  - Software vulnerability scan
            sva  - Software vulnerability scan (same as svm)
            sam  - Server access management scan
            fim  - File integrity monitoring scan
            sv   - Agent self-verifiation scan

        Returns:
            dict: Dictionary describing command created as a result of this \
            call
            Failure throws an exception.
        """

        if self.scan_type_supported(scan_type) is False:
            exception_message = "Unsupported scan type: %s" % scan_type
            raise CloudPassageValidation(exception_message)
        else:
            scan_type_normalized = self.supported_scans[scan_type]
            request_body = {"scan": {"module": scan_type_normalized}}
            endpoint = "/v1/servers/%s/scans" % server_id
            request = HttpHelper(self.session)
            response = request.post(endpoint, request_body)
            command_info = response["command"]
            return(command_info)

    def last_scan_results(self, server_id, scan_type):
        """Get the results of scan_type performed on server_id.

        Args:
            server_id (str): ID of server
            scan_type (str): Type of scan to filter results for

        Valid scan types:
          sca  - Configuration scan
          csm  - Configuration scan (same as sca)
          svm  - Software vulnerability scan
          sva  - Software vulnerability scan (same as svm)
          sam  - Server access management scan
          fim  - File integrity monitoring scan

        Returns:
            dict: Dictionary object describing last scan results

        """

        if self.scan_history_supported(scan_type) is False:
            exception_message = "Unsupported scan type: %s" % scan_type
            raise CloudPassageValidation(exception_message)
        else:
            scan_type_normalized = self.supported_scans[scan_type]
            endpoint = "/v1/servers/%s/%s" % (server_id, scan_type_normalized)
            request = HttpHelper(self.session)
            response = request.get(endpoint)
            return(response)

    def scan_history(self, **kwargs):
        """Get a list of historical scans.

        Args:
            server_id (str): Id of server
            module (str or list): sca, fim, svm, sam
            status (str or list): queued, pending, running, completed_clean,
            completed_with_errors, failed

        Returns:
            list: List of scan objects
        """

        max_pages = 20
        url_params = {}
        if "server_id" in kwargs:
            url_params["server_id"] = kwargs["server_id"]
        if "module" in kwargs:
            url_params["module"] = self.verify_and_build_module_params(
                                   kwargs["module"])
        if "status" in kwargs:
            url_params["status"] = self.verify_and_build_status_params(
                                   kwargs["status"])
        if "max_pages" in kwargs:
            max_pages = kwargs["max_pages"]
        endpoint = "/v1/scans"
        key = "scans"
        request = HttpHelper(self.session)
        if url_params != {}:
            response = request.get_paginated(endpoint, key, max_pages,
                                             params=url_params)
        else:
            response = request.get_paginated(endpoint, key, max_pages)
        return(response)

    def findings(self, scan_id, findings_id):
        """Get FIM findings details by scan and findings ID

        Args:
            scan_id (str): ID of scan_id
            findings_id (str): ID of findings to retrieve

        Returns:
            dict: Dictionary object descrbing findings

        """

        endpoint = "/v1/scans/%s/findings/%s" % (scan_id, findings_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        return(response)

    def scan_details(self, scan_id):
        """Get detailed scan information

        Args:
            scan_id (str): ID of scan

        Returns:
            dict: Dictionary object describing scan details

        """

        endpoint = "/v1/scans/%s" % scan_id
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        report = response["scan"]
        return(report)

    def scan_status_supported(self, scan_status):
        if scan_status in self.supported_scan_status:
            return True
        else:
            return False

    def scan_type_supported(self, scan_type):
        if scan_type in self.supported_scans:
            return True
        else:
            return False

    def scan_history_supported(self, scan_type):
        if scan_type in self.supported_historical_scans:
            return True
        else:
            return False

    def verify_and_build_status_params(self, status_raw):
        if type(status_raw) is list:
            for status in status_raw:
                if self.scan_status_supported(status) is not True:
                    exception_message = "%s is not supported" % status
                    raise CloudPassageValidation(exception_message)
        else:
            if self.scan_status_supported(status_raw) is False:
                error_message = "Unsupported status: %s" % status_raw
                raise CloudPassageValidation(error_message)
        return(status_raw)

    def verify_and_build_module_params(self, module_raw):
        if type(module_raw) is list:
            for module in module_raw:
                if self.scan_type_supported(module) is not True:
                    exception_message = "%s is not supported" % module
                    raise CloudPassageValidation(exception_message)
        else:
            if self.scan_type_supported(module_raw) is False:
                error_message = "Unsupported module: %s" % module_raw
                raise CloudPassageValidation(error_message)
        return(module_raw)


class CveException(Policy):
    """Initializing the CveException class:

    Args:
        session (:class:`cloudpassage.HaloSession`): \
        This will define how you interact \
        with the Halo API, including proxy settings and API keys \
        used for authentication.

    """

    policy = "cve_exception"
    policies = "cve_exceptions"

    def endpoint(self):
        return("/v1/%s" % CveException.policies)

    def pagination_key(self):
        return(CveException.policies)

    def policy_key(self):
        return(CveException.policy)

    def create(self, unimportant):
        raise NotImplementedError

    def delete(self, unimportant):
        raise NotImplementedError

    def update(self, unimportant):
        raise NotImplementedError
