from unittest import TestCase, mock

from cherryserver.util import test_util
from cherryserver.util.test_util import get_mock_call_args_list


def dummy_function(arg1, arg2, arg3):
    return arg1, arg2, arg3


class TestTestUtil(TestCase):
    @mock.patch("cherryserver.util.test.test_test_util.dummy_function")
    def test_is_get_mock_call_arg_return_correct_value(self, dummy_func_mock):
        arg1, arg2, arg3 = 1, 2, 3
        dummy_func_mock(arg1, arg2, arg3)

        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 0), arg1)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 1), arg2)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 2), arg3)

    @mock.patch("cherryserver.util.test.test_test_util.dummy_function")
    def test_is_get_mock_call_arg_return_correct_call_args(self, dummy_func_mock):
        first_call_arg1, first_call_arg2, first_call_arg3 = 1, 2, 3
        dummy_func_mock(first_call_arg1, first_call_arg2, first_call_arg3)

        second_call_arg1, second_call_arg2, second_call_arg3 = 11, 12, 13
        dummy_func_mock(second_call_arg1, second_call_arg2, second_call_arg3)

        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 0), first_call_arg1)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 1), first_call_arg2)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 0, 2), first_call_arg3)

        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 1, 0), second_call_arg1)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 1, 1), second_call_arg2)
        self.assertEqual(test_util.get_mock_call_arg(dummy_func_mock, 1, 2), second_call_arg3)

    def test_is_get_mock_call_args_list_raise_type_error_when_arg_is_none(self):
        self.assertRaises(TypeError, lambda: get_mock_call_args_list(None))
