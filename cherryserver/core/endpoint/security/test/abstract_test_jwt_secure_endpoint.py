from unittest import TestCase

import cherrypy

from cherryserver.core.http.header_element import HeaderElement


class AbstractTestJWTSecureEndpoint(TestCase):
    def _get_roles_from_request_header(self, role_in_request_header: str):
        return lambda header_element, default_value: \
            role_in_request_header if header_element == HeaderElement.AUTHORIZATION.value else \
                cherrypy.request.headers.get(header_element, default_value)