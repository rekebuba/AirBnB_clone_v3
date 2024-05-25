#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.user import User
import models
from datetime import datetime


@app_views.route('/users', strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    lists = []
    for value in storage.all(User).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)

@app_views.route('/users/<user_id>')
def id_user(user_id):
    """Retrieves a User object based on id"""
    try:
        result = BaseModel.to_dict(
            storage.get(User, user_id)
        )
    except:
        abort(404)
    return jsonify(result)

@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object based on id"""
    if models.storage_t == 'db':
        storage._DBStorage__session.query(User).filter(User.id == user_id).delete()
    else:
        del storage._FileStorage__objects['User' + '.' + user_id]

    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a new User"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif 'name' not in request.json:
        abort(400, description="Missing name")
    elif 'password' not in request.json:
        abort(400, description="Mising password")     

    new_obj = User(**request.json)
    BaseModel.save(new_obj)
    
    result = BaseModel.to_dict(storage.get(User, new_obj.id))
    
    return make_response(jsonify(result), 201)

@app_views.route('/users/<user_id>', methods=['PUT'])
def put_user(user_id):
    """Updates a User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    object = storage.get(User, user_id)
    if object is None:
        abort(404)
    
    request.json['updated_at'] = datetime.utcnow()
    
    if models.storage_t == 'db':
        storage._DBStorage__session.query(User).filter(User.id == user_id).update(request.json)
    else:
        result = storage._FileStorage__objects['User' + '.' + user_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in ['id', 'email', 'state_id' 'created_at']:
                setattr(result, key, value)
    
    storage.save()
    result = BaseModel.to_dict(storage.get(User, user_id))

    return make_response(jsonify(result), 200)
