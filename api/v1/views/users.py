#!/usr/bin/python3
"""User request management"""
from models import storage
from flask import Flask, jsonify, abort, request
from models.user import User
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/users",
                 methods=["GET"], strict_slashes=False)
def getuser():
    """GET route to return all Users"""
    allusers = []
    users = storage.all(User)
    for user in users.values():
        allusers.append(user.to_dict())
    return jsonify(allusers)


@app_views.route("/users/<user_id>",
                 methods=["GET"], strict_slashes=False)
def getuserid(user_id):
    """GET route to return a User by it's id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>",
                 methods=["DELETE"], strict_slashes=False)
def deleteuser(user_id):
    """DELETE route to delete a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users",
                 methods=["POST"], strict_slashes=False)
def createuser():
    """POST a new User"""
    user = request.get_json()
    if request.is_json:
        if 'email' not in user:
            return "Misiing email", 400
        if 'password' not in user:
            return "Missing password", 400
        newuser = User(**user)
        storage.new(newuser)
        storage.save()
        return jsonify(newuser.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("users/<user_id>",
                 methods=["PUT"], strict_slashes=False)
def updateuser(user_id):
    """PUT updates a city by id"""
    users = storage.get(User, user_id)
    ignore = ["id", "email", "created_at", "updated_at"]
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(users, k, v)
        storage.save()
        return jsonify(users.to_dict()), 200
    except Exception:
        if users is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
