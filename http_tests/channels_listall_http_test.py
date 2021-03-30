from http_tests import * # import fixtures for pytest

# error when listing channels with an invalid token
def test_channels_listall_invalid_user(client, setup_user_data):
    users = setup_user_data

    # Invalidate an existing token to guarantee a token is invalid 
    invalid_token = users['user1']['token']
    client.post('/logout', json={
        'token': invalid_token
    })

    # Ensure AccessError
    assert client.post('/listall', json={
        'token': invalid_token,
    }).status_code == 405

# listing channels with none created
def test_channels_listall_empty(client, setup_user_data):
    users = setup_user_data

    assert client.post('/listall', json={
        'token': users['user1']['token'],
    }).get_json() == {'channels': []}

# listing a single channel
def test_channels_listall_single(client, setup_user_data):
    users = setup_user_data

    # Creating a basic public channel
    channel_id = client.post('/create', json={
        'token': users['user1']['token'],
        'name': 'Basic Stuff',
        'is_public': True,
    }).get_json()

    # ensure channels_listall returns correct values
    channel_list = client.post('/listall', json={
        'token': users['user1']['token'],
    }).get_json()

    assert channel_list['channels'][0]['channel_id'] == channel_id['channel_id']
    assert channel_list['channels'][0]['name'] == 'Basic Stuff'

# listing multiple channels
def test_channels_listall_multiple(client, setup_user_data):

    users = setup_user_data

    channel_id3 = client.post('/create', json={
        'token': users['user3']['token'],
        'name': 'Public3',
        'is_public': True,
    }).get_json()

    channel_id4 = client.post('/create', json={
        'token': users['user2']['token'],
        'name': 'Private4',
        'is_public': False,
    }).get_json()

    channel_id5 = client.post('/create', json={
        'token': users['user1']['token'],
        'name': 'Public5',
        'is_public': True,
    }).get_json()

    # ensure channels_listall returns correct values
    channel_list = client.post('/listall', json={
        'token': users['user1']['token'],
    }).get_json()

    assert channel_list['channels'][0]['channel_id'] == channel_id3['channel_id']
    assert channel_list['channels'][0]['name'] == 'Public3'

    assert channel_list['channels'][1]['channel_id'] == channel_id4['channel_id']
    assert channel_list['channels'][1]['name'] == 'Private4'

    assert channel_list['channels'][2]['channel_id'] == channel_id5['channel_id']
    assert channel_list['channels'][2]['name'] == 'Public5'