import cherrypy
from cherryserver.core.endpoint.endpoint import Endpoint
from cherryserver.core.http.code import HttpCode
from cherryserver.core.server.cherrypy import error_handler
from cherryserver.core.server.cherrypy import request_logger

from cherryserver.core.server.cherrypy import cherrypy_util


class CherrypyEndpoint(Endpoint):
    @error_handler.application_error_to_http_500
    @request_logger.log_request_response
    def GET(self, *args, **kwargs):
        return self.get_method(*args, **kwargs)

    def get_method(self, *args, **kwargs):
        self._method_not_allowed()

    @error_handler.application_error_to_http_500
    @request_logger.log_request_response
    def POST(self, *args, **kwargs):
        return self.post_method(*args, **kwargs)

    def post_method(self, *args, **kwargs):
        self._method_not_allowed()

    @error_handler.application_error_to_http_500
    @request_logger.log_request_response
    def PUT(self, *args, **kwargs):
        return self.put_method(*args, **kwargs)

    def put_method(self, *args, **kwargs):
        self._method_not_allowed()

    def _method_not_allowed(self):
        cherrypy.response.status = HttpCode.METHOD_NOT_ALLOWED

    def _to_json(self, d: dict):
        return cherrypy_util.to_json(d)
