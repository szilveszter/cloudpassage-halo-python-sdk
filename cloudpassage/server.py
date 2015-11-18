from http_helper import HttpHelper
from exceptions import CloudPassageAuthorization
from exceptions import CloudPassageValidation
from exceptions import CloudPassageResourceExistence


class Server:

    def __init__(self, session):
        self.session = session
        return None

    def retire(self, server_id):
        """This method retires a server"""

        endpoint = "/v1/servers/%s" % server_id
        body = {"server":
                {"retire": True}}
        request = HttpHelper(self.session)
        try:
            response = request.put(endpoint, body)
        except request.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        except request.CloudPassageValidation as e:
            raise CloudPassageValidation(e.msg)
        except request.CloudPassageResourceExistence:
            raise CloudPassageResourceExistence(endpoint)
        return True

    def command_details(self, server_id, command_id):
        """This method retrieves the details and status of a server command.

        Command status is returned as a dictionary object:
        {"name": "",
         "status: "",
         "created_at": "",
         "updated_at": "",
         "result": ""}

         For server account creation and server account password resets,
         the password will be contained in the result field, as a dictionary:
         {"name": "",
          "status: "",
          "created_at": "",
          "updated_at": "",
          "result": {"password": ""}
          }
        """

        endpoint = "/v1/servers/%s/commands/%s" % (server_id, command_id)
        request = HttpHelper(self.session)
        try:
            response = request.get(endpoint)
            command_status = response["command"]
            return(command_status)
        except CloudPassageResourceExistence as e:
            raise CloudPassageResourceExistence(endpoint)
