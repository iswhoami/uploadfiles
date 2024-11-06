from flask.views import MethodView


class _BaseView(MethodView):
    pass


class FilesView(_BaseView):
    def get(self):
        return 'files'


class FileView(_BaseView):
    def get(self):
        return 'file'


class FileUpload(_BaseView):
    def post(self):
        return 'uploaded'


class FileDelete(_BaseView):
    def delete(self):
        return 'deleted'
