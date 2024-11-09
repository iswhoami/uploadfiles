from flask import Blueprint

from views import FileView, FileUpload, FileDelete

files = Blueprint('files', __name__)

files.add_url_rule('/file', methods=['GET'], view_func=FileView.as_view('file_view'))
files.add_url_rule('/upload', methods=['POST'], view_func=FileUpload.as_view('upload_file_view'))
files.add_url_rule('/delete', methods=['DELETE'], view_func=FileDelete.as_view('delete_file_view'))
