import pytest

from src.error import InputError
from src.auth import auth_login_v1, auth_email_format, auth_register_v1, auth_encode_token, auth_decode_token, auth_token_ok
from src.data import reset_data, retrieve_data
import time

#from error import InputError
#from auth import auth_login_v1, auth_email_format, auth_register_v1
#from data import reset_data, retrieve_data

@pytest.fixture
def test_users():
    reset_data()

    dict1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    dict2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    dict3 = auth_register_v1('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    dict4 = auth_register_v1('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
    dict5 = auth_register_v1('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

    return {
        'login1' : dict1,
        'login2' : dict2,
        'login3' : dict3,
        'login4' : dict4,
        'login5' : dict5
    }


def test_auth_email_format():
    assert auth_email_format('123@gmailcom') == False, 'invalid email format'
    assert auth_email_format('jsfdsfdsds123.con') == False, 'invalid email format'
    assert auth_email_format('myvalidemail@yahoogmail.com') == True, 'valid email format'

def test_auth_login_v1(test_users):
    loginResponse = auth_login_v1('user1@email.com', 'User1_pass!')
    assert loginResponse['auth_user_id'] == test_users['login1']['auth_user_id']

    with pytest.raises(InputError):
        auth_login_v1('nonexistentKey@gmail.com', 'notimportantpasswd') # can't find a match
    with pytest.raises(InputError):
        auth_login_v1('jsfdsfdsds123.con', '123456') # invalid email format 

def test_auth_register_v1():
    data = reset_data()

    registerDict = auth_register_v1('example1@hotmail.com', 'password1', 'bob', 'builder')
    assert data['users'][registerDict['auth_user_id']]['handle_str'] == 'bobbuilder'

    with pytest.raises(InputError):
        auth_register_v1('example1@hotmail.com', 'password1', 'test', 'user1') # duplicate key(email)
    with pytest.raises(InputError):
        auth_register_v1('sampleemail1gmail.com', 'password1', 'test', 'user1') # invalid email format 
    with pytest.raises(InputError):
        auth_register_v1('sampleemail2@gmail.com', '12345', 'test', 'user1') # password too short, less than 6 chars
    with pytest.raises(InputError):
        auth_register_v1('sampleemail2@gmail.com', 'passwo', '', 'user1') # invalid firstname length 

def test_auth_register_v1_nonunique_handle():
    data = reset_data()

    r1 = auth_register_v1('example1@hotmail.com', 'password1', 'bob', 'builder')
    r2 = auth_register_v1('example2@hotmail.com', 'password1', 'bob', 'builder')

    assert data['users'][r1['auth_user_id']]['handle_str'] == 'bobbuilder'
    assert data['users'][r2['auth_user_id']]['handle_str'] == 'bobbuilder0'

def test_check_auth_permissions(test_users):
    data = retrieve_data()

    assert data['users'][test_users['login1']['auth_user_id']]['permission_id'] == 1 # admin
    assert data['users'][test_users['login2']['auth_user_id']]['permission_id'] == 2 # non-admin
    assert data['users'][test_users['login3']['auth_user_id']]['permission_id'] == 2 # etc
    assert data['users'][test_users['login4']['auth_user_id']]['permission_id'] == 2
    assert data['users'][test_users['login5']['auth_user_id']]['permission_id'] == 2

def test_encode_decode_token(test_users):
    token = auth_encode_token(test_users['login1']['auth_user_id'])
    assert isinstance(token, str) == True
    assert auth_decode_token(token) == test_users['login1']['auth_user_id']
    assert auth_decode_token('whatisthis') == 'invalid token, log in again'

    time.sleep(6)
    assert auth_decode_token(token) == 'Session expired, log in again'


def test_auth_token_ok():
    token = auth_encode_token(123)
    assert auth_token_ok(token) == True
    bad_token = 'edaeddawedead'
    assert auth_token_ok(bad_token) == False

