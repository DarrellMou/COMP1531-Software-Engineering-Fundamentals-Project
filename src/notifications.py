from src.data import data, retrieve_data
from src.auth import auth_decode_token

def notifications_get_v1(token):
    with open("data.json", "r") as FILE:
        data = json.load(FILE)

    user_id = auth_decode_token(token)

    with open("data.json", "w") as FILE:
        json.dump(data, FILE)
    return {'notifications': data['users'][user_id]['notifications']}
