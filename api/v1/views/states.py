#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify, abort
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
def id_states(id):
    """Retrieves a State object based on id"""
    try:
        result = BaseModel.to_dict(
            storage.all(State)["State." + id]
        )
    except:
        abort(404)
    return jsonify(result)

@app_views.route('/states/<id>', methods=['DELETE'])
def delete_state(id):
    """Deletes a State object based on id"""
    try:
        result = storage.all(State)["State." + id]
        storage.delete(result)
        storage.reload()
    except:
        abort(404)
    return jsonify({})
