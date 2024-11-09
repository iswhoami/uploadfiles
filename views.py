import os
import uuid

from flask import jsonify, make_response, send_file

from baseview import BaseView
from config import UPLOAD_FOLDER


class FilesView(BaseView):
    """ Список файлов """

    DEFAULT_PER_PAGE_LIMIT = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.limit = self.DEFAULT_PER_PAGE_LIMIT

    @property
    def offset(self):
        return self.page * self.limit - self.limit

    def get(self):
        # parsing
        self.page = self.parse_int('page', 1)
        # processing
        try:
            all_count = self._conn.execute_single_value('SELECT COUNT (*) FROM files')
            pages = all_count // self.limit if all_count % self.limit == 0 else all_count // self.limit + 1

            if self.page > 1:
                sql_query = 'SELECT * FROM files LIMIT {} OFFSET {}'.format(self.limit, self.offset)
            else:
                sql_query = 'SELECT * FROM files LIMIT {}'.format(self.limit)

            result = self._conn.execute(sql_query)
        except Exception as e:
            api_result = {
                'result': False,
                'message': str(e)
            }
            return make_response(jsonify(api_result), 500)

        api_result = {
            'status': True,
            'items': result,
            'page': self.page,
            'pageSize': self.limit,
            'pages': pages
        }

        return make_response(jsonify(api_result), 200)


class FileView(BaseView):
    """ Загрузка файла с сервера """

    def get(self):
        # parse
        file_id = self.parse_int('file_id')
        # processing
        result = self._conn.execute_one_row('SELECT filename, filename_new '
                                            'FROM files '
                                            'WHERE file_id = ?', (file_id,))
        if not result:
            api_result = {
                'status': False,
                'message': "File not found"
            }
            return make_response(jsonify(api_result), 200)

        filename = result.get('filename')
        filename_new = result.get('filename_new')

        from config import UPLOAD_FOLDER
        file_path = os.path.join(UPLOAD_FOLDER, filename_new)

        return make_response(send_file(file_path, as_attachment=True, download_name=filename), 200)


class FileUpload(BaseView):
    """ Загрузка файла на сервер """

    def post(self):
        # parse
        file = self.parse_file('file')
        # processing
        try:
            oldfilename = file.filename
            filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            file_id = self._conn.execute_single_value("INSERT INTO files (filename, filename_new) "
                                                      "VALUES (?, ?) "
                                                      "RETURNING file_id",
                                                      (oldfilename, filename))
        except Exception as e:
            api_result = {
                'result': False,
                'message': str(e)
            }
            return make_response(jsonify(api_result), 500)
        else:
            api_result = {
                'result': True,
                'file_id': file_id,
                'message': "uploaded"
            }
        return make_response(jsonify(api_result), 200)


class FileDelete(BaseView):
    """ Удаление файла """

    def delete(self):
        # parse
        file_id = self.parse_int('file_id')
        # processing
        try:
            result = self._conn.execute_one_row('SELECT filename, filename_new '
                                                'FROM files '
                                                'WHERE file_id = ?', (file_id,))
            if not result:
                api_result = {
                    'status': False,
                    'message': "File not found"
                }
                return make_response(jsonify(api_result), 200)

            filename_new = result.get('filename_new')

            from config import UPLOAD_FOLDER
            file_path = os.path.join(UPLOAD_FOLDER, filename_new)

            os.remove(file_path)
            sql_query = 'DELETE FROM files WHERE file_id = ?'
            self._conn.execute_void(sql_query, (file_id,))
        except Exception as e:
            api_result = {
                'result': False,
                'message': str(e)
            }
            return make_response(jsonify(api_result), 500)

        api_result = {
            'status': False,
            'message': "File successfully deleted"
        }

        return make_response(jsonify(api_result), 200)
