from flask import Flask, request, send_from_directory, jsonify
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

import inspect
import os
import uuid

from .AppCore import AppCore

app = Flask(__name__, static_folder='../static', static_url_path='/static')
api = Api(app)

# アップロード設定
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


class FileUpload(Resource):
    """ファイルアップロードAPI"""

    def post(self):
        if 'file' not in request.files:
            return {'error': 'No file part'}, 400

        file = request.files['file']
        if file.filename == '':
            return {'error': 'No selected file'}, 400

        # ユニークIDを生成
        file_id = str(uuid.uuid4())
        filename = secure_filename(file.filename)

        # ファイル保存用ディレクトリを作成
        save_dir = os.path.join(UPLOAD_FOLDER, file_id)
        os.makedirs(save_dir, exist_ok=True)

        # ファイルを保存
        file_path = os.path.join(save_dir, filename)
        file.save(file_path)

        # ダウンロードURLを生成
        download_url = f'/api/download/{file_id}/{filename}'

        return {
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'download_url': download_url
        }


class FileDownload(Resource):
    """ファイルダウンロードAPI"""

    def get(self, file_id, filename):
        directory = os.path.join(UPLOAD_FOLDER, file_id)

        if not os.path.exists(directory):
            return {'error': 'File not found'}, 404

        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            return {'error': 'File not found'}, 404

        return send_from_directory(
            directory,
            filename,
            as_attachment=True,
            download_name=filename
        )


# BridgeDrop API エンドポイント
api.add_resource(FileUpload, '/api/upload')
api.add_resource(FileDownload, '/api/download/<string:file_id>/<string:filename>')


# 既存のAppCore自動登録（互換性維持）
def add_resource_legacy(module_name: str, c):
    api.add_resource(c, f'/{module_name}/{c.__name__}/<{c.type}:{c.arg}>')


def add_resources(module):
    classes = [cls for name, cls in inspect.getmembers(AppCore, inspect.isclass) if name != "__class__"]
    for cls in classes:
        add_resource_legacy(module.__name__, cls)


add_resources(AppCore)
