#!/usr/bin/python3
"""Views module for Amenity objects - handles all RESTful API functions."""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves list of all Amenity objects."""
    ameni = storage.all(Amenity)
    ameni_lst = []
    for ob in ameni.values():
        ameni_lst.appent(ob.to_dict())
    return jsonify(ameni_lst)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a single amenity object."""
    am_ob = storage.get(Amenity, amenity_id)
    if am_ob is None:
        return abort(404)

    return jsonify(am_ob.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity object"""
    ameni = storage.get(Amenity, amenity_id)
    if ameni is None:
        return abort(404)
    storage.delete(ameni)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity object."""
    try:
        req = request.get_json()
        if 'name' not in req.keys():
            return jsonify({'message': 'Missing name'}), 400
        new_amen = Amenity(**req)
    except (BadRequest, AttributeError):
        return jsonify({'message': 'Not a JSON'}), 400
    new_amen.save()
    return jsonify(new_amen.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', method=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates given Amenity object."""
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
