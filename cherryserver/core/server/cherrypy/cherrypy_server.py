import logging

import cherrypy
from cherrypy import engine, tree

import cherryserver
from cherryserver.core.exception.error import ServerConfigurationError
from cherryserver.core.server.cherrypy.config_key import CherrypyConfigKey
from cherryserver.core.server.server import Server


class CherrypyServer(Server):
    DEFAULT_ADDR = "127.0.0.1"
    DEFAULT_PORT = 8080

    class CherrypyServerConfig(Server.ServerConfig):
        def __init__(self, addr: str, port: int, context_path=None, ssl_cert=None, ssl_private_key=None,
                     ssl_cert_chain=None, ssl_module="builtin"):
            super().__init__(addr, port, context_path, ssl_cert, ssl_private_key, ssl_cert_chain)
            self.ssl_module = ssl_module

        @property
        def ssl_module(self):
            return self._ssl_module

        @ssl_module.setter
        def ssl_module(self, ssl_module):
            self._ssl_module = ssl_module

        def as_dict(self):
            return {
                CherrypyConfigKey.SERVER_ADDR.value: self.addr,
                CherrypyConfigKey.SERVER_PORT.value: self.port
            }

    def __init__(self, config: CherrypyServerConfig = None):
        config = config or CherrypyServer.CherrypyServerConfig(CherrypyServer.DEFAULT_ADDR, CherrypyServer.DEFAULT_PORT)
        super().__init__(config)
        self._logger = logging.getLogger(__name__)

    def start(self):
        conf = self._config.as_dict()
        ssl_conf = self.__configure_ssl()
        conf.update(ssl_conf)
        self._logger.info("Starting server with config: {}".format(conf))
        cherrypy.config.update(conf)
        engine.start()
        self._logger.info("Server started")
        engine.block()

    def stop(self):
        raise NotImplementedError()

    def register_endpoint(self, endpoint_obj: cherryserver.core.endpoint.endpoint.Endpoint):
        conf = self.__default_conf()
        if endpoint_obj.conf:
            conf.update(endpoint_obj.conf)
        path = self.__append_context_path(endpoint_obj)
        self._logger.info("Registering endpoint: {}, final path='{}', final conf='{}'".format(endpoint_obj, path, conf))
        tree.mount(endpoint_obj, path, conf)

    def __configure_ssl(self) -> dict:
        ssl_conf = [self._config.ssl_cert, self._config.ssl_private_key, self._config.ssl_cert_chain]
        if not any(ssl_conf):
            self._logger.info("SSL disabled.")
            return {}
        elif not all(ssl_conf):
            self._logger.error("SSL configuration seems to be broken, ssl_cert [{}], ssl_private_key [{}], "
                               "ssl_cert_chain [{}] or ssl_module [{}] property isn't set.".format(
                self._config.ssl_cert, self._config.ssl_private_key, self._config.ssl_cert_chain,
                self._config.ssl_module))
            raise ServerConfigurationError("SSL configuration is broken.")

        return {
            CherrypyConfigKey.SERVER_SSL_CERT.value: self._config.ssl_cert,
            CherrypyConfigKey.SERVER_SSL_PRIVATE_KEY.value: self._config.ssl_private_key,
            CherrypyConfigKey.SERVER_SSL_CERT_CHAIN.value: self._config.ssl_cert_chain,
            CherrypyConfigKey.SERVER_SSL_MODULE.value: self._config.ssl_module
        }

    def __append_context_path(self, endpoint_obj):
        return "".join([self._config.context_path, endpoint_obj.path]) if self._config.context_path else \
            endpoint_obj.path

    def __default_conf(self):
        return {
            "/": {
                CherrypyConfigKey.REQUEST_DISPATCH.value: cherrypy.dispatch.MethodDispatcher()
            }
        }
