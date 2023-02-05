#!/usr/bin/python3
"""View module for Place objects - handles all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_city_places(city_id):
    """retrieves a list of all Place objects of a City."""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    all_places = [place.to_dict() for place in city.places]
    return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a single place object."""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes a place object."""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object."""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    try:
        place_data = request.get_json()
        for key, val in place_data.items():
            if key not in ['id', 'user_id', 'city_id', 'created_at',
                           'updated_at']:
                setattr(place, key, val)
    except (BadRequest, AttributeError):
        return jsonify({"message": "Not a JSON"}), 400
    place.save()
    return jsonify(place.to_dict()), 200
