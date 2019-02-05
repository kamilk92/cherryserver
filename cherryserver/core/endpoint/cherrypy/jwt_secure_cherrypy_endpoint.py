from cherryserver.core.endpoint.security.jwt_secure_endpoint import JWTSecureEndpoint

from cherryserver.core.endpoint.cherrypy.secure_cherrypy_endpoint import SecureCherrypyEndpoint


class JWTSecureCherrypyEndpoint(SecureCherrypyEndpoint, JWTSecureEndpoint):
    def __init__(self, path: str, name: str, secure_roles: list, conf: dict = None):
        SecureCherrypyEndpoint.__init__(self, path, name, secure_roles, conf)
        JWTSecureEndpoint.__init__(self, path, name, secure_roles, conf)

    def _validate_roles(self) -> bool:
        return JWTSecureEndpoint._validate_roles(self)
