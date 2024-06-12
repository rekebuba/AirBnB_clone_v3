#!/usr/bin/python3
"""Status of your API"""

from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

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
    """ Close Storage """
    storage.close()


if __name__ == '__main__':
    """ Main Function """
    HOST = getenv('HBNB_API_HOST') if getenv('HBNB_API_HOST') else '0.0.0.0'
    PORT = getenv('HBNB_API_PORT') if getenv('HBNB_API_PORT') else '5002'
    app.run(host=HOST, port=PORT, threaded=True)
