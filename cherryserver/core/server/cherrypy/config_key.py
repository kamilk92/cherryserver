from enum import Enum


class CherrypyConfigKey(Enum):
    REQUEST_DISPATCH = "request.dispatch"
    SERVER_PORT = "server.socket_port"
    SERVER_ADDR = "server.socket_host"
    SERVER_SSL_MODULE = "server.ssl_module"
    SERVER_SSL_CERT = "server.ssl_certificate"
    SERVER_SSL_CERT_CHAIN = "server.ssl_certificate_chain"
    SERVER_SSL_PRIVATE_KEY = "server.ssl_private_key"
