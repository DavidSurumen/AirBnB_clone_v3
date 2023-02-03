#!/usr/bin/python3
"""views module for City objects - handles all default RESTful
API functions.
Import this module in __init__ of this package.
"""
from models import storage
from models.state import State, City
from api.v1.views import app_views
from flask import abort, jsonify
from flask import request
from werkzeug.exceptions import BadRequest


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves the list of all City objects of a State."""
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    all_cities = [city.to_dict() for city in state.cities]
    return jsonify(all_cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    storage.delete(city)
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City object."""
    if storage.get(State, state_id) is None:
        return abort(404)
    try:
        city_args = request.get_json()  # throws BadRequest if Content-Type\
        # of header is not 'application/json'
        if 'name' not in city_args.keys():  # AttributeError if not a dict
            return jsonify({"message": "Missing name"}), 400
        city_args['state_id'] = state_id
    except (BadRequest, AttributeError) as e:
        return jsonify({'message': 'Not a JSON'}), 400
    new_city = City(**city_args)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object, given its id."""
    ct_obj = storage.get(City, city_id)
    if ct_obj is None:
        return abort(404)
    try:
        req_dict = request.get_json()  # could throw BadReuest if no good json
        # found or header Content-Type not application/json

        ct_args = req_dict.items()  # could throw AttributeError
    except (AttributeError, BadRequest):
        return jsonify({'message': 'Not a JSON'}), 400

    for key, val in ct_args:
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(ct_obj, key, val)
    ct_obj.save()
    return jsonify(ct_obj.to_dict()), 200
