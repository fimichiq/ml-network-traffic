import os
import requests

from flask import Blueprint, request, jsonify
from ..config import UPLOAD_FOLDER, CICFLOWMETER_URL


manage_bp = Blueprint('manage', __name__)

@manage_bp.route('/convert', methods=['POST'])
def convert_pcap():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files.get('file')
        if not file:
            return jsonify({"error": "No file provided"}), 400
        
        # Save file temporarily with new name
        file_name = file.filename
        file_path = os.path.join(UPLOAD_FOLDER, file_name)
        file.save(file_path)
        
        response = requests.get(
            f"{CICFLOWMETER_URL}/convert/{file_name}"
        )
        
        if response.status_code == 200:
            return response.json(), 200
        else:
            return jsonify({"error": "Conversion failed", "details": response.text}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
