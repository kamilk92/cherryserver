from cherryserver.core.endpoint.cherrypy.jwt_secure_cherrypy_endpoint import JWTSecureCherrypyEndpoint
from cherryserver.core.endpoint.time.time_endpoint import TimeEndpoint


class SecureTimeEndpoint(JWTSecureCherrypyEndpoint):
    def __init__(self, secure_roles: list, path="/time", name="time_endpoint", conf: dict = None):
        super().__init__(path, name, secure_roles, conf)

    def secure_post(self, *args, **kwargs):
        return TimeEndpoint.post_method(self, *args, **kwargs)
