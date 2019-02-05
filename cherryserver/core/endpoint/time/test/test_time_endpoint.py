import ast
from unittest import TestCase

from cherryserver.core.endpoint.time.time_endpoint import TimeEndpoint


class TestTimeEndpoint(TestCase):
    def test_is_time_endpoint_return_json_rsp(self):
        time_endpoint = TimeEndpoint()
        time_rsp = time_endpoint.post_method()
        self.assertIsNotNone(time_rsp)
        rsp_as_json = ast.literal_eval(time_rsp.decode("utf-8"))
        self.assertIsNotNone(rsp_as_json["time"])
