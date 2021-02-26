def test_authorized_user_and_valid_channel_id():
    assert channel_details_v1('darrellmounarath', '1') == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'first_name',
                'name_last': 'last_name',
            }
        ],
        'all_members': [
            {
                'u_id': 3,
                'name_first': 'first_name',
                'name_last': 'last_name',
            }
        ],
    }

def test_authorized_user_and_invalid_channel_id():

def test_unauthorized_user_and_valid_channel_id():

def test_unauthorized_user_and_invalid_channel_id():