#!/usr/bin/python3
"""The API module for the project's part 3"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.teardown_appcontext
def do_teardown(exception):
    """Calls close() for this app's context"""
    storage.close()


@app.errorhandler(404)
def error(e):
    """handler for 404 errors"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST')
    port = getenv('HBNB_API_PORT')

    if host and port:
        app.run(host=host, port=port, threaded=True)
    else:
        app.run(host='0.0.0.0', port=5000, threaded=True)
