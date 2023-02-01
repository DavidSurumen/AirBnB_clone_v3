#!/usr/bin/python3
"""views module for State objects that handles all default
RESTful API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve list of all State objects."""

    states_dct = storage.all(State)
    states_lst = []
    for obj in states_dct.values():
        states_lst.append(obj.to_dict())
    return jsonify(states_lst)


@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieves a single State object by its id."""

    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if state_id is None or state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def create_state():
    """Creates a new state object"""
    try:
        res = request.get_json()
        if 'name' not in res:
            return jsonify({"message": "Missing name"}), 400
        new_state = State(**res)
    except (BadRequest, TypeError) as e:
        return jsonify({"message": "Not a JSON"}), 400

    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """Updates a State object."""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    try:
        res = request.get_json()
        res_items = res.items()
    except (BadRequest, AttributeError) as e:
        return jsonify({"message": "Not a JSON"}), 400

    for key, val in res_items:
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj, key, val)
    obj.save()
    return jsonify(obj.to_dict()), 200
