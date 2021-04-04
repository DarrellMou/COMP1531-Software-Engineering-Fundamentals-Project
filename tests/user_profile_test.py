import pytest

from src.error import InputError, AccessError
from src.auth import auth_login_v1, auth_email_format, auth_register_v1, auth_encode_token, auth_decode_token, auth_token_ok
from src.user import user_profile_v2, user_profile_setname_v2, user_profile_setemail_v2, user_profile_sethandle_v2, users_all_v1
from src.data import retrieve_data
from src.other import clear_v1
import time

#from error import InputError
#from auth import auth_login_v1, auth_email_format, auth_register_v1
#from data import reset_data, retrieve_data

@pytest.fixture
def test_users():
    clear_v1()

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

# todo: turn all these into normal pytest

def test_user_profile(test_users):
    profile = user_profile_v2(test_users['login1']['token'], test_users['login1']['auth_user_id'])
    assert profile == {'user' : {
                'auth_user_id' :  test_users['login1']['auth_user_id'],
                'email'        : 'user1@email.com',
                'name_first'   : 'user1_first',
                'name_last'    : 'user1_last',
                'handle_str'   : 'user1_firstuser1_las'
                }
           }


def test_user_profile_invalid_token(test_users):
    with pytest.raises(AccessError):
        user_profile_v2('someRandomToken', test_users['login1']['auth_user_id'])


def test_user_profile_invalid_auth_id(test_users):
    with pytest.raises(InputError):
        user_profile_v2(test_users['login1']['token'], 'abcdefg')


def test_user_profile_non_existent_user(test_users):
    with pytest.raises(InputError):
        user_profile_v2(test_users['login1']['token'], test_users['login1']['auth_user_id']+1)


def test_user_profile_setname(test_users):
    resp = user_profile_setname_v2(test_users['login1']['token'], 'changedFirstname', 'changedLastname')
    assert resp == {}

    profile = user_profile_v2(test_users['login1']['token'], test_users['login1']['auth_user_id'])
    assert profile == {'user' : 
                {
                'auth_user_id' :  test_users['login1']['auth_user_id'],
                'email'        : 'user1@email.com',
                'name_first'   : 'changedFirstname',
                'name_last'    : 'changedLastname',
                'handle_str'   : 'user1_firstuser1_las'
                }
           }


def test_user_profile_setname_invalid_token(test_users):
    with pytest.raises(InputError):
        user_profile_setname_v2('someRandomToken', 'changedFirstname', 'changedLastname')


def test_user_profile_setname_invalid_name_length(test_users):
    with pytest.raises(InputError):
        user_profile_setname_v2(test_users['login1']['token'], '', 'changedLastname')


def test_user_profile_setemail(test_users):
    resp = user_profile_setemail_v2(test_users['login1']['token'], 'changedEmail@gmail.com')
    assert resp == {}

    profile = user_profile_v2(test_users['login1']['token'], test_users['login1']['auth_user_id'])
    assert profile == {'user' : 
                {
                'auth_user_id' : test_users['login1']['auth_user_id'],
                'email'        : 'changedEmail@gmail.com',
                'name_first'   : 'user1_first',
                'name_last'    : 'user1_last',
                'handle_str'   : 'user1_firstuser1_las'
                }
           }

def test_user_profile_setemail_invalid_token(test_users):
    with pytest.raises(InputError):
        user_profile_setemail_v2('someRandomToken', 'somevalid12345@gmail.com')


def test_user_profile_setemail_invalid_format(test_users):
    with pytest.raises(InputError):
        user_profile_setemail_v2(test_users['login1']['token'], '@gmail.com')


def test_user_profile_setemail_duplicate(test_users):
    with pytest.raises(InputError):
        user_profile_setemail_v2(test_users['login1']['token'], 'user3@email.com')


def test_user_profile_sethandle_v1(test_users):
    resp = user_profile_sethandle_v2(test_users['login1']['token'], 'changedHandle')
    assert resp == {}

    profile = user_profile_v2(test_users['login1']['token'], test_users['login1']['auth_user_id'])
    assert profile == {'user' : 
                {
                'auth_user_id' : test_users['login1']['auth_user_id'],
                'email'        : 'user1@email.com',
                'name_first'   : 'user1_first',
                'name_last'    : 'user1_last',
                'handle_str'   : 'changedHandle'
                }
           }


def test_user_profile_sethandle_invalid_token(test_users):
    with pytest.raises(InputError):
        user_profile_sethandle_v2('someRandomToken', 'validHandle')


def test_user_profile_sethandle_invalid_format(test_users):
    with pytest.raises(InputError):
        user_profile_sethandle_v2(test_users['login1']['token'], '12')


def test_user_profile_sethandle_duplicate(test_users):
    with pytest.raises(InputError):
        user_profile_sethandle_v2(test_users['login1']['token'], 'user1_firstuser1_las')


def test_users_all_v1(test_users):
    resp = users_all_v1(test_users['login1']['token'])
    assert resp


def test_users_all_v1_invalid_token(test_users):
    with pytest.raises(InputError):
        users_all_v1('someRandomToken')
