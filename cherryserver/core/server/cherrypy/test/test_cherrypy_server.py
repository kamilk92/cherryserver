from unittest import TestCase, mock

from cherryserver.core.endpoint.endpoint import Endpoint
from cherryserver.core.exception.error import ServerConfigurationError
from cherryserver.core.server.cherrypy.cherrypy_server import CherrypyServer
from cherryserver.core.server.cherrypy.config_key import CherrypyConfigKey
from cherryserver.util import test_util


class TestCherrypyServer(TestCase):
    @mock.patch("cherrypy.engine.start")
    @mock.patch("cherrypy.engine.block")
    def test_is_server_starting(self, block_func_mock, start_func_mock):
        cherrypy_server = CherrypyServer()
        cherrypy_server.start()
        block_func_mock.assert_called_once()
        start_func_mock.assert_called_once()

    @mock.patch("cherrypy.engine.start")
    @mock.patch("cherrypy.engine.block")
    @mock.patch("cherrypy.config.update")
    def test_is_server_starting_with_ssl(self, update_conf_func_mock, block_func_mock, start_func_mock):
        server_config = CherrypyServer.CherrypyServerConfig("127.0.0.1", "8080", ssl_cert="cert.pem",
                                                            ssl_private_key="key.pem", ssl_cert_chain="chain.pem",
                                                            ssl_module="sslmodule")
        cherrypy_server = CherrypyServer(server_config)

        cherrypy_server.start()

        start_func_mock.assert_called_once()
        block_func_mock.assert_called_once()
        update_conf_func_mock.assert_called_once()

        called_config = test_util.get_mock_call_arg(update_conf_func_mock, 0, 0)
        self.assertTrue(isinstance(called_config, dict))
        self.assertEqual(called_config[CherrypyConfigKey.SERVER_SSL_CERT.value], server_config.ssl_cert)
        self.assertEqual(called_config[CherrypyConfigKey.SERVER_SSL_PRIVATE_KEY.value], server_config.ssl_private_key)
        self.assertEqual(called_config[CherrypyConfigKey.SERVER_SSL_CERT_CHAIN.value], server_config.ssl_cert_chain)
        self.assertEqual(called_config[CherrypyConfigKey.SERVER_SSL_MODULE.value], server_config.ssl_module)

    @mock.patch("cherrypy.engine.start")
    @mock.patch("cherrypy.engine.block")
    @mock.patch("cherrypy.config.update")
    def test_is_server_raise_exception_when_ssl_broken(self, update_conf_func_mock, block_func_mock, start_func_mock):
        server_config = CherrypyServer.CherrypyServerConfig("127.0.0.1", "8080", ssl_private_key="key.pem",
                                                            ssl_cert_chain="chain.pem", ssl_module="sslmodule")
        cherrypy_server = CherrypyServer(server_config)
        self.__is_server_raise_exception_on_start(cherrypy_server, ServerConfigurationError)
        update_conf_func_mock.assert_not_called()
        block_func_mock.assert_not_called()
        start_func_mock.assert_not_called()

        cherrypy_server._config = CherrypyServer.CherrypyServerConfig("127.0.0.1", "8080", ssl_cert="cert.pem",
                                                                      ssl_cert_chain="chain.pem", ssl_module="ssl")
        self.__is_server_raise_exception_on_start(cherrypy_server, ServerConfigurationError)
        update_conf_func_mock.assert_not_called()
        block_func_mock.assert_not_called()
        start_func_mock.assert_not_called()

        cherrypy_server._config = CherrypyServer.CherrypyServerConfig("127.0.0.1", "8080", ssl_cert="cert.pem",
                                                                      ssl_private_key="key.pem", ssl_module="ssl")
        self.__is_server_raise_exception_on_start(cherrypy_server, ServerConfigurationError)
        update_conf_func_mock.assert_not_called()
        block_func_mock.assert_not_called()
        start_func_mock.assert_not_called()

    @mock.patch("cherrypy.tree.mount")
    def test_is_server_registering_endpoint(self, mount_func_mock):
        endpoint_path = "/endpoint/path"
        dummy_endpoint_conf = {
            "key_1": "value_1",
            "key_2": "value_2"
        }
        dummy_endpoint = type("", (Endpoint, object), {
            "path": endpoint_path,
            "conf": dummy_endpoint_conf
        })
        cherrypy_server = CherrypyServer()

        cherrypy_server.register_endpoint(dummy_endpoint)

        mount_func_mock.assert_called_once()
        self.assertEqual(dummy_endpoint, test_util.get_mock_call_arg(mount_func_mock, 0, 0))
        self.assertEqual(endpoint_path, test_util.get_mock_call_arg(mount_func_mock, 0, 1))
        registered_endpoint_conf = test_util.get_mock_call_arg(mount_func_mock, 0, 2)
        self.assertTrue("key_1" in registered_endpoint_conf)
        self.assertEqual(registered_endpoint_conf.get("key_1"), dummy_endpoint_conf.get("key_1"))
        self.assertTrue("key_2" in registered_endpoint_conf)
        self.assertEqual(registered_endpoint_conf.get("key_2"), dummy_endpoint_conf.get("key_2"))

    @mock.patch("cherrypy.tree.mount")
    def is_server_registering_endpoint_with_context_path(self, mount_func_mock):
        context_path = "/appcontext"
        endpoint_path = "/endpoint"
        server_config = CherrypyServer.CherrypyServerConfig("127.0.0.1", port="8080", context_path=context_path)
        endpoint = type("", (Endpoint, object), {
            "path": endpoint_path,
            "conf": {}
        })
        cherrypy_server = CherrypyServer(server_config)

        cherrypy_server.register_endpoint(endpoint)

        mount_func_mock.assert_called_once()
        self.assertEqual(endpoint, test_util.get_mock_call_arg(mount_func_mock, 0, 0))
        self.assertEqual("".join([context_path, endpoint_path]),
                               test_util.get_mock_call_arg(mount_func_mock, 0, 1))

    def __is_server_raise_exception_on_start(self, server, expected_exception):
        with self.assertRaises(expected_exception) as context:
            server.start()
