import os
import subprocess
import uuid

from flask import Flask, request, send_file, jsonify
import requests

app = Flask(__name__)

# Directory where uploaded files will be saved
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/files/PCAPs')
CONVERT_FOLDER = os.getenv('CONVERT_FOLDER', '/files/Netflows')

@app.route('/convert/<file_name>', methods=['GET'])
def upload_file(file_name: str):

    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    base_name, ext = os.path.splitext(file_name)
    new_name = f"{base_name}_{uuid.uuid4().hex}_flow.csv"
    converted_file = os.path.join(CONVERT_FOLDER, new_name)


    try:
        command = f"CICFlowMeter-4.0/bin/cfm {file_path} {CONVERT_FOLDER}"
        subprocess.run(command, shell=True, check=True)

        flow_file = os.path.join(CONVERT_FOLDER, f"{file_name}_Flow.csv")
        
        if os.path.isfile(flow_file):
            os.rename(flow_file, converted_file)
        else:
            return {"error": "Conversion failed, output file not found"}, 500
        
        # Check if the converted file exists
        if os.path.exists(converted_file):
            return {"message": f"File {file_name} converted successfully", "filename": new_name}, 200
        else:
            return {"error": "Conversion completed but output file not found"}, 404
            
    except subprocess.CalledProcessError as e:
        return {"error": f"Error processing file: {str(e)}"}, 500
    
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(CONVERT_FOLDER, exist_ok=True)
    app.run(host='0.0.0.0', port=6000)

