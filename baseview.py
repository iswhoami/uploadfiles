from flask import request
from flask.views import MethodView

from connection import Connection


class BaseView(MethodView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn = Connection()

    def parse_file(self, argname, default=None):
        file = request.files.get(argname, default)
        return file

    def parse_int(self, argname, default=None):
        value = request.values.get(argname, default)
        try:
            return int(value)
        except ValueError:
            return default

    def parse_str(self, argname, default=None):
        return request.values.get(argname, default)
