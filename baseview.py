from flask import request
from flask.views import MethodView
from werkzeug.exceptions import BadRequest

from connection import Connection


class BaseView(MethodView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._conn = Connection()

    def parse_file(self, argname, default=None):
        """
        Парсинг файла

        :param argname: Имя аргумента
        :param default: Значение по-умолчанию
        """

        file = request.files.get(argname, default)
        return file

    def parse_int(self, argname, default=None):
        """
        Парсинг целого числа

        :param argname: Имя аргумента
        :param default: Значение по-умолчанию
        """

        value = request.values.get(argname, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def parse_str(self, argname, default=None):
        """
        Парсинг строки

        :param argname: Имя аргумента
        :param default: Значение по-умолчанию
        """

        return request.values.get(argname, default)

    @staticmethod
    def check_arg_required(expr, argname):
        """
        Проверяет на истинность условие `expr` и генерирует `BadRequest`,
        если оно ложно

        :param bool expr: условие для проверки
        :param str argname: имя требуемого аргумента
        """

        if expr is None:
            raise BadRequest('Argument \'{}\' is required'.format(argname))
