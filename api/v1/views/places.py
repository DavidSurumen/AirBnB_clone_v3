#!/usr/bin/python3
"""View module for Place objects - handles all default RESTful API actions."""
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
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
    """Retrieves all place objects depending on the body of the request."""
    try:
        req_body = request.get_json()
        if type(req_body) != dict:
            raise AttributeError('Request body not valid json')
    except (BadRequest, AttributeError):
        return jsonify({"message": "Not a JSON"}), 400
    if len(req_body) == 0 or [len(req_body[key]) == 0 for key in
            req_body.keys()]:
        return jsonify(storage.all(Place).values())
    all_cities_id = req_body.get('cities', [])
    states = req_body.get('states')
    if states:
        all_states = [storage.get(State, st_id) for st_id in states]
        all_states = [a for a in all_states if a is not None]
        all_cities_id += [cty.id for st in all_states for cty in st.cities]
    all_cities_id = list(set(all_cities_id))

    all_amenities = req_body.get("amenities")
    all_places = []
    if all_cities_id or all_amenities:
        all_places2 = storage.all(Place).values()
        if all_cities_id:
            all_places2 = [pl for pl in all_places2 if pl.city_id in
                           all_cities_id]
        if all_amenities:
            if storage_t != 'db':
                all_places = [pl for pl in all_places2 if
                              set(all_amenities) <= set(pl.amenities.id)]
            else:
                for e in all_places2:
                    flag = True
                    for a in all_amenities:
                        if a not in [i.id for i in e.amenities]:
                            flag = False
                            break
                    if flag:
                        all_places.append(e)
        else:
            all_places = all_places2
    return jsonify([pl.to_dict() for pl in all_places])
