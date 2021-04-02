import json
import requests
import urllib

from src.config import url


###############################################################################
#                               HELPER FUNCTIONS                              #
###############################################################################


def user_body(num):
    return {
        "email": f"example{num}@hotmail.com",
        "password": f"password{num}",
        "name_first": f"first_name{num}",
        "name_last": f"last_name{num}"
    }

def dm_create_body(user, u_ids): 
    u_ids_list = [u_id['auth_user_id'] for u_id in u_ids]
    return {
        "token": user["token"],
        "u_ids": u_ids_list
    }

def dm_invite_body(user1, dm, user2):
    return {
        "token": user1["token"],
        "dm_id": dm["dm_id"],
        "u_id": user2["auth_user_id"]
    }

def dm_messages_body(user, dm, start):
    return {
        "token": user["token"],
        "dm_id": dm["dm_id"],
        "start": start
    }

def message_senddm_body(user, dm, message):
    return {
        "token": user["token"],
        "dm_id": dm["dm_id"],
        "message": message
    }

def set_up_data():
    requests.delete(f"{url}clear/v1")
    
    a_u_id0 = requests.post(f"{url}auth/register/v2", json=user_body(0))
    user0 = a_u_id0.json()

    a_u_id1 = requests.post(f"{url}auth/register/v2", json=user_body(1))
    user1 = a_u_id1.json()

    dm_id0 = requests.post(f"{url}dm/create/v1", json=dm_create_body(user0, [user1]))
    dm0 = dm_id0.json()

    setup = {
        'user0': user0['token'],
        'user1': user1['token'],
        'dm0': dm0['dm_id']
    }

    return setup

def send_x_message(user, dm, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user, dm, str(message_num)))
        message_count += 1

def send_x_messages_two_users(user1, user2, dm, num_messages):
    message_count = 0
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm, str(message_num)))
        else:
            requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user2, dm, str(message_num)))
        message_count += 1


###############################################################################
#                             END HELPER FUNCTIONS                            #
###############################################################################



###############################################################################
#                                   TESTING                                   #
###############################################################################

############################# EXCEPTION TESTING ###############################

# Testing for when the user is not part of the dm (testing Access Error)
def test_dm_messages_v1_AccessError():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']
    a_u_id2 = requests.post(f"{url}auth/register/v2", json=user_body(2))
    user2 = a_u_id2.json()
    
    # Add 1 message to dm0
    send_x_message(user0, dm0, 1)

    # user2 is not part of dm0 - should raise an access error
    r = requests.get(f"{url}dm/messages/v1", json=dm_messages_body(user2, dm0, 0))
    dm_messages = r.json()

    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"
    
# Testing for when an invalid dm_id is used (testing input error)
def test_dm_messages_v1_InputError_invalid_dm():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']
    
    # Add 1 message to dm0
    send_x_message(user0, dm0, 1)

    # 2 is an invalid dm_id in this case
    r = requests.get(f"{url}dm/messages/v1", json=dm_messages_body(user0, 2, 0))
    dm_messages = r.json()

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"

# Testing for when an invalid start is used (start > num messages in dm)
def test_dm_messages_v1_InputError_invalid_start():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']

    # Add 1 message to dm1
    send_x_message(user0, dm0, 1)

    r = requests.get(f"{url}dm/messages/v1", json=dm_messages_body(user0, dm0, 2))
    dm_messages = r.json()

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p></p>"


############################ END EXCEPTION TESTING ############################


############################ TESTING DM MESSAGES ##############################


# Testing for when there are no messages - should return {'messages': [], 'start': 0, 'end': -1}
# ASSUMPTION: No messages mean that the most recent message has been returned - therefore end = -1
def test_dm_messages_v1_no_messages():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']

    r = requests.get(f"{url}dm/messages/v1", json=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages == {'messages': [], 'start': 0, 'end': -1}, "No messages - should return end: -1"

# Testing to see if the function is working for a single message
def test_dm_messages_v1_1_message():
    setup = set_up_data()
    data = retrieve_data()
    user0, dm0 = setup['user0'], setup['dm0']

    send_x_message(user0, dm0, 1)

    r = requests.get(f"{url}dm/messages/v1", json=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages == {
        'messages': ["1"], 'start': 0, 'end': -1
    }