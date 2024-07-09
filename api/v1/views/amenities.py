#!/usr/bin/python3
"""Amenities request management"""
from models import storage
from flask import Flask, jsonify, abort, request
from models.amenity import Amenity
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/amenities",
                 methods=["GET"], strict_slashes=False)
def getamenity():
    """GET route to return all Amenities"""
    allamenities = []
    amenities = storage.all(Amenity)
    for amenity in amenities.values():
        allamenities.append(amenity.to_dict())
    return jsonify(allamenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def getamenityid(amenity_id):
    """GET route to return a Ameinity by it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def deleteamenity(amenity_id):
    """DELETE route to delete a Amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities",
                 methods=["POST"], strict_slashes=False)
def createamenity():
    """POST a new Amenity"""
    amenity = request.get_json()
    if not amenity:
        return "Not a JSON", 400
    if "name" not in amenity:
        return "Missing name", 400
    newamenity = Amenity(**amenity)
    storage.new(newamenity)
    storage.save()
    return jsonify(newamenity.to_dict()), 201


@app_views.route("amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def updateamenity(amenity_id):
    """PUT updates an Amenity by id"""
    amenities = storage.get(Amenity, amenity_id)
    ignore = ["id", "created_at", "updated_at"]
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(amenities, k, v)
        storage.save()
        return jsonify(amenities.to_dict()), 200
    except Exception:
        if amenities is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
