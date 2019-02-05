class CherryServerError(Exception):
    def __init__(self, message):
        super().__init__(message)


class ServerError(CherryServerError):
    def __init__(self, response_hhtp_code, service_code, msg):
        self.response_http_code = response_hhtp_code
        self.service_code = service_code
        self.msg = msg

    @property
    def response_http_code(self):
        return self._response_code

    @response_http_code.setter
    def response_http_code(self, response_code):
        self._response_code = response_code

    @property
    def service_code(self):
        return self._service_code

    @service_code.setter
    def service_code(self, service_code):
        self._service_code = service_code

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg


class ServerConfigurationError(CherryServerError):
    pass
