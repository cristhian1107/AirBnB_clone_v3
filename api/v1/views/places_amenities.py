#!/usr/bin/python3
""" Methos API for object Place-Amenities """
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models import place
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route("/places/<place_id>/amenities", methods=["GET"],
                 strict_slashes=False)
def get_place_amenity(place_id):
    """ Get Amenities objects of Places """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        return jsonify([amenity.to_dict() for amenity in place.amenities])

    return jsonify(
        [storage.get(Amenity, id).to_dict() for id in place.amenity_ids]
        )


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """ Delete a Amenity object """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == "db":
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ Create a new Amenity object """
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if not place or not amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity.id in place.amenity_id:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
