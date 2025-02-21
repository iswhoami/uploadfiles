from flask import Blueprint

from endpoints.file import FileView, FileUpload

files = Blueprint('files', __name__)

files.add_url_rule('/<date>/<filename>', methods=['GET'], view_func=FileView.as_view('file_view'))
files.add_url_rule('/upload', methods=['POST'], view_func=FileUpload.as_view('upload_file_view'))
