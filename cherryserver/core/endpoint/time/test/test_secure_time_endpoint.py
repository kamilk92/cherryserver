import ast
from unittest import TestCase, mock

import cherrypy

from cherryserver.core.endpoint.time.secure_time_endpoint import SecureTimeEndpoint
from cherryserver.core.http.code import HttpCode
from cherryserver.core.http.header_element import HeaderElement


class TestSecureTimeEndpoint(TestCase):
    VALID_ROLES = ["USER", "ADMIN"]

    def setUp(self):
        self.endpoint = SecureTimeEndpoint(TestSecureTimeEndpoint.VALID_ROLES)

    def test_is_endpoint_answer(self):
        cherrypy.request.headers = {
            HeaderElement.AUTHORIZATION.value: TestSecureTimeEndpoint.VALID_ROLES[0]
        }

        with mock.patch.object(self.endpoint, "_validate_roles", wraps=self.endpoint._validate_roles) as validate_roles_mock:
            rsp = self.endpoint.POST()
            validate_roles_mock.assert_called_once()
            self.assertIsNotNone(rsp)
            rsp_as_json = ast.literal_eval(rsp.decode("utf-8"))
            self.assertIsNotNone(rsp_as_json["time"])

    def test_is_endpoint_raise_exception_when_roles_are_missing_in_request(self):
        cherrypy.request.headers = {
            HeaderElement.AUTHORIZATION.value: None
        }

        with mock.patch.object(self.endpoint, "_validate_roles", wraps=self.endpoint._validate_roles) as validate_roles_mock:
            rsp = self.endpoint.POST()
            validate_roles_mock.assert_called_once()
            self.assertIsNone(rsp)
            self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)
