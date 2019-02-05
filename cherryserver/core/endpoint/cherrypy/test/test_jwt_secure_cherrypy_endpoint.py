from unittest import mock

import cherrypy

from cherryserver.core.endpoint.cherrypy.jwt_secure_cherrypy_endpoint import JWTSecureCherrypyEndpoint
from cherryserver.core.endpoint.security.test.abstract_test_jwt_secure_endpoint import AbstractTestJWTSecureEndpoint
from cherryserver.core.http.code import HttpCode


class DummyJWTSecureCherrypyEndpoint(JWTSecureCherrypyEndpoint):
    pass


class TestJWTSecureCherrypyEndpoint(AbstractTestJWTSecureEndpoint):
    VALID_ROLES = ["ROLE_USER", "ROLE_ADMIN"]

    @mock.patch("cherrypy.request.headers.get")
    @mock.patch.object(DummyJWTSecureCherrypyEndpoint, "secure_get")
    @mock.patch.object(DummyJWTSecureCherrypyEndpoint, "secure_post")
    @mock.patch.object(DummyJWTSecureCherrypyEndpoint, "secure_put")
    def is_method_invoked_when_roles_valid(self, secure_put_mock, secure_post_mock, secure_get_mock,
                                           cherrypy_get_headers_mock):
        cherrypy_get_headers_mock.side_effect = self._get_roles_from_request_header(
            TestJWTSecureCherrypyEndpoint.VALID_ROLES[0])
        jwt_secure_endpoint = DummyJWTSecureCherrypyEndpoint("", "", TestJWTSecureCherrypyEndpoint.VALID_ROLES)

        jwt_secure_endpoint.get_method("arg_1", named="named_arg_1")

        secure_get_mock.assert_called_with("arg_1", named="named_arg_1")
        cherrypy_get_headers_mock.assert_called_once()

        jwt_secure_endpoint.post_method("arg_2", named="named_arg_2")

        secure_post_mock.assert_called_with("arg_2", named="named_arg_2")
        self.assertEqual(cherrypy_get_headers_mock.call_count, 2)

        jwt_secure_endpoint.put_method("arg_3", named="named_arg_3")

        secure_put_mock.assert_called_with("arg_3", named="named_arg_3")
        self.assertEqual(cherrypy_get_headers_mock.call_count, 3)

    @mock.patch("cherrypy.request.headers.get")
    def test_is_set_forbidden_when_roles_not_valid(self, cherrypy_get_headers_mock):
        cherrypy_get_headers_mock.side_effect = self._get_roles_from_request_header("NOT_VALID_ROLE")
        jwt_secure_endpoint = DummyJWTSecureCherrypyEndpoint("", "", TestJWTSecureCherrypyEndpoint.VALID_ROLES)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.get_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.post_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.put_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)

    def test_is_set_forbidden_when_roles_missing(self):
        jwt_secure_endpoint = DummyJWTSecureCherrypyEndpoint("", "", TestJWTSecureCherrypyEndpoint.VALID_ROLES)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.get_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.post_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)

        cherrypy.response.status = HttpCode.SUCCESS
        jwt_secure_endpoint.put_method()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)
