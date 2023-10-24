#!/usr/bin/python3
"""States api"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Récupère la liste de tous les objets State"""
    # Récupère tous les objets State de la db
    all_states = storage.all(State).values()
    state_list = [state.to_dict() for state in all_states]
    # Renvoie la liste de dictionnaires en JSON
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Récupère un objet State"""
    # Récupère l'objet State correspondant à l'ID
    state = storage.get(State, state_id)
    # Vérifie si l'objet State existe
    if state is None:
        abort(404)
    # Retourne State converti en dictionnaire sous forme de réponse JSON
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Supprime un objet State"""
    # Récupère l'objet State correspondant à l'ID
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200

@app_views.route("/states", methods=["POST"])
def create_state():
    """Crée un nouvel objet State"""
    # Récupère les données JSON de la requête
    http_body_request = request.get_json()
    # Vérifie si les données JSON sont valides
    if http_body_request is None:
        abort(400, 'Not a JSON')
    if "name" not in http_body_request.key():
        abort(400, 'Missing name')
        # Crée un nouvel objet State avec les données JSON fournies
    new_state = State(name=http_body_request["name"])
    # Ajoute le nouvel objet State à la db
    storage.new(new_state)
    storage.save()
    # Renvoie State converti en dictionnaire en JSON
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    http_body_request = request.get_json()
    if http_body_request is None:
        abort(400, "Not a JSON")
    ignore_key = ['id', 'created_at', 'updated_at']
    for key, value in http_body_request.items():
        if key not in ignore_key:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200