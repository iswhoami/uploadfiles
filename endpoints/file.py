import os
import uuid
from datetime import datetime

from flask import jsonify, make_response, send_file

from baseview import BaseView
from config import UPLOAD_FOLDER


class FileView(BaseView):
    """ Загрузка файла с сервера """

    def get(self, date, filename):
        file_path = os.path.join(UPLOAD_FOLDER, date, filename)
        if os.path.isfile(file_path):
            filename = self._conn.execute_single_value('SELECT original_filename '
                                                       'FROM files '
                                                       'WHERE path = ?', (file_path,))
            return make_response(send_file(file_path, as_attachment=True,
                                                            download_name=filename), 200)
        else:
            api_result = {
                'status': False,
                'error': "Path to the file does not exist"
            }
            return make_response(jsonify(api_result), 404)


class FileUpload(BaseView):
    """ Загрузка файла на сервер """

    def post(self):
        # parse
        file = self.parse_file('file')
        # check
        self.check_arg_required(file, 'file')
        # processing
        try:
            original_filename = file.filename
            new_filename = str(uuid.uuid4()) + os.path.splitext(file.filename)[1]
            today_date = datetime.today().strftime('%d-%m-%Y')
            working_dir = os.path.join(UPLOAD_FOLDER, today_date)

            if not os.path.exists(working_dir):
                os.makedirs(working_dir)

            path = os.path.join(working_dir, new_filename)
            file.save(path)
            self._conn.execute_void('INSERT INTO files (original_filename, new_filename, path) '
                                    'VALUES (?, ?, ?)',
                                    (original_filename, new_filename, path))
        except Exception as e:
            api_result = {
                'result': False,
                'error': str(e)
            }
            return make_response(jsonify(api_result), 500)
        else:
            api_result = {
                'result': True,
                'file_path': path,
                'message': "uploaded"
            }
        return make_response(jsonify(api_result), 200)
