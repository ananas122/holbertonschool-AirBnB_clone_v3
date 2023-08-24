#!/usr/bin/python3
"""app.py to connect API"""
import os
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS
from os import getenv
from api.v1.views import app_views
from models import storage

app = Flask(__name__)
cors = CORS(app, ressources={"/*:": {"origins:" "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def tear_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """errorhandle : No found"""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0,0,0,0"),
            port=int(os.getenv("HBNB_API_PORT", "5000")))
