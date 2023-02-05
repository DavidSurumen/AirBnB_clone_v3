#!/usr/bin/python3
"""View module for Review objects - handles all default RESTful API actions"""
from api.v1.views import app_views
from models import storage
from models.review import Review
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves list of all Review objects of a Place."""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    reviews_list = [rev.to_dict() for rev in place.reviews]
    return jsonify(reviews_list)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a single review object."""
    rev = storage.get(Review, review_id)
    if rev is None:
        return abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object."""
    rev = storage.get(Review, review_id)
    if rev is None:
        return abort(404)
    storage.delete(rev)
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a Review object."""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    try:
        data = request.get_json()
        if 'user_id' not in data.keys():
            return jsonify({"message": "Missing user_id"}), 400
        if 'text' not in data.keys():
            return jsonify({"message": "Missing text"}), 400
    except (BadRequest, AttributeError):
        return jsonify({"message": "Not a JSON"}), 400
    user = storage.get(User, data.get('user_id'))
    if user is None:
        return abort(404)
    data['user_id'] = user.id
    new_rev = Review(**data)
    return jsonify(new_rev.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object."""
    rev = storage.get(Review, review_id)
    if rev is None:
        return abort(404)
    try:
        data = request.get_json()
        for key, val in data.keys():
            if key not in ['id', 'user_id', 'place_id', 'created_at',
                           'updated_at']:
                setattr(rev, key, val)
    except (BadRequest, AttributeError):
        return jsonify({"message": "Not a JSON"}), 400
    rev.save()
    return jsonify(rev.to_dict()), 200
