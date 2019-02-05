from unittest import mock

import cherrypy

from cherryserver.core.endpoint.security.jwt_secure_endpoint import JWTSecureEndpoint
from cherryserver.core.endpoint.security.test.abstract_test_jwt_secure_endpoint import AbstractTestJWTSecureEndpoint
from cherryserver.core.http.header_element import HeaderElement


class DummyJWTSecureEndpoint(JWTSecureEndpoint):
    def _roles_not_valid_response(self):
        pass

    def _method_not_allowed(self):
        pass


class TestJWTSecureEndpoint(AbstractTestJWTSecureEndpoint):
    VALID_ROLES = ["USER_ROLE", "ADMIN_ROLE"]

    @mock.patch.object(DummyJWTSecureEndpoint, "secure_get")
    @mock.patch.object(DummyJWTSecureEndpoint, "secure_post")
    @mock.patch.object(DummyJWTSecureEndpoint, "secure_put")
    def test_is_method_invoked_when_roles_valid(self, secure_put_mock, secure_post_mock, secure_get_mock):
        cherrypy.request.headers = {
            HeaderElement.AUTHORIZATION.value: TestJWTSecureEndpoint.VALID_ROLES[0]
        }

        jwt_secure_endpoint = DummyJWTSecureEndpoint("", "", TestJWTSecureEndpoint.VALID_ROLES)

        jwt_secure_endpoint.get_method("arg_1", named="named_arg_1")
        secure_get_mock.assert_called_with("arg_1", named="named_arg_1")

        jwt_secure_endpoint.post_method("arg_2", named="named_arg_2")
        secure_post_mock.assert_called_with("arg_2", named="named_arg_2")

        jwt_secure_endpoint.put_method("arg_3", named="named_arg_3")
        secure_put_mock.assert_called_with("arg_3", named="named_arg_3")

    @mock.patch.object(DummyJWTSecureEndpoint, "_roles_not_valid_response")
    def test_is_return_not_valid_response_when_missing_roles(self, roles_not_valid_response_mock):
        cherrypy.request.headers = {
            HeaderElement.AUTHORIZATION.value: None
        }
        jwt_secure_endpoint = DummyJWTSecureEndpoint("", "", TestJWTSecureEndpoint.VALID_ROLES)
        not_valid_rsp = "NOT_VALID_FLAG"
        roles_not_valid_response_mock.return_value = not_valid_rsp

        self.assertEqual(jwt_secure_endpoint.get_method(), not_valid_rsp)
        roles_not_valid_response_mock.assert_called_once()

        self.assertEqual(jwt_secure_endpoint.post_method(), not_valid_rsp)
        self.assertEqual(roles_not_valid_response_mock.call_count, 2)

        self.assertEqual(jwt_secure_endpoint.put_method(), not_valid_rsp)
        self.assertEqual(roles_not_valid_response_mock.call_count, 3)

    @mock.patch.object(DummyJWTSecureEndpoint, "_roles_not_valid_response")
    def test_is_return_not_valid_response_when_role_not_valid(self, roles_not_valid_rsp_mock):
        cherrypy.request.headers = {
            HeaderElement.AUTHORIZATION.value: "NOT_VALID_ROLE"
        }
        not_valid_rsp = "NOT_VALID_FLAG"
        roles_not_valid_rsp_mock.return_value = not_valid_rsp

        jwt_secure_endpoint = DummyJWTSecureEndpoint("", "", TestJWTSecureEndpoint.VALID_ROLES)

        self.assertEqual(jwt_secure_endpoint.get_method(), not_valid_rsp)
        roles_not_valid_rsp_mock.assert_called_once()

        self.assertEqual(jwt_secure_endpoint.post_method(), not_valid_rsp)
        self.assertEqual(roles_not_valid_rsp_mock.call_count, 2)

        self.assertEqual(jwt_secure_endpoint.put_method(), not_valid_rsp)
        self.assertEqual(roles_not_valid_rsp_mock.call_count, 3)
