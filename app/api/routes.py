from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, Player, player_schema, player_schemas


api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/playerinfo', methods = ['POST'])
@token_required
def create_player(current_user_token):
    name = request.json['name']
    team = request.json['team']
    number = request.json['number']
    position = request.json['position']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    player = Player(name, team, number, position, user_token = user_token )

    db.session.add(player)
    db.session.commit()

    response = player_schema.dump(player)
    return jsonify(response)

@api.route('/playerinfo', methods = ['GET'])
@token_required
def get_player(current_user_token):
    a_user = current_user_token.token
    player = Player.query.filter_by(user_token = a_user).all()
    response = player_schemas.dump(player)
    return jsonify(response)




@api.route('/playerinfo/<id>', methods = ['POST','PUT'])
@token_required
def update_player(current_user_token,id):
    player = Player.query.get(id) 
    player.name = request.json['name']
    player.team = request.json['team']
    player.number = request.json['number']
    player.position = request.json['position']
    player.user_token = current_user_token.token

    db.session.commit()
    response = player_schema.dump(player)
    return jsonify(response)


@api.route('/playerinfo/<id>', methods = ['DELETE'])
@token_required
def delete_player(current_user_token, id):
    player = Player.query.get(id)
    db.session.delete(player)
    db.session.commit()
    response = player_schema.dump(player)
    return jsonify(response)