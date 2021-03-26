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
    }).status_code == 400



