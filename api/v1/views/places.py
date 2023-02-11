#!/usr/bin/python3
"""View module for Place objects - handles all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.user import User
from models.amenity import Amenity
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


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a Place object for a City object."""
    city = storage.get(City, city_id)
    if city is None:
        return abort(404)
    try:
        req_body = request.get_json()
        if 'user_id' not in req_body.keys():
            return jsonify({'message': 'Missing user_id'}), 400
        if 'name' not in req_body.keys():
            return jsonify({'message': 'Missing name'}), 400
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    user_id = req_body.get('user_id')
    if storage.get(User, user_id) is None:
        return abort(404)
    req_body['city_id'] = city_id
    place = Place(**req_body)
    return jsonify(place.to_dict()), 201


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def retrieve_all_places():
    """Retrieves all place objects depending on the body of the JSON in the
    body of the request."""
    if request.get_json() is None:
        return jsonify({'message': 'Not a JSON'}), 400

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
