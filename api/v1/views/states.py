#!/usr/bin/python3
"""States api"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Récupère la liste de tous les objets State"""
    # Récupère tous les objets State de la db
    states = storage.all(State)
    # Crée une liste vide pr stocker les obj State convertis en dictionnaires
    state_list = []
    # Parcourt tous les obj State
    for state in states.values():
        # Convertit chaque objet State en dict et l'ajoute à la liste
        state_list.append(state.to_dict())
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
    http_body_request = request.get_json
    # Vérifie si les données JSON sont valides
    if http_body_request is None:
        return ({'error': 'Not a JSON'}), 400
    elif "name" not in http_body_request:
        return ({'error': 'Mising name'}), 400
    else:
        # Crée un nouvel objet State avec les données JSON fournies
        new_state = State(name=http_body_request["name"])
        # Ajoute le nouvel objet State à la db
        storage.new(new_state)
        storage.save()
        # Renvoie State converti en dictionnaire en JSON
        return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Met à jour un objet State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    # Vérifie si la requête est au format JSON
    if not request.is_json:
        abort({'error': 'Not a JSON'})
    # Récupère les données JSON de la requête
    http_body_request = request.get_json()
    # Liste des clés à ignorer lors de la mise à jour de State
    ignore_keys = ['id', 'created_at', 'updated_at']
    # Parcourt les K et V du dict des données JSON
    for key, value in http_body_request.items():
        # Vérifie si la clé doit être ignorée
        if key not in ignore_keys:
            # Met à jour l'attribut correspondant de l'objet State avec la nouvelle valeur
            setattr(state, key, value)
    # Enregistre les modifications dans la base de données
    state.save()
    return jsonify(state.to_dict()), 200
