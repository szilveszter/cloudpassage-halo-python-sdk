from http_helper import HttpHelper


class Server:

    def __init__(self, session):
        self.session = session
        return None

    def retire(self, server_id):
        endpoint = "/v1/servers/%s" % server_id
        body = {"server":
                {"retire": True}}
        request = HttpHelper(self.session)
        try:
            response = request.put(endpoint, body)
        except put.CloudPassageAuthorization as e:
            raise CloudPassageAuthorization(e.msg)
        except put.CloudPassageValdiation as e:
            raise CloudPassageValidation(e.msg)
        return True
