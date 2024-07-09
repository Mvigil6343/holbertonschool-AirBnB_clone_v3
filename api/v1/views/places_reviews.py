#!/usr/bin/python3
"""State request management"""
from models import storage
from flask import Flask, jsonify, abort, request
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from api.v1.views import app_views


app = Flask(__name__)


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def getreview(place_id):
    """GET route to return all Reviews from a Place"""
    reviewplaces = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    for review in place.reviews:
        reviewplaces.append(review.to_dict())
    return jsonify(reviewplaces)


@app_views.route("/reviews/<review_id>",
                 methods=["GET"], strict_slashes=False)
def getreviewid(review_id):
    """GET route to return a Review by it's id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def deletereview(review_id):
    """DELETE route to delete a Review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def createreview(place_id):
    """POST a new Review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.is_json:
        info = request.get_json()
        if "user_id" not in info:
            return "Missing user_id", 400
        if storage.get(User, info["user_id"]) is None:
            abort(404)
        if "text" not in info:
            return "Missing text", 400
        newreview = Review(place_id=place_id, **info)
        storage.new(newreview)
        storage.save()
        return jsonify(newreview.to_dict()), 201
    return "Not a JSON", 400


@app_views.route("/reviews/<review_id>",
                 methods=["PUT"], strict_slashes=False)
def updatereview(review_id):
    """PUT updates a Review by id"""
    review = storage.get(Review, review_id)
    ignore = {"id", "user_id", "place_id", "created_at", "updated_at"}
    try:
        info = request.get_json()
        for k, v in info.items():
            if k not in ignore:
                setattr(review, k, v)
        storage.save()
        return jsonify(review.to_dict()), 200
    except Exception:
        if review is None:
            abort(404)
        if not request.is_json:
            return "Not a JSON", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
