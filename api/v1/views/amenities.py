#!/usr/bin/python3
"""views module for Amenity objects - handles all default RESTful API
functions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request
from werkzeug.exceptions import BadRequest


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities(amenity_id=None):
    """Retrieve a list of all amenities, or a one specified"""
    if amenity_id is None:
        ameni_lst = [ameni.to_dict() for ameni in
                     storage.all(Amenity).values()]
        return jsonify(ameni_lst)
    ameni_ob = storage.get(Amenity, amenity_id)
    if ameni_ob is None:
        return abort(404)
    return jsonify(ameni_ob.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    ameni = storage.get(Amenity, amenity_id)
    if ameni is None:
        return abort(404)
    storage.delete(ameni)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an Amenity object"""
    try:
        req = request.get_json()
        if 'name' not in req.keys():
            return jsonify({'message': 'Missing name'}), 400
        new_ameni = Amenity(**req)
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    new_ameni.save()
    return jsonify(new_ameni.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """updates given amenity object"""
    amen = storage.get(Amenity, amenity_id)
    if amen is None:
        return abort(404)
    try:
        req = request.get_json()
        for key, val in req.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amen, key, val)
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    amen.save()
    return jsonify(amen.to_dict()), 200
