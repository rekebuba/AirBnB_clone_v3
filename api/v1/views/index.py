#!/usr/bin/python3
""" Index """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """return the status of API"""
    return jsonify({"status": "ok"})


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    result = {}
    for value in storage.all().values():
        result[value.__class__.__name__] = storage.count(
                                                value.__class__.__name__
                                            )

    return jsonify(result)
