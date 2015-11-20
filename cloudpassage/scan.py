from http_helper import HttpHelper
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence


class Scan:

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

        server_id    -- Server ID (not name)
        scan_type    -- Scan type to initiate.

        Valid scan types:
          sca  - Configuration scan
          csm  - Configuration scan (same as sca)
          svm  - Software vulnerability scan
          sva  - Software vulnerability scan (same as svm)
          sam  - Server access management scan
          fim  - File integrity monitoring scan
          sv   - Agent self-verifiation scan

        Returns the metadata from the command issued,
        in a dict.
        Failure throws an exception.
        """

        if self.scan_type_supported(scan_type) is False:
            exception_message = "Unsupported scan type: %s" % scan_type
            raise CloudPassageValidation(exception_message)
        else:
            scan_type_normalized = self.supported_scans[scan_type]
            request_body = {"scan": {"module": scan_type_normalized}}
            endpoint = "/v1/servers/%s/scans" % server_id
            try:
                request = HttpHelper(self.session)
                response = request.post(endpoint, request_body)
                command_info = response["command"]
                return(command_info)
            except CloudPassageResourceExistence as e:
                raise CloudPassageResourceExistence(e.msg)

    def last_scan_results(self, server_id, scan_type):
        """Get the results of scan_type performed on server_id.

        Valid scan types:
          sca  - Configuration scan
          csm  - Configuration scan (same as sca)
          svm  - Software vulnerability scan
          sva  - Software vulnerability scan (same as svm)
          sam  - Server access management scan
          fim  - File integrity monitoring scan
        """

        if self.scan_history_supported(scan_type) is False:
            exception_message = "Unsupported scan type: %s" % scan_type
            raise CloudPassageValidation(exception_message)
        else:
            scan_type_normalized = self.supported_scans[scan_type]
            endpoint = "/v1/servers/%s/%s" % (server_id, scan_type_normalized)
            try:
                request = HttpHelper(self.session)
                response = request.get(endpoint)
                return(response)
            except CloudPassageResourceExistence:
                raise CloudPassageResourceExistence(endpoint)

    def scan_history(self, **kwargs):
        """Get a list of historical scans, pertinent to the criteria
        defined in kwargs, detailed below.

        server_id  -- ID of server
        module     -- sca, fim, svm, sam (accepts single value or list)
        status     -- queued, pending, running, completed_clean,
                      completed_with_errors, failed (accepts single value
                      or list)
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
        """Get FIM findings details by scan and findings ID"""

        endpoint = "/v1/scans/%s/findings/%s" % (scan_id, findings_id)
        request = HttpHelper(self.session)
        response = request.get(endpoint)
        return(response)

    def scan_details(self, scan_id):
        """Get detailed scan information"""

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
