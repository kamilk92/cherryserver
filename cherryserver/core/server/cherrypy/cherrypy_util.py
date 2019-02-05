import json

import cherrypy
from cherryserver.core.http.header_element import HeaderElement

from cherryserver.core.http.content_type import ContentType


def to_json(d: dict):
    cherrypy.response.headers[HeaderElement.CONTENT_TYPE.value] = ContentType.APPLICATION_JSON.value

    return json.dumps(d).encode("utf-8")


def get_request_path():
    return cherrypy.request.script_name


def get_request_method():
    return cherrypy.request.method
