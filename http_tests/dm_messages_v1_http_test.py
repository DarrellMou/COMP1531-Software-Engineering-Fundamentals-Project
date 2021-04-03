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
        'user0': user0,
        'user1': user1,
        'dm0': dm0
    }

    return setup

def send_x_message(user, dm, num_messages):
    message_count = 0
    message_id_list = []
    while message_count < num_messages:
        message_num = message_count + 1
        r = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user, dm, str(message_num)))
        message_id = r.json()
        message_id_list.append(message_id["message_id"])
        message_count += 1

    return message_id_list

def send_x_messages_two_users(user1, user2, dm, num_messages):
    message_count = 0
    message_id_list = []
    while message_count < num_messages:
        message_num = message_count + 1
        if message_count % 2 == 0:
            r = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user1, dm, str(message_num)))
        else:
            r = requests.post(f"{url}message/senddm/v1", json=message_senddm_body(user2, dm, str(message_num)))
        message_id = r.json()
        message_id_list.append(message_id["message_id"])
        message_count += 1

    return message_id_list


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
    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user2, dm0, 0))
    dm_messages = r.json()

    assert r.json()["code"] == 403
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p>The user corresponding to the given token is not in the dm</p>"


# Testing for when an invalid dm_id is used (testing input error)
def test_dm_messages_v1_InputError_invalid_dm():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']
    
    # Add 1 message to dm0
    send_x_message(user0, dm0, 1)

    # 2 is an invalid dm_id in this case
    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, {"dm_id": 2}, 0))
    dm_messages = r.json()

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p>dm_id is not valid</p>"

# Testing for when an invalid start is used (start > num messages in dm)
def test_dm_messages_v1_InputError_invalid_start():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']

    # Add 1 message to dm1
    send_x_message(user0, dm0, 1)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 2))
    dm_messages = r.json()

    assert r.json()["code"] == 400
    assert r.json()["name"] == "System Error"
    assert r.json()["message"] == "<p>Inputted starting index is larger than the current number of messages in the dm</p>"


############################ END EXCEPTION TESTING ############################


############################ TESTING DM MESSAGES ##############################


# Testing for when there are no messages - should return {'messages': [], 'start': 0, 'end': -1}
# ASSUMPTION: No messages mean that the most recent message has been returned - therefore end = -1
def test_dm_messages_v1_no_messages():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages == {'messages': [], 'start': 0, 'end': -1}, "No messages - should return end: -1"

# Testing to see if the function is working for a single message
def test_dm_messages_v1_1_message():
    setup = set_up_data()
    user0, dm0 = setup['user0'], setup['dm0']

    message_id_list = send_x_message(user0, dm0, 1)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 0, "Start should not change"
    
    assert dm_messages['end'] == -1, "The most recent message has been reached - return 'end': -1"
    
    assert dm_messages['messages'][0]["message"] == "1"
    assert dm_messages['messages'][0]["message_id"] == message_id_list[0]
    assert dm_messages['messages'][0]["u_id"] == user0["auth_user_id"]
    

# Testing for exactly 50 messages
# ASSUMPTION: 50th message IS the last message so return 'end': -1 rather than 'end': 50
# when there are 50 messages in the dm with start being 0
def test_dm_messages_v1_50_messages():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    # Add 50 messages
    message_id_list = send_x_messages_two_users(user0, user1, dm0, 50)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 0,\
    "Start should not change"
    
    assert dm_messages['end'] == -1,\
    "50th message IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages['messages']) == 50
    
    print(message_id_list)
    #assert dm_messages['messages'][49] == "50", "Error, messages do not match"
    assert dm_messages['messages'][49]["message"] == "1"
    assert dm_messages['messages'][49]["message_id"] == message_id_list[49]
    assert dm_messages['messages'][49]["u_id"] == user0["auth_user_id"]
    
    #assert dm_messages['messages'][34] == "35", "Error, messages do not match"
    assert dm_messages['messages'][34]["message"] == "35"
    assert dm_messages['messages'][34]["message_id"] == message_id_list[34]
    assert dm_messages['messages'][34]["u_id"] == user0["auth_user_id"]
    
    #assert dm_messages['messages'][0] == "1", "Error, messages do not match"
    assert dm_messages['messages'][0]["message"] == "1"
    assert dm_messages['messages'][0]["message_id"] == message_id_list[0]
    assert dm_messages['messages'][0]["u_id"] == user0["auth_user_id"]

'''
# Create 100 messages, with a given start of 50 (50th index means the 51st most
# recent message). Should return 50 messages (index 50 up to index 99 which
# corresponds with the 51st most recent message up to the least recent message,
# i.e. the 100th message) and an end of -1 as per the reasons in the test above
def test_dm_messages_v1_100_messages_start_50():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    # Add 100 messages
    send_x_messages_two_users(user0, user1, dm0, 100)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 50, "Start should not change"
    
    assert dm_messages['end'] == -1, "50th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages['messages']) == 50

    assert dm_messages['messages'][0] == "1"

    assert dm_messages['messages'][49] == "50"

# Given a dm with 10 messages and a start of 9 (10th most recent message
# i.e. the least recent message), return that last message as the only one in
# the messages list and an end of -1
def test_dm_messages_start_is_last_message():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    # Add 10 messages
    send_x_messages_two_users(user0, user1, dm0, 10)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 9))
    dm_messages = r.json()

    assert dm_messages['start'] == 9, "Start should not change"
    
    assert dm_messages['end'] == -1, "10th message from start IS the least recent message so it should return 'end': -1"
    
    assert len(dm_messages['messages']) == 1

    assert dm_messages['messages'] == ["1,2,3,4,5,6,7,8,9,10"]

# Given a start being equal to the number of messages in the given dm,
# return and empty messages list and an end of -1 as per spec and this
# forum post: https://edstem.org/courses/5306/discussion/384787
def test_start_equals_num_messages():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    # Add 10 messages
    send_x_messages_two_users(user0, user1, dm0, 10)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 10))
    dm_messages = r.json()

    assert dm_messages['start'] == 10, "Start should not change"
    
    assert dm_messages['end'] == -1, "No messages so the most recent message has been returned so function should return 'end': -1"
    
    assert len(dm_messages['messages']) == 0

    assert dm_messages['messages'] == []

# Testing for <50 messages (checking if 'end' returns -1)
def test_dm_messages_v1_48_messages():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']
    
    # Add members 1 and 2 into dm 1 and add 48 messages with the message just being the message id
    send_x_messages_two_users(user0, user1, dm0, 48)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 0, "Start should not change"

    assert dm_messages['end'] == -1, "48 < start + 50 so the funtion should return 'end': -1"

    assert dm_messages['messages'][47] == "48"

    assert dm_messages['messages'][0] == "1"

# Testing for >50 messages (checking if the correct final message is returned)
def test_dm_messages_v1_51_messages_start_0():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    send_x_messages_two_users(user0, user1, dm0, 51)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 0, "Start should not change"

    assert dm_messages['end'] == 50, "51 > start + 50 so the funtion should return 'end': 50"

    assert dm_messages['messages'][49] == "50"

    assert dm_messages_v1(user1, dm1, 0)['messages'][0] == "1"

# Testing for >50 messages wit start being 50
def test_dm_messages_v1_51_messages_start_50():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    send_x_messages_two_users(user0, user1, dm0, 51)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 50, "Start should not change"

    assert dm_messages['end'] == -1, "51 < start + 50 so the funtion should return 'end': -1"

    assert len(dm_messages['messages']) == 1

    assert dm_messages['messages'] == ["1"]

# Testing for between 100 and 150 messages with start being 0
def test_dm_messages_v1_111_messages_start_0():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user0, user1, dm0, 111)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 0))
    dm_messages = r.json()

    assert dm_messages['start'] == 0, "Start should not change"

    assert dm_messages_v1['end'] == 50, "111 > start + 50 - function should return 'end': 50"

    assert len(dm_messages['messages']) == 50, "function should return 50 messages max"

    assert dm_messages['messages'][0] == "111"

    assert dm_messages['messages'][25] == "86"

    assert dm_messages['messages'][49] == "61"

# Testing for between 100 and 150 messages with start being 50
def test_dm_messages_v1_111_messages_start_50():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user0, user1, dm0, 111)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 50))
    dm_messages = r.json()

    assert dm_messages['start'] == 50, "Start should not change"

    assert dm_messages['end'] == 100, "111 > start + 50 - function should return 'end': 100"

    assert len(dm_messages['messages']) == 50, "function should return 50 messages max"

    assert dm_messages['messages'][0] == "61"

    assert dm_messages['messages'][25] == "36"

    assert dm_messages['messages'][49] == "12"

# Testing for between 100 and 150 messages with start being 100
def test_dm_messages_v1_111_messages_start_100():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']

    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user0, user1, dm1, 111)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 100))
    dm_messages = r.json()

    assert dm_messages['start'] == 100, "Start should not change"

    assert dm_messages['end'] == -1, "111 < start + 50 - function should return 'end': -1"

    assert len(dm_messages['messages']) == 11, "function should return remaining 11 messages"

    assert dm_messages['messages'][0] == "11"

    assert dm_messages['messages'][5] == "5"

    assert dm_messages['messages'][10] == "1"

# Test for when start is not a multiple of 50 and there are more than 50 messages remaining
def test_dm_messages_v1_start_21():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']
    
    # Add members 1 and 2 into dm 1 and add 111 messages with the message just being the message id
    send_x_messages_two_users(user0, user1, dm0, 111)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 21))
    dm_messages = r.json()

    assert dm_messages['start'] == 21, "Start should not change"

    assert dm_messages['end'] == 71, "End = start + 50 if the least recent message is not returned"

    # The 22nd most recent message of the whole dm is the first one to be returned
    assert dm_messages['messages'][0] == "90"

    assert dm_messages['messages'][25] == "65"

    assert dm_messages['messages'][49] == "41"

# Test for when start is not a multiple of 50 and there are less than 50 messages remaining
def test_dm_messages_v1_start_21_end_neg1():
    setup = set_up_data()
    user0, user1, dm0 = setup['user0'], setup['user1'], setup['dm0']
    
    # Add members 1 and 2 into dm 1 and add 50 messages with the message just being the message id 
    send_x_messages_two_users(user1, user2, dm1, 50)

    r = requests.get(f"{url}dm/messages/v1", params=dm_messages_body(user0, dm0, 21))
    dm_messages = r.json()

    assert dm_messages['start'] == 21, "Start should not change"

    assert dm_messages['end'] == -1, "50 < start + 50 if so return 'end': -1"

    # The 22nd most recent message of the whole dm is the first one to be returned
    # (essentially data['messages'][21] - the 21st index)
    assert dm_messages['messages'][0] == "29"

    assert dm_messages['messages'][25] == "4"
    
    assert dm_messages['messages'][28] == "1"

'''