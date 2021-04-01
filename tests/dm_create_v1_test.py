import pytest

from src.data import retrieve_data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.dm import dm_create_v1
from src.other import clear_v1

# Typical case
def test_function():
    clear_v1()
    data = retrieve_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')

    assert dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id']]) == {
        'dm_id': list(data['dms'].keys())[-1],
        'dm_name': 'first_name1last_name, first_name2last_name'
    }

# dm_create directed to multiple users
def test_multiple():
    clear_v1()
    data = retrieve_data()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')
    a_u_id2 = auth_register_v1('example2@hotmail.com', 'password2', 'first_name2', 'last_name2')
    a_u_id3 = auth_register_v1('example3@hotmail.com', 'password3', 'first_name3', 'last_name3')
    a_u_id4 = auth_register_v1('example4@hotmail.com', 'password4', 'first_name4', 'last_name4')
    a_u_id5 = auth_register_v1('example5@hotmail.com', 'password5', 'first_name5', 'last_name5')
    assert dm_create_v1(a_u_id1['token'], [a_u_id2['auth_user_id'], a_u_id3['auth_user_id'], a_u_id4['auth_user_id'], a_u_id5['auth_user_id']]) == {
        'dm_id': list(data['dms'].keys())[-1],
        'dm_name': 'first_name1last_name, first_name2last_name, first_name3last_name, first_name4last_name, first_name5last_name'
    }

# dm_create given invalid token
def test_invalid_token():
    clear_v1()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')

    with pytest.raises(AccessError):
        dm_create_v1(12345, [a_u_id1['auth_user_id']])

# dm_create given invalid user
def test_invalid_user():
    clear_v1()
    a_u_id1 = auth_register_v1('example1@hotmail.com', 'password1', 'first_name1', 'last_name1')

    with pytest.raises(InputError):
        dm_create_v1(a_u_id1['token'], [12345, 67890])