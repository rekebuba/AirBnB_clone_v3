#!/usr/bin/python3

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

@app_views.route('/states/<id>', strict_slashes=False)
def id_state(id):
    """Retrieves a State object based on id"""
    try:
        result = BaseModel.to_dict(
            storage.get(State, id)
        )
    except:
        abort(404)
    return jsonify(result)

@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """Deletes a State object based on id"""
    try:
        storage.delete(storage.get(State, id))
        storage.save()
    except:
        abort(404)

    return jsonify({})

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """Creates a new State"""
    try:
        if not request.json or 'name' not in request.json:
            raise
        new_obj = State(**request.json)
        BaseModel.save(new_obj)

        result = BaseModel.to_dict(storage.get(State, new_obj.id))
    except:
        abort(404)
    
    return make_response(jsonify(result), 201)
