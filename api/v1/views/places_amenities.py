#!/usr/bin/python3
"""
link between Place objects and Amenity objects
that handles all default RESTFul API actions
"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
import models
from datetime import datetime

@app_views.route('/places/<place_id>/amenities')
def amenityInPlace(place_id):
    """Retrieves the list of all Amenity objects of a Place"""
    if not storage.get(Place, place_id):
        abort(404)

    place = storage.get(Place, place_id)

    result = []
    for amenity in place.amenities:
        result.append(amenity.to_dict())

    return jsonify(result)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',  methods=['DELETE'])
def deleteAmenity(place_id, amenity_id):
    """Deletes a Amenity object by a Place id"""
    if not storage.get(Place, place_id) or not storage.get(Amenity, amenity_id):
        abort(404)

    place = storage.get(Place, place_id)

    result = []
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)

    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/places/<place_id>/amenities/<amenity_id>',  methods=['POST'])
def linkAmenity(place_id, amenity_id):
    """Link a Amenity object to a Place"""
    if not storage.get(Place, place_id) or not storage.get(Amenity, amenity_id):
        abort(404)

    place = storage.get(Place, place_id)

    result = []
    for amenity in place.amenities:
        if amenity.id == amenity_id:
            storage.delete(amenity)

    storage.save()

    return make_response(jsonify({}), 200)
