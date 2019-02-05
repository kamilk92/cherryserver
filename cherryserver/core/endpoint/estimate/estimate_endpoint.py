import json

from cherryserver.core.endpoint.cherrypy.cherrypy_endpoint import CherrypyEndpoint


class EstimateEndpoint(CherrypyEndpoint):
    def __init__(self):
        super().__init__("/estimate", "estimator_endpoint")

    def post_method(self, *args, **kwargs):
        if "body" not in kwargs:
            raise Exception("Missing body request")

        req_json = json.loads(kwargs["body"])

        return self._to_json({
            "data": req_json["body"],
            "result": 1
        })
