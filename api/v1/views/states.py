#!/usr/bin/python3

from datetime import datetime
import models
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.state import State

@app_views.route('/states', strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects"""
    lists = []
    for value in storage.all(State).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)

@app_views.route('/states/<state_id>')
def id_state(state_id):
    """Retrieves a State object based on id"""
    try:
        result = BaseModel.to_dict(
            storage.get(State, state_id)
        )
    except:
        abort(404)

    return jsonify(result)

@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object based on id"""
    if models.storage_t == 'db':
        storage._DBStorage__session.query(State).filter(State.id == state_id).delete()
    else:
        del storage._FileStorage__objects['State' + '.' + state_id]

    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new State"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif 'name' not in request.json:
        abort(400, description="Missing name")        
    
    new_obj = State(**request.json)
    BaseModel.save(new_obj)

    result = BaseModel.to_dict(storage.get(State, new_obj.id))
    
    return make_response(jsonify(result), 201)

@app_views.route('/states/<state_id>', methods=['PUT'])
def put_state(state_id):
    """Updates a State object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    object = storage.get(State, state_id)
    if object is None:
        abort(404)

    request.json['updated_at'] = datetime.utcnow()
    
    if models.storage_t == 'db':
        storage._DBStorage__session.query(State).filter(State.id == state_id).update(request.json)
    else:
        result = storage._FileStorage__objects['State' + '.' + state_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in ['id', 'state_id' 'created_at', 'updated_at']:
                setattr(result, key, value)
    
    storage.save()
    result = BaseModel.to_dict(storage.get(State, state_id))

    return make_response(jsonify(result), 200)