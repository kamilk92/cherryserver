from enum import IntEnum


class HttpCode(IntEnum):
    SUCCESS = 200
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    INTERNAL_ERROR = 500
