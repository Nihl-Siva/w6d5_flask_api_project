from functools import wraps

import secrets
from flask import request, jsonify, json

from brick_inventory.models import User

import decimal

import requests


def token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token'].split(' ')[1]
            print(token)

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            our_user = User.query.filter_by(token = token).first()
            print(our_user)
            if not our_user or our_user.token != token:
                return jsonify({'message': 'Token is invalid'})

        except:
            owner = User.query.filter_by(token=token).first()
            if token != owner.token and secrets.compare_digest(token, owner.token):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(our_user, *args, **kwargs)
    return decorated



def random_joke_generator():


    url = "https://random-stuff-api.p.rapidapi.com/joke/random"

    querystring = {"exclude":"None"}

    headers = {
    "Authorization": "2vhFy7Zt8VDC",
    "X-RapidAPI-Key": "dd32d3ce01msh09c4725f53a9d2dp186958jsn12c9c67e941a",
    "X-RapidAPI-Host": "random-stuff-api.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    data = response.json()
    return data['message']

def get_set_info(set_num):
    if "-" not in set_num:
        set_num = f"{set_num}-1"

    headers = {
        'Accept': 'application/json',
        'Authorization': 'key fd058bebd42442a56ad97ef42820df4a'
    }
    url = f'https://rebrickable.com/api/v3/lego/sets/{set_num}/?key=fd058bebd42442a56ad97ef42820df4a'

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return {"error": f"Set not found: {set_num}"}




class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        return super(JSONEncoder, self).default(obj)

