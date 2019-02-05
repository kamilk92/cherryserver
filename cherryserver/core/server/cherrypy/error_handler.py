import logging
import traceback

import cherrypy
from cherryserver.core.exception.error import ServerError
from cherryserver.core.http.code import HttpCode

from cherryserver.core.server.cherrypy import cherrypy_util

logger = logging.getLogger(__name__)


def application_error_to_http_500(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
        except cherrypy.HTTPError as e:
            response = __handle_cherrypy_http_error(e)
        except ServerError as e:
            response = __handle_server_error(e)
        except Exception as e:
            response = __handle_error(e)

        return response

    return wrapper


def __handle_cherrypy_http_error(e: cherrypy.HTTPError) -> dict:
    __log_error()
    response = __set_response(e.status, 0, e._message)

    return response


def __handle_server_error(e: ServerError):
    __log_error()
    response = __set_response(e.response_http_code, e.service_code, e.msg)

    return response


def __handle_error(e: Exception):
    __log_error()
    response = __set_response(HttpCode.INTERNAL_ERROR, 0, "Unexpected application error")

    return response


def __log_error():
    formatted_error = traceback.format_exc()
    logger.error(formatted_error)


def __set_response(http_code: int, service_code: int, message: str):
    cherrypy.response.status = http_code

    return cherrypy_util.to_json({
        "service_code": service_code,
        "message": message
    })
