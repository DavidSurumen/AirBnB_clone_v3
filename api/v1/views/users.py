#!/usr/bin/python3
"""View for User objects - handles all defaul RESTful API actions."""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id=None):
    """Retrieves a list of all users or one user if id specified."""
    if user_id is None:
        user_ls = [user.to_dict() for user in storage.all(User).values()]
        return jsonify(user_ls)
    user_ls = storage.get(User, user_id)
    if user_ls is None:
        return abort(404)
    return jsonify(user_ls.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user object."""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new User object."""
    try:
        user_data = request.get_json()
        keys = user_data.keys()
        if 'email' not in keys:
            return jsonify({'message': 'Missing email'}), 400
        if 'password' not in keys:
            return jsonify({'message': 'Missing password'}), 400
        new_user = User(**user_data)
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object."""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    try:
        user_data = request.get_json()
        for key, val in user_data.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, val)
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    user.save()
    return jsonify(user.to_dict()), 200
