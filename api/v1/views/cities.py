#!/usr/bin/python3
"""State request management"""
from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State, City
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def getcities(state_id):
    """GET route to return all cities from a state"""
    allcities = []
    states = storage.get(State, state_id)
    if states is None:
        abort(404)
    for cities in states.cities:
        allcities.append(cities.to_dict())
    return jsonify(allcities)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def getcityid(city_id):
    """GET route to return a City by it's id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletecity(city_id):
    """DELETE route to delete a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def createcity(state_id):
    """POST a new City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if request.is_json:
        info = request.get_json()
        if "name" not in info:
            return "Missing name", 400
        info["state_id"] = state_id
        ncity = City(**info)
        storage.new(ncity)
        storage.save()
        return jsonify(ncity.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def updatecity(city_id):
    """PUT updates a city by id"""
    city = storage.get(City, city_id)
    ignore = {"id", "created_at", "updated_at", "state_id"}
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(city, k, v)
        storage.save()
        return jsonify(city.to_dict()), 200
    except Exception:
        if city is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
