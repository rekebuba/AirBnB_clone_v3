#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.review import Review
from models.place import Place
import models
from datetime import datetime

@app_views.route('/cities/<place_id>/reviews')
def reviewInplace(place_id):
    """Retrieves the list of all Review objects of a Place"""
    if not storage.get(Review, place_id):
        abort(404)
    
    lists = []
    for value in storage.all(Place).values():
        if value.place_id == place_id:
            lists.append(BaseModel.to_dict(value))

    return jsonify(lists)

@app_views.route('/reviews', strict_slashes=False)
def all_reviews():
    """Retrieves the list of all Place objects"""
    lists = []
    for value in storage.all(Place).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)

@app_views.route('/reviews/<review_id>')
def place_id(review_id):
    """Retrieves a Place object based on id"""
    try:
        result = BaseModel.to_dict(
            storage.get(Place, review_id)
        )
    except:
        abort(404)
    return jsonify(result)

@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_place(review_id):
    """Deletes a Place object based on id"""
    if models.storage_t == 'db':
        storage._DBStorage__session.query(Place).filter(Place.id == review_id).delete()
    else:
        del storage._FileStorage__objects['Place' + '.' + review_id]

    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/cities/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_place(place_id):
    """Creates a new Place"""
    if not storage.get(Place, place_id):
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    elif 'text' not in request.json:
        abort(400, description="Missing text")
        
        
    # TODO: If the user_id is not linked to any User object, raise a 404 error

    request.json['place_id']  = place_id
    
    new_obj = Place(**request.json)
    BaseModel.save(new_obj)
    
    result = BaseModel.to_dict(storage.get(Place, new_obj.id))
    
    return make_response(jsonify(result), 201)

@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_place(review_id):
    """Updates a Place object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    object = storage.get(Review, review_id)
    if object is None:
        abort(404)
    
    request.json['updated_at'] = datetime.utcnow()
    
    if models.storage_t == 'db':
        storage._DBStorage__session.query(Place).filter(Place.id == review_id).update(request.json)
    else:
        result = storage._FileStorage__objects['Place' + '.' + review_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in ['id', 'city_id' 'created_at']:
                setattr(result, key, value)
    
    storage.save()
    result = BaseModel.to_dict(storage.get(Place, review_id))

    return make_response(jsonify(result), 200)
