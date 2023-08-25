#!/usr/bin/python3
"""
app.py to connect to API
"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, make_response
from flask_cors import CORS

app = Flask(__name__)


# Register the blueprint containing the API routes
app.register_blueprint(app_views)


# Setup CORS to allow requests from any origin
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


# Teardown app context to close the database connection
@app.teardown_appcontext
def teardown_appcontext(error):
    """Teardown app context"""
    storage.close()


# Handle 404 errors by returning a JSON response
@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    # Start the Flask app
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')))
            