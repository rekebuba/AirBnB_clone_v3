#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)

app.register_blueprint(app_views)


@app.errorhandler(404)
def error(error):
    """
    handler for 404 errors that returns a JSON-formatted
    404 status code response
    """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.errorhandler(400)
def error(error):
    """
    handler for 400 errors that returns a JSON-formatted
    400 status code response
    """
    return make_response(jsonify({"error": error.description}), 400)


@app.teardown_appcontext
def tear_stortage(exception):
    storage.close()


if __name__ == '__main__':
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True, debug=True)
