import ast
from unittest import TestCase
from unittest.mock import Mock

import cherrypy
from cherrypy import HTTPError

from cherryserver.core.exception.error import ServerError
from cherryserver.core.http.code import HttpCode
from cherryserver.core.server.cherrypy.error_handler import application_error_to_http_500


class TestErrorHandler(TestCase):
    def test_is_handled_cherrypy_http_error(self):
        decorated_func_mock = Mock()
        expected_status = HttpCode.NOT_FOUND
        expected_msg = "NOT FOUND MESSAGE"
        decorated_func_mock.side_effect = HTTPError(expected_status, expected_msg)

        response = application_error_to_http_500(decorated_func_mock)()

        self.assertIsNotNone(response)
        rsp_dict = ast.literal_eval(response.decode("utf-8"))
        decorated_func_mock.assert_called_once()
        self.assertEqual(cherrypy.response.status, expected_status)
        self.assertEqual(rsp_dict["service_code"], 0)
        self.assertEqual(rsp_dict["message"], expected_msg)

    def test_is_handle_server_error(self):
        decorated_func_mock = Mock()
        expected_status = HttpCode.NOT_FOUND
        expected_service_code = 10
        expected_msg = "NOT FOUND MESSAGE"
        decorated_func_mock.side_effect = ServerError(expected_status, expected_service_code, expected_msg)

        response = application_error_to_http_500(decorated_func_mock)()

        self.assertIsNotNone(response)
        rsp_dict = ast.literal_eval(response.decode("utf-8"))
        decorated_func_mock.assert_called_once()
        self.assertEqual(cherrypy.response.status, expected_status)
        self.assertEqual(rsp_dict["service_code"], expected_service_code)
        self.assertEqual(rsp_dict["message"], expected_msg)

    def test_is_handle_unexpected_exception(self):
        decorated_func_mock = Mock()
        expected_status = HttpCode.INTERNAL_ERROR
        expected_service_code = 0
        expected_msg = "Unexpected application error"
        decorated_func_mock.side_effect = Exception()

        response = application_error_to_http_500(decorated_func_mock)()

        self.assertIsNotNone(response)
        rsp_dict = ast.literal_eval(response.decode("utf-8"))
        decorated_func_mock.assert_called_once()
        self.assertEqual(cherrypy.response.status, expected_status)
        self.assertEqual(rsp_dict["service_code"], expected_service_code)
        self.assertEqual(rsp_dict["message"], expected_msg)
