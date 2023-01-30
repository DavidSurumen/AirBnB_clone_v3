#!/usr/bin/python3
"""index module of the api"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """Returns status OK"""
    return jsonify(status='OK'), 200
