import time

from cherryserver.core.endpoint.cherrypy.cherrypy_endpoint import CherrypyEndpoint

from cherryserver.core.server.cherrypy import cherrypy_util


class TimeEndpoint(CherrypyEndpoint):
    def __init__(self, path="/time", name="time", conf=None):
        super().__init__(path, name, conf)

    def post_method(self, *args, **kwargs):
        return cherrypy_util.to_json({
            "time": time.time()
        })
