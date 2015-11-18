from http_helper import HttpHelper
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence


class Scan:

    def __init__(self, session):
        self.session = session
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

        supported_scan_mapping = {"sca": "sca",
                                  "csm": "sca",
                                  "svm": "svm",
                                  "sva": "svm",
                                  "sam": "sam",
                                  "fim": "fim",
                                  "sv": "sv"}
        if scan_type not in supported_scan_mapping:
            exception_message = "Unsupported scan type: %s" % scan_type
            raise CloudPassageValidation(exception_message)
        else:
            scan_type_valid = supported_scan_mapping[scan_type]
            request_body = {"scan": {"module": scan_type_valid}}
            endpoint = "/v1/servers/%s/scans" % server_id
            try:
                request = HttpHelper(self.session)
                response = request.post(endpoint, request_body)
                command_info = response["command"]
                return(command_info)
            except CloudPassageResourceExistence as e:
                print e.msg
                raise CloudPassageResourceExistence(e.msg)
