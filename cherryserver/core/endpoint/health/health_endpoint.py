from cherryserver.core.endpoint.cherrypy.cherrypy_endpoint import CherrypyEndpoint


class HealthEndpoint(CherrypyEndpoint):
    HEALTH_MSG = "health"

    def __init__(self, path="/health", name="health", conf: dict = None):
        super().__init__(path, name, conf)

    def get_method(self, *args, **kwargs):
        return HealthEndpoint.HEALTH_MSG

    def post_method(self, *args, **kwargs):
        return HealthEndpoint.HEALTH_MSG
