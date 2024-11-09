import os
import uuid

from flask import jsonify, make_response, send_file

from baseview import BaseView
from config import UPLOAD_FOLDER


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
