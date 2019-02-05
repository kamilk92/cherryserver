from abc import abstractmethod

from cherryserver.core.endpoint.endpoint import Endpoint


class SecureEndpoint(Endpoint):
    def __init__(self, path: str, name: str, secure_roles: list, conf: dict = None):
        super().__init__(path, name, conf)
        self.secure_roles = secure_roles

    def get_method(self, *args, **kwargs):
        return self.secure_get(*args, **kwargs) if self._validate_roles() else self._roles_not_valid_response()

    def secure_get(self, *args, **kwargs):
        self._method_not_allowed()

    def post_method(self, *args, **kwargs):
        return self.secure_post(*args, **kwargs) if self._validate_roles() else self._roles_not_valid_response()

    def secure_post(self, *args, **kwargs):
        self._method_not_allowed()

    def put_method(self, *args, **kwargs):
        return self.secure_put(*args, **kwargs) if self._validate_roles() else self._roles_not_valid_response()

    def secure_put(self, *args, **kwargs):
        self._method_not_allowed()

    @property
    def secure_roles(self):
        return self._secure_roles

    @secure_roles.setter
    def secure_roles(self, secure_roles):
        self._secure_roles = secure_roles

    @abstractmethod
    def _validate_roles(self) -> bool:
        pass

    @abstractmethod
    def _roles_not_valid_response(self):
        pass
