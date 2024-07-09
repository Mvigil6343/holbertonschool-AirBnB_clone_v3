#!/usr/bin/python3
"""State request management"""
from models import storage
from flask import Flask, jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User

from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def getplace(city_id):
    """GET route to return all Places from a city"""
    allplaces = []
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for place in city.places:
        allplaces.append(place.to_dict())
    return jsonify(allplaces)


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def getplaceid(place_id):
    """GET route to return a Place by it's id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def deleteplace(place_id):
    """DELETE route to delete a Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def createplace(city_id):
    """POST a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.is_json:
        info = request.get_json()
        if "user_id" not in info:
            return "Missing user_id", 400
        if storage.get(User, info["user_id"]) is None:
            abort(404)
        if "name" not in info:
            return "Missing name", 400
        newplace = Place(city_id=city_id, **info)
        storage.new(newplace)
        storage.save()
        return jsonify(newplace.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/places/<place_id>",
                 methods=["PUT"], strict_slashes=False)
def updateplace(place_id):
    """PUT updates a Place by id"""
    place = storage.get(Place, place_id)
    ignore = {"id", "user_id", "city_id", "created_at", "updated_at"}
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(place, k, v)
        storage.save()
        return jsonify(place.to_dict()), 200
    except Exception:
        if place is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
