from src.data import retrieve_data
from src.auth import auth_decode_token
import uuid

from src.error import InputError, AccessError
from src.auth import auth_token_ok, auth_decode_token

from flask import jsonify, request, Blueprint, make_response
from json import dumps
# bp stands for blueprint, they are components of the DREAMS communication tool
bp = Blueprint('channels', __name__, url_prefix='/')

#################################################################################
#                                FUNCTIONS                                      #
#   * channels_list, channels_listall, channels_create                          #
#                                                                               #                                                                      #
#################################################################################

def channels_list_v1(auth_user_id):
    data = retrieve_data()

    # AccessError occurs when input is invalid auth_user_id
    if auth_user_id not in data['users']: raise AccessError("Invalid token")

    # No parameter errors
    # List of channels
    channel_ids = data['channels']
    channel_list = []

    # Search through individual channels for specific user
    # Go through each channel
    for channel in channel_ids:
        for member in data['channels'][channel]['all_members']:
            if member == auth_user_id:
                # Create a list of channel attributes
                channel_details = {
                    'channel_id' : channel,
                    'name' : data['channels'][channel]['name'],
                }
                channel_list.append(channel_details)
    
    return{
        'channels': channel_list
    }

# 2nd version of channels list that requires authenticated token
def channels_list_v2(token):
    user_id = auth_decode_token(token)
    return channels_list_v1(user_id)

# Provide a list of all channels (and their associated details)
def channels_listall_v2(token):

    data = retrieve_data()
    
    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)


    # Create list of all channels
    channel_listall = []
    for channel in data['channels']:
        channel_details = {
            'channel_id' : channel,
            'name' : data['channels'][channel]['name'],
        }
        channel_listall.append(channel_details)

    return {
        'channels': channel_listall
    }


# Creates a new channel with that name that is either a public or private channel
def channels_create_v2(token, name, is_public):

    data = retrieve_data()

    # InputError occurs when creating a channel name longer than 20 characters
    if len(name) > 20: raise InputError("Channel name cannot be longer than 20 characters")

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Generate unique channel_id
    channel_id = int(uuid.uuid1())

    # Add new channel to channels data
    data['channels'][channel_id] = {
        'name' : name, 
        'is_public' : is_public, 
        'owner_members': [auth_user_id],
        'all_members': [auth_user_id],
        'messages' : [],
    }   

    return {
        'channel_id': channel_id
    }

#################################################################################
#                                API ROUTES                                     #
#   * channels_list, channels_listall, channels_create                          #
#                                                                               #                                                                      #
#################################################################################

@bp.route('create', methods=['POST'])
def create_channels():
    token = request.json['token']
    name = request.json['name']
    is_public = bool(request.json['is_public'])

    responseObj = channels_create_v2(token, name, is_public)

    return dumps(responseObj)

@bp.route('listall', methods=['GET'])
def listall_channels():
    token = request.json['token']

    return dumps(channels_listall_v2(token))

