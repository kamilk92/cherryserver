from unittest import TestCase

from cherryserver.core.endpoint.health.health_endpoint import HealthEndpoint


class TestHealthEndpoint(TestCase):
    def setUp(self):
        self.health_endpoint = HealthEndpoint()

    def test_is_get_return_health_message(self):
        rsp = self.health_endpoint.GET()
        self.assertEqual(rsp, HealthEndpoint.HEALTH_MSG)

    def test_is_post_return_health_message(self):
        rsp = self.health_endpoint.POST()
        self.assertEqual(rsp, HealthEndpoint.HEALTH_MSG)
