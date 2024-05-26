#!/usr/bin/python3
"""City objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.city import City
from models.state import State
import models
from datetime import datetime


@app_views.route('/states/<state_id>/cities')
def cityInState(state_id):
    """Retrieves the list of all City objects of a State"""
    if not storage.get(State, state_id):
        abort(404)

    lists = []
    for value in storage.all(City).values():
        if value.state_id == state_id:
            lists.append(BaseModel.to_dict(value))

    return jsonify(lists)


@app_views.route('/cities', strict_slashes=False)
def all_cities():
    """Retrieves the list of all City objects"""
    lists = []
    for value in storage.all(City).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)


@app_views.route('/cities/<city_id>')
def id_city(city_id):
    """Retrieves a City object based on id"""
    object = storage.get(City, city_id)
    if not object:
        abort(404)
    result = BaseModel.to_dict(object)

    return jsonify(result)


# TODO
@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Deletes a City object based on id"""
    if models.storage_t == 'db':
        storage._DBStorage__session.query(City).filter(
            City.id == city_id).delete()
    else:
        del storage._FileStorage__objects['City' + '.' + city_id]

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def post_city(state_id):
    """Creates a new City"""
    if not storage.get(State, state_id):
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'name' not in request.json:
        abort(400, description="Missing name")

    request.json['state_id'] = state_id

    new_obj = City(**request.json)
    BaseModel.save(new_obj)

    result = BaseModel.to_dict(storage.get(City, new_obj.id))

    return make_response(jsonify(result), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'])
def put_city(city_id):
    """Updates a City object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    object = storage.get(City, city_id)
    if object is None:
        abort(404)

    request.json['updated_at'] = datetime.utcnow()

    if models.storage_t == 'db':
        storage._DBStorage__session.query(City).filter(
            City.id == city_id).update(request.json)
    else:
        result = storage._FileStorage__objects['City' + '.' + city_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in [
                    'id', 'state_id' 'created_at']:
                setattr(result, key, value)

    storage.save()
    result = BaseModel.to_dict(storage.get(City, city_id))

    return make_response(jsonify(result), 200)
