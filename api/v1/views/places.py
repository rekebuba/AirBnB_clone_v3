#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.user import User
from models.place import Place
import models
from datetime import datetime


@app_views.route('/cities/<city_id>/places')
def placeInCity(city_id):
    """Retrieves the list of all Place objects of a City"""
    if not storage.get(City, city_id):
        abort(404)

    lists = []
    for value in storage.all(Place).values():
        if value.city_id == city_id:
            lists.append(BaseModel.to_dict(value))

    return jsonify(lists)

# @app_views.route('/places', strict_slashes=False)
# def all_places():
#     """Retrieves the list of all Place objects"""
#     lists = []
#     for value in storage.all(Place).values():
#         lists.append(BaseModel.to_dict(value))

#     return jsonify(lists)


@app_views.route('/places/<place_id>')
def place_id(place_id):
    """Retrieves a Place object based on id"""
    object = storage.get(Place, place_id)
    if not object:
        abort(404)
    result = BaseModel.to_dict(object)

    return jsonify(result)


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object based on id"""
    place_to_delete = storage.get(Place, place_id)
    if not place_to_delete:
        abort(404)

    storage.delete(place_to_delete)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False
    )
def post_place(city_id):
    """Creates a new Place"""
    if not storage.get(City, city_id):
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif not storage.get(User, request.json['user_id']):
        abort(404)
    elif 'name' not in request.json:
        abort(400, description="Missing name")

    request.json['city_id'] = city_id

    new_obj = Place(**request.json)
    BaseModel.save(new_obj)

    result = BaseModel.to_dict(storage.get(Place, new_obj.id))

    return make_response(jsonify(result), 201)


@app_views.route('/places/<place_id>', methods=['PUT'])
def put_place(place_id):
    """Updates a Place object"""
    if not storage.get(Place, place_id):
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")

    request.json['updated_at'] = datetime.utcnow()

    if models.storage_t == 'db':
        storage._DBStorage__session.query(Place).filter(
            Place.id == place_id).update(request.json)
    else:
        result = storage._FileStorage__objects['Place' + '.' + place_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in [
                    'id', 'user_id', 'city_id' 'created_at']:
                setattr(result, key, value)

    storage.save()
    result = BaseModel.to_dict(storage.get(Place, place_id))

    return make_response(jsonify(result), 200)
