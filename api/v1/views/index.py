#!/usr/bin/python3
"""index module of the api"""
from api.v1.views import app_views
from flask import jsonify
import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns status OK"""
    return jsonify(status='OK'), 200


@app_views.route('/stats', strict_slashes=False)
def objects():
    """Retrieves the number of each objects by type"""
    return jsonify({
            "amenities": models.storage.count(Amenity),
            "cities": models.storage.count(City),
            "places": models.storage.count(Place),
            "reviews": models.storage.count(Review),
            "states": models.storage.count(State),
            "users": models.storage.count(User)
            })
