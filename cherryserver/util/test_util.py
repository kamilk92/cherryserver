from unittest.mock import Mock


def get_mock_call_args_list(mock: Mock):
    if mock is None:
        raise TypeError("mock is None")

    return mock.call_args_list


def get_mock_call_arg(mock: Mock, call_num: int, arg_num: int):
    all_calls = get_mock_call_args_list(mock)

    return all_calls[call_num][0][arg_num]
