from src.data import data, retrieve_data
from src.auth import auth_decode_token

def notifications_get_v1(token):
    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Create list of all notifications
    #notification_list = data['users'][user_id]['notifications']
    '''
    for notif in data['users'][user_id]['notifications']:
        print(notif)
        print(data)
        notif_details = {
            'channel_id' : notif['channel_id'],
            'dm_id' : notif['dm_id'],
            'notification_message' : notif['notification_message'],
        }
        notification_list.append(notif_details)
    
    return data['users'][user_id]['notifications']
    '''
    return {'notifications': data['users'][user_id]['notifications']}
