import os
import uuid

import requests
from flask import Flask
from flask_cors import CORS

from .config import UPLOAD_FOLDER, CONVERT_FOLDER, MODEL_FOLDER
from .routes.files import files_bp
from .routes.manage import manage_bp

app = Flask(__name__)
CORS(app)


def setup_app():

    app.register_blueprint(manage_bp)
    app.register_blueprint(files_bp)

    return app
