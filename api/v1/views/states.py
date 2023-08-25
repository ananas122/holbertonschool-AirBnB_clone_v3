#!/usr/bin/python3
"""States api"""

from flask import jsonify, abort, request, make_response
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Récupère la liste de tous les objets State"""
    stateList = []
    for state in storage.all(State).values():
        stateList.append(state.to_dict())
    return jsonify(stateList)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                strict_slashes=False)
def get_state(state_id):
    """Récupère un objet State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                strict_slashes=False)
def delete_state(state_id):
    """Supprime un objet State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states/', methods=['POST'],
                strict_slashes=False)
def create_state():
    """Crée un nouvel objet State"""
    http_body_request = request.get_json()
    if http_body_request is None:
        abort(400, 'Not a JSON')
    if "name" not in http_body_request:
        abort(400, 'Missing name')
    new_state = State(name=http_body_request["name"])
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route("/states/", methods=["POST"],
                strict_slashes=False)
def post_state():
    """create a new state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a json"}), 400)
    if "name" not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    state = State(**request.get_json())
    state.save()
    return make_response(jsonify(state.ti_disct()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                strict_slashes=False)
def put_state(state_id):
    """Met à jour un objet State"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for attr, value in request.get_json().items():
        if attr not in ["id", "created_at", "upgrade_at"]:
            setattr(state, attr, value)
    state.save()
    return jsonify(state.to_disct())
