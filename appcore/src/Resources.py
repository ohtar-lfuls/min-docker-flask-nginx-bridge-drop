from flask import Flask, request, send_from_directory, send_file, Response
from flask_restful import Api, Resource
from werkzeug.utils import secure_filename

import inspect
import os
import uuid
import time
import threading
import shutil
import io
import qrcode

from .AppCore import AppCore

app = Flask(__name__, static_folder='../static', static_url_path='/static')
api = Api(app)

# アップロード設定
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ファイル有効期限（秒）
FILE_EXPIRY_SECONDS = 600  # 10分


def get_base_url():
    """リクエストからベースURLを取得"""
    # X-Forwarded-Host があればそれを使用（プロキシ経由）
    host = request.headers.get('X-Forwarded-Host') or request.host
    scheme = request.headers.get('X-Forwarded-Proto') or request.scheme
    return f"{scheme}://{host}"


def cleanup_old_files():
    """古いファイルを削除するバックグラウンドタスク"""
    while True:
        try:
            now = time.time()
            for file_id in os.listdir(UPLOAD_FOLDER):
                dir_path = os.path.join(UPLOAD_FOLDER, file_id)
                if os.path.isdir(dir_path):
                    dir_mtime = os.path.getmtime(dir_path)
                    if now - dir_mtime > FILE_EXPIRY_SECONDS:
                        shutil.rmtree(dir_path)
                        print(f"[Cleanup] Deleted expired file: {file_id}")
        except Exception as e:
            print(f"[Cleanup] Error: {e}")
        time.sleep(60)


# バックグラウンドでクリーンアップスレッドを起動
cleanup_thread = threading.Thread(target=cleanup_old_files, daemon=True)
cleanup_thread.start()


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
        download_path = f'/api/download/{file_id}/{filename}'
        
        # ベースURLを取得して完全なURLを生成
        base_url = get_base_url()
        full_download_url = f'{base_url}{download_path}'

        return {
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'download_url': download_path,
            'full_download_url': full_download_url,
            'expires_in': FILE_EXPIRY_SECONDS
        }


class FileDownload(Resource):
    """ファイルダウンロードAPI"""

    def get(self, file_id, filename):
        directory = os.path.join(UPLOAD_FOLDER, file_id)

        if not os.path.exists(directory):
            return {'error': 'File not found or expired'}, 404

        file_path = os.path.join(directory, filename)
        if not os.path.exists(file_path):
            return {'error': 'File not found or expired'}, 404

        return send_from_directory(
            directory,
            filename,
            as_attachment=True,
            download_name=filename
        )


class QRCodeGenerator(Resource):
    """QRコード生成API"""

    def get(self):
        url = request.args.get('url')
        if not url:
            return {'error': 'URL parameter required'}, 400

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        img_io = io.BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)

        return send_file(img_io, mimetype='image/png')


class ServerInfo(Resource):
    """サーバー情報API"""

    def get(self):
        return {
            'base_url': get_base_url(),
            'host': request.host
        }


# BridgeDrop API エンドポイント
api.add_resource(FileUpload, '/api/upload')
api.add_resource(FileDownload, '/api/download/<string:file_id>/<string:filename>')
api.add_resource(QRCodeGenerator, '/api/qrcode')
api.add_resource(ServerInfo, '/api/server-info')


# 既存のAppCore自動登録（互換性維持）
def add_resource_legacy(module_name: str, c):
    api.add_resource(c, f'/{module_name}/{c.__name__}/<{c.type}:{c.arg}>')


def add_resources(module):
    classes = [cls for name, cls in inspect.getmembers(AppCore, inspect.isclass) if name != "__class__"]
    for cls in classes:
        add_resource_legacy(module.__name__, cls)


add_resources(AppCore)
