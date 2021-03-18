def message_send_v1(auth_user_id, channel_id, message):
    return {
        'message_id': 1,
    }

def message_remove_v1(auth_user_id, message_id):
    return {
    }

def message_edit_v1(auth_user_id, message_id, message):
    return {
    }

def message_senddm_v1(token, dm_id, message):

    data = retrieve_data()

    # Checks if dm_id is valid
    if dm_id not in data['dms']: raise InputError

    # Checks if token exists
    if not auth_token_ok(token): raise AccessError
    auth_user_id = auth_decode_token(token)

    # Checks if user belongs in dm
    if auth_user_id not in data['dms'][dm_id]['members']: raise AccessError

    # Checks if message is no more than 1000 characters
    if count(message) > 1000: raise InputError

    return {
    }