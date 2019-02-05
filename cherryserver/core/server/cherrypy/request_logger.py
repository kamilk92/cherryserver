import logging

import cherrypy
from cherryserver.core.http.header_element import HeaderElement

from cherryserver.core.server.cherrypy import cherrypy_util

logger = logging.getLogger(__name__)


def log_request_response(func):
    def wrapper(*args, **kwargs):
        req_path = " ".join([cherrypy_util.get_request_method(), cherrypy_util.get_request_path()])
        __log_request_headers(req_path)
        body = __log_request_body(req_path)
        kwargs["body"] = body
        result = func(*args, **kwargs)
        __log_response(result, req_path)

        return result

    return wrapper


def __log_request_headers(req_path):
    if not cherrypy.request.headers:
        logger.error("[{}] Missing request headers".format(req_path))
        return

    logger.info("[{}] Request headers: '{}'".format(req_path, cherrypy.request.headers))


def __log_request_body(req_path):
    if (not cherrypy.request.headers) or (int(cherrypy.request.headers.get(HeaderElement.CONTENT_LENGTH.value, 0)) <= 0):
        logger.info("[{}] Empty request body".format(req_path))
        return

    body = cherrypy.request.body.read(int(cherrypy.request.headers[HeaderElement.CONTENT_LENGTH.value]))
    logger.info("[{}] Request body: '{}'".format(req_path, body))

    return body


def __log_response(rsp, req_path):
    if not rsp:
        logger.info("[{}] Empty request's response body".format(req_path))
        return

    logger.info("[{}] Request's response body: '{}'".format(req_path, rsp))
