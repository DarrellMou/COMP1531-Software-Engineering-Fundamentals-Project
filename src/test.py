from data import data, reset_data, retrieve_data
from channels import channels_create_v1
from auth import auth_register_v1

'''
def add_simple_data():
    # Populate data
    user1 = {'auth_user_id': 1, 'passwd': 1234, 'handle': 'brendanye'} # Should be using auth_register function but don't have that yet
    user2 = {'auth_user_id': 2, 'passwd': 5678, 'handle': 'bobbuilder'} # Ditto above
    data = retrieve_data()

    data['users'].extend([user1, user2])
    #print(data)
    channel_1 = {'channel_id': 1, 'channel_name': 'channel_1', 'is_public': True,
    'owner': data['users'][0]['auth_user_id'], 'all_members': [{'auth_user_id': 1}], 'messages': []}
    data['channels'].append(channel_1) # Should really be using the channels_create function instead but don't have that yet
    #print(data)
    return data

def add_1_message():
    data = retrieve_data()
    data = {
        "users" : [],
        "channels" : []
    }
    data = add_simple_data()
    #print(data)
    data['channels'][0]['messages'].append({'message_id': 1, 'u_id': 1, 'message': "Test message", 'time_created': 1})

    return data

add_1_message()
print(add_1_message())
'''

'''
add_1_message()
print(data)
print()
print()

def is_valid_channel_id(channel_id):

    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            return True
    
    return False

print(is_valid_channel_id(1))
'''

'''
def test_invalid_start():
    # Add member 1 into channel 1 and add 1 message
    # Data is already reset in add_1_message()
    add_1_message() # Only has 1 message
    add_1_message()
    add_1_message()

    return print(num_messages(1))

#print(test_invalid_start())
'''
def add_1_message(user1, channel1):
    #data = retrieve_data()
    #data = reset_data()
    #data = add_simple_data()
    # Physically creating messages because we don't have message_send available yet
    print("HIHIHI")
    print()
    print()
    print(user1)
    print(channel1)
    print("BBBBBBBBBBBBBBBBBBBbb")
    data = retrieve_data()
    print(data)
    data['channels'][channel1['channel_id']]['messages'].append({'message_id': 1, 'u_id': data['users'][user1['auth_user_id']]['u_id'], 'message': "Test message", 'time_created': 1})
    
    return data

def test_1():
    # Add member 1 into channel 1 and add 1 message
    # Data is already reset in add_1_message()
    data = retrieve_data()
    data = reset_data()
    
    # Populate data - create/register users 1 and 2 and have user 1 make
    # channel1
    user1 = auth_register_v1('bob.builder@email.com', 'badpassword1', 'Bob', 'Builder')
    print(user1)
    user2 = auth_register_v1('shaun.sheep@email.com', 'password123', 'Shaun', 'Sheep')
    print(user2)
    channel1 = channels_create_v1(user1['auth_user_id'], 'Channel1', True)
    print(channel1)

    print()
    print()
    print()
    print(data)

    # Add 1 message to channel1
    data = add_1_message(user1, channel1) # Only has 1 message
    #return data

test_1()
print(data['users'])