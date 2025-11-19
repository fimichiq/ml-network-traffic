"""Application configuration - centralized constants and environment variables."""
import os

# Folder paths
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/shared-files/PCAPs')
CONVERT_FOLDER = os.getenv('CONVERT_FOLDER', '/app/shared-files/Netflows')
MODEL_FOLDER = 'ml_model'

# Service URLs
CICFLOWMETER_URL = os.getenv('CICFLOWMETER_URL', 'http://localhost:6000')

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERT_FOLDER, exist_ok=True)
