#!/usr/bin/python3
"""View for the link between Place objects and Amenity objects. -\
handles all RESTful API actions."""
from api.v1.views import app_views
from models import storage
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity
from models import storage_t


if storage_t == 'db':
    # list, create and delete Amenity objects from amenities relationship
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def get_place_amenities(place_id):
        """Retrieves a list of all Amenity objects of a Place."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenities = [amty.to_dict() for amty in place.amenities]
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id, amenity_id):
        """Deletes an Amenity from a Place."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        if amenity.id not in [amty.id for amty in places.amenities]:
            return abort(404)
        storage.delete(amenity)
        return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_placeamenity(place_id, amenity_id):
        """Links an Amenity object to a Place object."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        if amenity in places.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
else:
    # FILE STORAGE
    # list, add and remove Amenity id in the list amenity_ids of a Place obj
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def get_place_amenities(place_id):
        """Retrieves a list of all Amenity objects of a Place."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenities = [ame.to_dict() for ame in place.amenities]
        return jsonify(amenities)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id, amenity_id):
        """Deletes an amenity from a place."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        storage.delete(amenity)
        return jsonify({}), 200

    @app_views.route('places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_placeamenity(place_id, amenity_id):
        """Links an Amenity object to a Place object."""
        place = storage.get(Place, place_id)
        if place is None:
            return abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            return abort(404)
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
        place.save()
        return jsonify(amenity.to_dict()), 201
