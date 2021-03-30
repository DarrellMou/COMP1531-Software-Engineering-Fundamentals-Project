import pytest

from src.data import reset_data, data

from src.error import InputError, AccessError

from src.auth import auth_register_v1, auth_decode_token
from src.dm import dm_create_v1, dm_details_v1, dm_invite_v1

# Typical case
def test_function():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    a_u_id3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')

    dm_id = dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']])
    dm_invite_v1(a_u_id1['token'], dm_id['dm_id'], a_u_id3['auth_user_id'])
    
    assert dm_details_v1(a_u_id1['token'], dm_id['dm_id']) == {
        'name': 'first_name1last_name, first_name2last_name',
        'members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            }
        ]
    }

# dm_invite run multiple times
def test_multiple():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    a_u_id3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')
    a_u_id4 = auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4')
    a_u_id5 = auth_register_v1('example5@hotmail.com', 'password5', 'first_name5', 'last_name5')
    dm_id = dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']])

    dm_invite_v1(a_u_id1['token'], dm_id['dm_id'], a_u_id3['auth_user_id'])
    dm_invite_v1(a_u_id1['token'], dm_id['dm_id'], a_u_id4['auth_user_id'])
    dm_invite_v1(a_u_id1['token'], dm_id['dm_id'], a_u_id5['auth_user_id'])
    
    assert dm_details_v1(a_u_id3['token'], dm_id['dm_id']) == {
        'name': 'first_name1last_name, first_name2last_name',
        'members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first_name1',
                'name_last': 'last_name1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first_name2',
                'name_last': 'last_name2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first_name3',
                'name_last': 'last_name3',
            },
            {
                'u_id': a_u_id4['auth_user_id'],
                'name_first': 'first_name4',
                'name_last': 'last_name4',
            },
            {
                'u_id': a_u_id5['auth_user_id'],
                'name_first': 'first_name5',
                'name_last': 'last_name5',
            }
        ]
    }

# dm_invite given invalid token
def test_invalid_token():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    a_u_id3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')

    dm_id = dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']])

    with pytest.raises(AccessError):
        dm_invite_v1(12345, dm_id['dm_id'], a_u_id3['auth_user_id'])

# dm_invite given invalid dm_id
def test_invalid_dm_id():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')

    with pytest.raises(InputError):
        dm_invite_v1(a_u_id1['token'], 12345, a_u_id2['auth_user_id'])

# dm_invite given invalid user
def test_invalid_user():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')

    dm_id = dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']])
    
    with pytest.raises(InputError):
        dm_invite_v1(a_u_id1['token'], dm_id['dm_id'], 12345)

# dm_invite given unauthorised user
def test_unauthorised_user():
    reset_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    a_u_id3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')
    a_u_id4 = auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4')

    dm_id = dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']])
    
    with pytest.raises(AccessError):
        dm_invite_v1(a_u_id3['token'], dm_id['dm_id'], a_u_id4['auth_user_id'])