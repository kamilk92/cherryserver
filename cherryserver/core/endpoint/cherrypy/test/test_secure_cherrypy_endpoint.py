from unittest import TestCase
from unittest.mock import patch

import cherrypy

from cherryserver.core.endpoint.cherrypy.secure_cherrypy_endpoint import SecureCherrypyEndpoint
from cherryserver.core.http.code import HttpCode


class DummySecureCherrypyEndpoint(SecureCherrypyEndpoint):
    def _validate_roles(self) -> bool:
        pass


class TestSecureCherrypyEndpoint(TestCase):
    @patch.object(DummySecureCherrypyEndpoint, "_validate_roles")
    @patch.object(DummySecureCherrypyEndpoint, "secure_get")
    @patch.object(DummySecureCherrypyEndpoint, "secure_post")
    @patch.object(DummySecureCherrypyEndpoint, "secure_put")
    def test_get_method_called_on_valid_roles(self, secure_put_mock, secure_post_mock, secure_get_mock, validate_roles_mock):
        validate_roles_mock.return_value = True
        expected_ret_value = "SECURE_GET_VALUE"
        secure_get_mock.return_value = expected_ret_value
        cherrypy_endpoint = DummySecureCherrypyEndpoint("", "", [])

        get_ret_value = cherrypy_endpoint.GET("arg1", named="named_arg_1")

        self.assertEqual(get_ret_value, expected_ret_value)
        validate_roles_mock.assert_called_once()
        secure_get_mock.assert_called_with("arg1", body=None, named="named_arg_1")

        expected_ret_value = "SECURE_POST_VALUE"
        secure_post_mock.return_value = expected_ret_value
        post_ret_value = cherrypy_endpoint.POST("arg2", named="named_arg_2")

        self.assertEqual(post_ret_value, expected_ret_value)
        self.assertEqual(validate_roles_mock.call_count, 2)
        secure_post_mock.assert_called_with("arg2", body=None, named="named_arg_2")

        expected_ret_value = "SECURE_PUT_VALUE"
        secure_put_mock.return_value = expected_ret_value
        put_ret_value = cherrypy_endpoint.PUT("arg3", body=None, named="named_arg_3")

        self.assertEqual(put_ret_value, expected_ret_value)
        self.assertEqual(validate_roles_mock.call_count, 3)
        secure_put_mock.assert_called_with("arg3", body=None, named="named_arg_3")

    @patch.object(DummySecureCherrypyEndpoint, "_validate_roles")
    def test_is_response_status_forbidden_when_roles_not_valid(self, validate_roles_mock):
        cherrypy_endpoint = DummySecureCherrypyEndpoint("", "", [])
        validate_roles_mock.return_value = False

        cherrypy_endpoint.GET()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)
        cherrypy.response.status = HttpCode.SUCCESS

        cherrypy_endpoint.POST()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)
        cherrypy.response.status = HttpCode.SUCCESS

        cherrypy_endpoint.PUT()
        self.assertEqual(cherrypy.response.status, HttpCode.FORBIDDEN)