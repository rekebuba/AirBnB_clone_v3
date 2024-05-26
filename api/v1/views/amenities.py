#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.amenity import Amenity
import models
from datetime import datetime


@app_views.route('/amenities', strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    lists = []
    for value in storage.all(Amenity).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)


@app_views.route('/amenities/<amenity_id>')
def amenity_id(amenity_id):
    """Retrieves a Amenity object based on id"""
    object = storage.get(Amenity, amenity_id)
    if not object:
        abort(404)
    result = BaseModel.to_dict(object)

    return jsonify(result)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """Deletes a Amenity object based on id"""
    amenity_to_delete = storage.get(Amenity, amenity_id)
    if not amenity_to_delete:
        abort(404)

    storage.delete(amenity_to_delete)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a new Amenity"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif 'name' not in request.json:
        abort(400, description="Missing name")

    new_obj = Amenity(**request.json)
    BaseModel.save(new_obj)

    result = BaseModel.to_dict(storage.get(Amenity, new_obj.id))

    return make_response(jsonify(result), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    if not storage.get(Amenity, amenity_id):
        abort(404)

    request.json['updated_at'] = datetime.utcnow()

    if models.storage_t == 'db':
        storage._DBStorage__session.query(Amenity).filter(
            Amenity.id == amenity_id).update(request.json)
    else:
        result = storage._FileStorage__objects['Amenity' + '.' + amenity_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in ['id', 'created_at']:
                setattr(result, key, value)

    storage.save()
    result = BaseModel.to_dict(storage.get(Amenity, amenity_id))

    return make_response(jsonify(result), 200)
