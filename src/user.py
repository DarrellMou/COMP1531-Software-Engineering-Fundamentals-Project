"""
A user's profile is set when he registers, in auth_register
"""
from flask import jsonify, request, Blueprint, make_response

from src.data import retrieve_data
from src.error import InputError
from src.auth import auth_token_ok, auth_decode_token, auth_email_format


bp = Blueprint('user/profile', __name__, url_prefix='/')


@bp.route('user/profile/v2', methods=['GET'])
def user_profile_v2():

    token = request.json['token']
    u_id = request.json['u_id']
    data = retrieve_data()

    if not auth_token_ok(token):
        raise InputError('invalid token')
    auth_user_id = auth_decode_token(token)

    #if not auth_user_id in data['users']:
    #    raise InputError 

    if not any(x == u_id for x in data['users'].keys()):
        raise InputError('User doesn\'t exist')

    userDict = data['users'][auth_user_id]

    return make_response(jsonify({
            'auth_user_id' : auth_user_id,
            'email'        : userDict['email'],
            'name_first'   : userDict['name_first'],
            'name_last'    : userDict['name_last'],
            'handle_str'   : userDict['handle_str']
           }))


@bp.route('user/profile/setname/v2', methods=['PUT'])
def user_profile_setname_v2():

    data = retrieve_data()

    token = request.json['token']
    name_first = request.json['name_first']
    name_last = request.json['name_last']

    if len(name_first) not in range(1, 50) or len(name_last) not in range(1, 50):
        raise InputError('invalid name length')

    if not auth_token_ok(token):
        raise InputError('invalid token')

    auth_user_id = auth_decode_token(token)

    if auth_user_id in data['users']:
        data['users'][auth_user_id]['name_last'] = name_last
        data['users'][auth_user_id]['name_first'] = name_first

    return make_response(jsonify({}))
