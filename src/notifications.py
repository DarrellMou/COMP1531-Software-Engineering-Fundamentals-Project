from src.data import data, retrieve_data
from src.auth import auth_decode_token

def notifications_get_v1(token):
    data = retrieve_data()
    user_id = auth_decode_token(token)

    # Create list of all motifications
    notification_list = []
    for notif in data['users'][user_id]['notifications']:
        notif_details = {
            'channel_id' : notif['channel_id'],
            'dm_id' : notif['dm_id'],
            'notification_message' : notif['notification_message'],
        }
        notification_list.append(notif_details)

    return {'notifications': notification_list}