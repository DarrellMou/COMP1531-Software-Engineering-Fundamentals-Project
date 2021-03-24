import pytest

from src.error import InputError
from src.auth import auth_login_v1, auth_email_format, auth_register_v1
from src.data import retrieve_data
from src.other import clear_v1

#from error import InputError
#from auth import auth_login_v1, auth_email_format, auth_register_v1
#from data import clear_v1, retrieve_data


def setup_user():
    clear_v1()

    a_u_id1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    a_u_id2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user1_first', 'user1_last')
    a_u_id3 = auth_register_v1('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    a_u_id4 = auth_register_v1('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')
    a_u_id5 = auth_register_v1('user5@email.com', 'User5_pass!', 'user5_first', 'user5_last')

    return {
        'user1' : a_u_id1,
        'user2' : a_u_id2,
        'user3' : a_u_id3,
        'user4' : a_u_id4,
        'user5' : a_u_id5
    }


def test_auth_email_format():
    assert auth_email_format('123@gmailcom') == False, 'invalid email format'
    assert auth_email_format('jsfdsfdsds123.con') == False, 'invalid email format'
    assert auth_email_format('myvalidemail@yahoogmail.com') == True, 'valid email format'

def test_auth_login_v1():
    users = setup_user()

    assert auth_login_v1('user1@email.com', 'User1_pass!') == users['user1'], 'login function broken'
    with pytest.raises(InputError):
        auth_login_v1('nonexistentKey@gmail.com', 'notimportantpasswd') # can't find a match
    with pytest.raises(InputError):
        auth_login_v1('jsfdsfdsds123.con', '123456') # invalid email format 

def test_auth_register_v1():
    clear_v1()
    data = retrieve_data()

    a_u_id = auth_register_v1('example1@hotmail.com', 'password1', 'bob', 'builder')
    assert data['users'][a_u_id['auth_user_id']]['handle_str'] == 'bobbuilder'
    with pytest.raises(InputError):
        auth_register_v1('example1@hotmail.com', 'password1', 'test', 'user1') # duplicate key(email)
    with pytest.raises(InputError):
        auth_register_v1('sampleemail1gmail.com', 'password1', 'test', 'user1') # invalid email format 
    with pytest.raises(InputError):
        auth_register_v1('sampleemail2@gmail.com', '12345', 'test', 'user1') # password too short, less than 6 chars
    with pytest.raises(InputError):
        auth_register_v1('sampleemail2@gmail.com', 'passwo', '', 'user1') # invalid firstname length 

def test_auth_register_v1_nonunique_handle():
    users = setup_user()
    data = retrieve_data()
    assert data['users'][users['user1']['auth_user_id']]['handle_str'] == 'user1_firstuser1_las'
    assert data['users'][users['user2']['auth_user_id']]['handle_str'] == 'user1_firstuser1_las0'

def test_check_auth_permissions():
    users = setup_user()
    data = retrieve_data()
    assert data['users'][users['user1']['auth_user_id']]['permission_id'] == 1
    assert data['users'][users['user2']['auth_user_id']]['permission_id'] == 2
    assert data['users'][users['user3']['auth_user_id']]['permission_id'] == 2
    assert data['users'][users['user4']['auth_user_id']]['permission_id'] == 2
    assert data['users'][users['user5']['auth_user_id']]['permission_id'] == 2
