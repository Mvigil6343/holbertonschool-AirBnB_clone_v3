#!/usr/bin/python3

from models import storage
from flask import Flask, jsonify, abort, request
from models.state import State
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def getstates():
    """GET route to return all State"""
    statess = []
    for states in storage.all('State').values():
        statess.append(states.to_dict())
    return jsonify(statess)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def getstatesid(state_id):
    """GET route to return a State by it's id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletestate(state_id):
    """DELETE route to delete a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def createstate():
    """POST a new State"""
    if request.is_json:
        info = request.get_json()
        if "name" not in info:
            return "Missing name", 400
        new = State(**info)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def updatestate(state_id):
    """PUT updates a State by id"""
    state = storage.get(State, state_id)
    ignore = {"id", "created_at", "updated_at"}
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(state, k, v)
        storage.save()
        return jsonify(state.to_dict()), 200
    except Exception:
        if state is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
