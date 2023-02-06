#!/usr/bin/python3
"""The API module for the project's part 3"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins='*')
app.register_blueprint(app_views)

# app.config['JSON_PRETTYPRINT_REGULAR'] = True
# app.json.compact = False -> will change to this in the future


@app.teardown_appcontext
def do_teardown(exception):
    """Calls close() for this app's context"""
    storage.close()


@app.errorhandler(404)
def error(e):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', "0.0.0.0")
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port)
