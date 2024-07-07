#!/usr/bin/python3
"""
    Module of the App
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    """Method to call storage.close()"""
    storage.close()


@app.error_handler(404)
def errorhdn():
    """404 error handler"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    app.run(host=os.getenv("HBNB_API_HOST", "0.0.0.0"),
            port=os.getenv("HBNB_API_PORT", "5000"),
            threaded=True, debug=False)
