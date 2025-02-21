from flask import Flask

from endpoints.routes import files


class Webserver(Flask):
    def __init__(self, import_name='webserver', *args, **kwargs):
        super().__init__(import_name=import_name, *args, **kwargs)
        self._register_blueprints()

    def _register_blueprints(self):
        self.register_blueprint(files, url_prefix='/files')


if __name__ == '__main__':
    webserver = Webserver()
    webserver.run()
