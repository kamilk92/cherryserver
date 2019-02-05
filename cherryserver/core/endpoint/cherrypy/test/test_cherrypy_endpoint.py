import json
from unittest import TestCase, mock

import cherrypy

from cherryserver.core.endpoint.cherrypy.cherrypy_endpoint import CherrypyEndpoint
from cherryserver.core.http.code import HttpCode
from cherryserver.core.http.content_type import ContentType
from cherryserver.core.http.header_element import HeaderElement


class DummyCherrypyEndpoint(CherrypyEndpoint):
    def get_method(self, *args, **kwargs):
        return "GET"

    def post_method(self, *args, **kwargs):
        return "POST"

    def put_method(self, *args, **kwargs):
        return "PUT"


class TestCherrypyEndpoint(TestCase):
    def setUp(self):
        self.cherrypy_endpoint = DummyCherrypyEndpoint("/dummy", "dummy_endpoint")

    @mock.patch.object(DummyCherrypyEndpoint, "get_method")
    def test_get_method(self, get_method_mock):
        self.cherrypy_endpoint.GET("get_arg", named="get_arg_named")
        get_method_mock.assert_called_once()
        get_method_mock.assert_called_with("get_arg", body=None, named="get_arg_named")

    @mock.patch.object(DummyCherrypyEndpoint, "post_method")
    def test_post_method(self, post_method_mock):
        self.cherrypy_endpoint.POST("post_arg", named="post_arg_named")
        post_method_mock.assert_called_once()
        post_method_mock.assert_called_with("post_arg", body=None, named="post_arg_named")

    @mock.patch.object(DummyCherrypyEndpoint, "put_method")
    def test_put_method(self, put_method_mock):
        self.cherrypy_endpoint.PUT("put_arg", named="put_arg_named")
        put_method_mock.assert_called_once()
        put_method_mock.assert_called_with("put_arg", body=None, named="put_arg_named")

    def test_is_cherrypy_jsonify(self):
        json_rsp = {"key": "value", "key_1": "value_1"}
        jsonified = self.cherrypy_endpoint._to_json(json_rsp)
        self.assertEqual(jsonified, json.dumps(json_rsp).encode("utf-8"))
        self.assertEqual(cherrypy.response.headers.get(HeaderElement.CONTENT_TYPE.value),
                         ContentType.APPLICATION_JSON.value)

    def test_is_method_not_allowed_set_405_http_code(self):
        cherrypy_enpoint = CherrypyEndpoint("", "")
        self.assertNotEqual(cherrypy.response.status, HttpCode.METHOD_NOT_ALLOWED)

        cherrypy.response.status = HttpCode.SUCCESS
        cherrypy_enpoint.PUT()
        self.assertEqual(cherrypy.response.status, HttpCode.METHOD_NOT_ALLOWED)

        cherrypy.response.status = HttpCode.SUCCESS
        cherrypy_enpoint.POST()
        self.assertEqual(cherrypy.response.status, HttpCode.METHOD_NOT_ALLOWED)

        cherrypy.response.status = HttpCode.SUCCESS
        cherrypy_enpoint.GET()
        self.assertEqual(cherrypy.response.status, HttpCode.METHOD_NOT_ALLOWED)
