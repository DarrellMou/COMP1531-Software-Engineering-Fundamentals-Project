import src.data

def clear_v1():
    src.data.data = {
        "users" : {},
        "channels" : {},
        "dms": {},
        "messages" : []
    }
    return {}

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
