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
        result.append(BaseModel.to_dict(amenity))

    return jsonify(result)
