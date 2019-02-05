from unittest import TestCase
from unittest.mock import patch

from cherryserver.core.endpoint.security.secure_endpoint import SecureEndpoint


class DummySecureEndpoint(SecureEndpoint):
    def secure_get(self, *args, **kwargs):
        pass

    def secure_post(self, *args, **kwargs):
        pass

    def secure_put(self, *args, **kwargs):
        pass

    def _roles_not_valid_response(self):
        pass

    def _validate_roles(self) -> bool:
        pass

    def _method_not_allowed(self):
        raise Exception("Method not allowed")


class TestSecureEndpoint(TestCase):
    @patch.object(DummySecureEndpoint, "_validate_roles")
    @patch.object(DummySecureEndpoint, "secure_get")
    def test_is_role_validated_on_get_method(self, secure_get_mock, validate_roles_mock):
        validate_roles_mock.return_value = True
        dummy_secure_endpoint = DummySecureEndpoint("", "", [])

        dummy_secure_endpoint.get_method()

        validate_roles_mock.assert_called_once()
        secure_get_mock.assert_called_once()

    @patch.object(DummySecureEndpoint, "_validate_roles")
    @patch.object(DummySecureEndpoint, "secure_post")
    def test_is_role_validated_on_get_method(self, secure_post_mock, validate_roles_mock):
        validate_roles_mock.return_value = True
        dummy_secure_endpoint = DummySecureEndpoint("", "", [])

        dummy_secure_endpoint.post_method()

        validate_roles_mock.assert_called_once()
        secure_post_mock.assert_called_once()

    @patch.object(DummySecureEndpoint, "_validate_roles")
    @patch.object(DummySecureEndpoint, "secure_put")
    def test_is_role_validated_on_put_method(self, secure_put_mock, validate_roles_mock):
        validate_roles_mock.return_value = True
        dummy_secure_endpoint = DummySecureEndpoint("", "", [])

        dummy_secure_endpoint.put_method()

        validate_roles_mock.assert_called_once()
        secure_put_mock.assert_called_once()

    @patch.object(DummySecureEndpoint, "_roles_not_valid_response")
    @patch.object(DummySecureEndpoint, "_validate_roles")
    def test_is_returned_valid_response_when_roles_not_valid(self, validate_roles_mock, roles_not_valid_response_mock):
        validate_roles_mock.return_value = False
        not_valid_value = "NOT_VALID_VALUE"
        roles_not_valid_response_mock.return_value = not_valid_value

        dummy_secure_endpoint = DummySecureEndpoint("", "", [])

        self.assertEqual(dummy_secure_endpoint.get_method(), not_valid_value)
        self.assertEqual(dummy_secure_endpoint.post_method(), not_valid_value)
        self.assertEqual(dummy_secure_endpoint.put_method(), not_valid_value)
