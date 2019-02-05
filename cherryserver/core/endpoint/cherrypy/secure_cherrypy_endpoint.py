from abc import abstractmethod, ABCMeta

import cherrypy
from cherryserver.core.endpoint.cherrypy.cherrypy_endpoint import CherrypyEndpoint
from cherryserver.core.endpoint.security.secure_endpoint import SecureEndpoint
from cherryserver.core.http.code import HttpCode


class SecureCherrypyEndpoint(SecureEndpoint, CherrypyEndpoint, metaclass=ABCMeta):
    def __init__(self, path: str, name: str, valid_secure_roles: list, conf: dict = None):
        CherrypyEndpoint.__init__(self, path, name, conf)
        SecureEndpoint.__init__(self, path, name, valid_secure_roles, conf)

    def _roles_not_valid_response(self):
        cherrypy.response.status = HttpCode.FORBIDDEN

    @abstractmethod
    def _validate_roles(self) -> bool:
        pass
