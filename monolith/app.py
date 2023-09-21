# all imports
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from os import environ
import requests

app = Flask(__name__)
CORS(app)

# for API Keys
# from dotenv import load_dotenv
# load_dotenv('spm.env')

@app.route("/")
def main():
    return

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for the SPM monolith...")
    app.run(host="0.0.0.0", port=8000, debug=True)