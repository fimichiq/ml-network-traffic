import os

from flask import Blueprint, request, jsonify
from ..config import CONVERT_FOLDER, MODEL_FOLDER

files_bp = Blueprint('files', __name__)

@files_bp.route("/files", methods=['GET'])
def get_files():
    try:
        files = os.listdir(CONVERT_FOLDER)
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@files_bp.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(CONVERT_FOLDER, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted"}), 200
    return jsonify({"error": "File not found"}), 404

@files_bp.route('/models', methods=['GET'])
def get_models():
    try:
        models = os.listdir(MODEL_FOLDER)
        models = [model for model in models if model.endswith('.pkl')]
        return jsonify(models)
    except Exception as e:
        return jsonify({"error": str(e)}), 500