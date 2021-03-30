from http_tests import * # import fixtures for pytest

def test_channels_create_access_error(client, setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    client.post('/logout', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert client.post('/create', json={
        'token': invalid_token,
        'name': 'Name',
        'is_public': True,
    }).status_code == 403

# error when creating a channel name longer than 20 characters
def test_channels_create_input_error(client, setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    client.post('/logout', json={
        'token': invalid_token
    })

    # public channel with namesize > 20 characters
    client.post('/create', json={
        'token': invalid_token,
        'name': 'wayyyytoolongggggoffffffaaaaaanameeeeeeee',
        'is_public': True,
    }).status_code == 400

    # Ensure input error: private channel with namesize > 20 characters
    client.post('/create', json={
        'token': invalid_token,
        'name': 'wayyyytoolongggggoffffffaaaaaanameeeeeeee',
        'is_public': False,
    }).status_code == 400

# create channels of the same name
def test_channels_create_same_name(client, setup_user_data):

    users = setup_user_data

    channel_id1 = client.post('/create', json={
        'token': users['user1']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).get_json()

    channel_id2 = client.post('/create', json={
        'token': users['user2']['token'],
        'name': "Public Channel",
        'is_public': True,
    }).get_json()

    # ensure channels_listall returns correct values
    channel_list = client.post('/listall', json={
        'token': users['user3']['token'],
    }).get_json()

    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public Channel'

    assert channel_list['channels'][1]['channel_id'] == channel_id2['channel_id']
    assert channel_list['channels'][1]['name'] == 'Public Channel'

# create channel with no name 
def test_channels_create_no_name(client, setup_user_data):

    users = setup_user_data

    channel_id1 = client.post('/create', json={
        'token': users['user1']['token'],
        'name': "",
        'is_public': True,
    }).get_json()

    # ensure channels_listall returns correct values
    channel_list = client.post('/listall', json={
        'token': users['user3']['token'],
    }).get_json()

    assert channel_list['channels'][0]['channel_id'] == channel_id1['channel_id']
    assert channel_list['channels'][0]['name'] == ''

# create channel with valid data
def test_channels_create_valid_basic(client, setup_user_data):
 
    users = setup_user_data

    # Creating a basic public channel
    channel_id = client.post('/create', json={
        'token': users['user1']['token'],
        'name': "Basic Stuff",
        'is_public': True,
    }).get_json()

    # Check that channels_create has returned a valid id (integer value)
    assert isinstance(channel_id['channel_id'], int)

    # Check that channel details have all been set correctly
    channel_details = client.post('/details', json={
        'token': users['user1']['token'],
        'channel_id': channel_id['channel_id'],
    }).get_json()

    assert channel_details['name'] == 'Basic Stuff'
    assert channel_details['owner_members'][0]['u_id'] == users['user1']['u_id']
    assert channel_details['owner_members'][0]['name_first'] == 'user1_first'
    assert channel_details['owner_members'][0]['name_last'] == 'user1_last'
    assert channel_details['all_members'][0]['u_id'] == users['user1']['u_id']
    assert channel_details['all_members'][0]['name_first'] == 'user1_first'
    assert channel_details['all_members'][0]['name_last'] == 'user1_last'




