from abc import ABCMeta, abstractmethod

from cherryserver.core.endpoint.endpoint import Endpoint


class Server(metaclass=ABCMeta):
    class ServerConfig(object):
        def __init__(self, addr, port, context_path=None, ssl_cert=None, ssl_private_key=None, ssl_cert_chain=None):
            self.addr = addr
            self.port = port
            self.context_path = context_path
            self.ssl_cert = ssl_cert
            self.ssl_private_key = ssl_private_key
            self.ssl_cert_chain = ssl_cert_chain

        @property
        def addr(self):
            return self._addr

        @addr.setter
        def addr(self, addr):
            self._addr = addr

        @property
        def port(self):
            return self._port

        @port.setter
        def port(self, port):
            self._port = port

        @property
        def context_path(self):
            return self._context_path

        @context_path.setter
        def context_path(self, path: str):
            self._context_path = path

        @property
        def ssl_cert(self):
            return self._ssl_cert

        @ssl_cert.setter
        def ssl_cert(self, cert):
            self._ssl_cert = cert

        @property
        def ssl_private_key(self):
            return self._ssl_private_key

        @ssl_private_key.setter
        def ssl_private_key(self, ssl_private_key):
            self._ssl_private_key = ssl_private_key

        @property
        def ssl_cert_chain(self):
            return self._ssl_cert_chain

        @ssl_cert_chain.setter
        def ssl_cert_chain(self, ssl_cert_chain):
            self._ssl_cert_chain = ssl_cert_chain

    def __init__(self, config: ServerConfig):
        self._config = config

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def register_endpoint(self, endpoint_obj: Endpoint):
        pass
