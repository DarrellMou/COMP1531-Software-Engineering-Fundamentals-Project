# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

from src.data import data, retrieve_data
from src.auth import auth_decode_token

def notifications_get_v1(token):
    data = retrieve_data()
    user_id = auth_decode_token(token)

    return {'notifications': data['users'][user_id]['notifications']}
