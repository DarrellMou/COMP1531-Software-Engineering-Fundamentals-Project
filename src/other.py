import json

def clear_v1():
    src.data.data = {
        "users" : {},
        "channels" : {},
        "dms" : {},
        "messages" : []
    }
    with open("data.json", "w") as FILE:
        json.dump(data, FILE)

def search_v1(auth_user_id, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'auth_user_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }
