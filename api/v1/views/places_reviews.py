#!/usr/bin/python3
"""Review objects that handles all default RESTFul API actions:"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.base_model import BaseModel
from models.review import Review
from models.place import Place
from models.user import User
import models
from datetime import datetime


@app_views.route('/places/<place_id>/reviews')
def reviewInplace(place_id):
    """Retrieves the list of all Review objects of a Place"""
    if not storage.get(Place, place_id):
        abort(404)

    lists = []
    for value in storage.all(Review).values():
        if value.place_id == place_id:
            lists.append(BaseModel.to_dict(value))

    return jsonify(lists)


@app_views.route('/reviews', strict_slashes=False)
def all_reviews():
    """Retrieves the list of all Review objects"""
    lists = []
    for value in storage.all(Review).values():
        lists.append(BaseModel.to_dict(value))

    return jsonify(lists)


@app_views.route('/reviews/<review_id>')
def review_id(review_id):
    """Retrieves a Review object based on id"""
    object = storage.get(Review, review_id)
    if not object:
        abort(404)
    result = BaseModel.to_dict(object)

    return jsonify(result)


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    """Deletes a Review object based on id"""
    if models.storage_t == 'db':
        storage._DBStorage__session.query(Review).filter(
            Review.id == review_id).delete()
    else:
        del storage._FileStorage__objects['Review' + '.' + review_id]

    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'])
def post_review(place_id):
    """Creates a new Review"""
    if not storage.get(Place, place_id):
        abort(404)
    elif not request.is_json:
        abort(400, description="Not a JSON")
    elif 'user_id' not in request.json:
        abort(400, description="Missing user_id")
    elif not storage.get(User, request.json['user_id']):
        abort(404)
    elif 'text' not in request.json:
        abort(400, description="Missing text")

    request.json['place_id'] = place_id

    new_obj = Review(**request.json)
    BaseModel.save(new_obj)

    result = BaseModel.to_dict(storage.get(Review, new_obj.id))

    return make_response(jsonify(result), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def put_review(review_id):
    """Updates a Review object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    elif not storage.get(Review, review_id):
        abort(404)

    request.json['updated_at'] = datetime.utcnow()

    if models.storage_t == 'db':
        storage._DBStorage__session.query(Review).filter(
            Review.id == review_id).update(request.json)
    else:
        result = storage._FileStorage__objects['Review' + '.' + review_id]
        for key, value in request.json.items():
            if hasattr(result, key) and key not in [
                    'id', 'user_id', 'place_id', 'created_at']:
                setattr(result, key, value)

    storage.save()
    result = BaseModel.to_dict(storage.get(Review, review_id))

    return make_response(jsonify(result), 200)
