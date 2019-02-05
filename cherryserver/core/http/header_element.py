from enum import Enum


class HeaderElement(Enum):
    AUTHORIZATION = "authorization"
    CONTENT_TYPE = "Content-Type"
    CONTENT_LENGTH = "Content-Length"
