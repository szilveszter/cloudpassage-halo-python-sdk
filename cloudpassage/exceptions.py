class CloudPassageAuthentication(Exception):
    """Exception related to authentication.

    error_msg  -- Message describing error
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageAuthorization(Exception):
    """Exception related to authorization.

    Oftentimes related to the scope of the API credentials
    error_msg  -- Message describing the error
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageValidation(Exception):
    """Exception related to request validation.

    Typically related to malformed json.
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageCollision(Exception):
    """Exception indicates a resource collision.

    This is thrown when attempting to create a resource
    which already exists.
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageInternalError(Exception):
    """This exception indicates an error in the Analytics Engine.

    This is thrown when a HTTP response code of 500 is detected.
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageResourceExistence(Exception):
    """This exception indicates that you're trying to access a
       resource that doesn't exist.

    This is oftentimes thrown in response to a 404 from the API.
    """

    def __init__(self, error_msg):
        self.msg = error_msg


class CloudPassageGeneral(Exception):
    """This is thrown when a more specific exception type is unavailable.

    The msg attribute should have plenty of information on what went wrong.
    """

    def __init__(self, error_msg):
        self.msg = error_msg
