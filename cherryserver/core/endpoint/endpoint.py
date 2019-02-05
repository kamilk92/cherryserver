from abc import ABCMeta, abstractmethod


class Endpoint(metaclass=ABCMeta):
    exposed = True

    def __init__(self, path: str, name: str, conf: dict = None):
        self.path = path
        self.name = name
        self.conf = conf or {}

    def get_method(self, *args, **kwargs):
        return self._method_not_allowed()

    def post_method(self, *args, **kwargs):
        return self._method_not_allowed()

    def put_method(self, *args, **kwargs):
        return self._method_not_allowed()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, path):
        self._path = path

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def conf(self):
        return self._conf

    @conf.setter
    def conf(self, conf: dict):
        self._conf = conf

    @abstractmethod
    def _method_not_allowed(self):
        pass

    def __str__(self):
        return "Endpoint name='{}', path='{}', conf='{}'".format(self.name, self.path, self.conf)
