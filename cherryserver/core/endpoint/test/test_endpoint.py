from unittest import TestCase, mock

from cherryserver.core.endpoint.endpoint import Endpoint


class DummyEndpoint(Endpoint):
    def _method_not_allowed(self):
        pass


class TestEndpoint(TestCase):
    def setUp(self):
        self.endpoint = DummyEndpoint("", "")

    @mock.patch.object(DummyEndpoint, "_method_not_allowed")
    def test_is_endpoint_by_default_not_allowed(self, method_not_allowed_mock):
        self.endpoint.get_method()
        method_not_allowed_mock.assert_called_once()

        self.endpoint.post_method()
        self.assertEqual(method_not_allowed_mock.call_count, 2)

        self.endpoint.put_method()
        self.assertEqual(method_not_allowed_mock.call_count, 3)
