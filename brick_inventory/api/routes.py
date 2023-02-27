from flask import Blueprint, request, jsonify
from brick_inventory.helpers import token_required, random_joke_generator
from brick_inventory.models import db, Brick, brick_schema, bricks_schema


api = Blueprint('api', __name__, url_prefix = '/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


# Create brick Endpoint
@api.route('/bricks', methods = ['POST'])
@token_required
def create_brick(our_user):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    camera_quality = request.json['camera_quality']
    flight_time = request.json['flight_time']
    max_speed = request.json['max_speed']
    dimensions = request.json['dimensions']
    weight = request.json['weight']
    cost_of_production = request.json['cost_of_production']
    series = request.json['series']
    random_joke = random_joke_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    brick = Brick(name, description, price, camera_quality, flight_time, max_speed, dimensions, weight, cost_of_production, series, random_joke, user_token = user_token)

    db.session.add(brick)
    db.session.commit()

    response = brick_schema.dump(brick)

    return jsonify(response)


# Retrieve all brick endpoints
@api.route('/bricks', methods = ['GET'])
@token_required
def get_bricks(our_user):
    owner = our_user.token
    bricks = Brick.query.filter_by(user_token = owner).all()
    response = bricks_schema.dump(bricks)

    return jsonify(response)


# Retrieve One brick endpoint
@api.route('/bricks/<id>', methods = ['GET'])
@token_required
def get_brick(our_user, id):
    owner = our_user.token
    if owner == our_user.token:
        brick = Brick.query.get(id)
        response = brick_schema.dump(brick)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid ID Required'}), 401


# Update Brick Endpoint
@api.route('/bricks/<id>', methods = ['PUT', 'POST'])
@token_required
def update_brick(our_user, id):
    brick = Brick.query.get(id)
    brick.name = request.json['name']
    brick.description = request.json['description']
    brick.price = request.json['price']
    brick.camera_quality = request.json['camera_quality']
    brick.flight_time = request.json['flight_time']
    brick.max_speed = request.json['max_speed']
    brick.dimensions = request.json['dimensions']
    brick.weight = request.json['weight']
    brick.cost_of_production = request.json['cost_of_production']
    brick.series = request.json['series']
    brick.random_joke = random_joke_generator()
    brick.user_token = our_user.token

    db.session.commit()
    response = brick_schema.dump(brick)
    return jsonify(response)

# Delete brick Endpoint
@api.route('/bricks/<id>', methods = ['DELETE'])
@token_required
def delete_brick(our_user, id):
    brick = Brick.query.get(id)
    db.session.delete(brick)
    db.session.commit()

    response = brick_schema.dump(brick)
    return jsonify(response)









