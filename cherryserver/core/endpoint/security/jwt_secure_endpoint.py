import logging
from abc import ABCMeta

from cherrypy import request

from cherryserver.core.endpoint.security.secure_endpoint import SecureEndpoint
from cherryserver.core.http.header_element import HeaderElement


class JWTSecureEndpoint(SecureEndpoint, metaclass=ABCMeta):
    def __init__(self, path: str, name: str, secure_roles: list, conf: dict = None):
        super().__init__(path, name, secure_roles, conf)
        self._logger = logging.getLogger(__name__)

    def _validate_roles(self) -> bool:
        req_role = request.headers.get(HeaderElement.AUTHORIZATION.value, None)
        if not req_role:
            self._logger.error("Missing roles in request header")
            return False
        if req_role not in self.secure_roles:
            self._logger.error("Role '{}' not allowed".format(req_role))
            return False

        return True
