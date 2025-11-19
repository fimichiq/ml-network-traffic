import os
import subprocess
from flask import Flask, request
from setup_app import setup_app

if __name__ == '__main__':
    app = setup_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

