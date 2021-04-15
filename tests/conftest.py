# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

import pytest
from src.auth import auth_register_v1
from src.other import clear_v1

'''
The following fixtures are used in:
- channels/create
- channels/listall
- admin/userpermission/change
- admin/user/remove
- search
'''

@pytest.fixture
def reset():
    clear_v1()

@pytest.fixture
def setup_user(reset):

    # a_u_id* has two fields: token and auth_user_id
    a_u_id1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    a_u_id2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
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

@pytest.fixture
def users(reset):

    # a_u_id* has two fields: token and auth_user_id
    a_u_id0 = auth_register_v1('user0@email.com', 'User0_pass!', 'user0_first', 'user0_last')
    a_u_id1 = auth_register_v1('user1@email.com', 'User1_pass!', 'user1_first', 'user1_last')
    a_u_id2 = auth_register_v1('user2@email.com', 'User2_pass!', 'user2_first', 'user2_last')
    a_u_id3 = auth_register_v1('user3@email.com', 'User3_pass!', 'user3_first', 'user3_last')
    a_u_id4 = auth_register_v1('user4@email.com', 'User4_pass!', 'user4_first', 'user4_last')

    return [a_u_id0, a_u_id1, a_u_id2, a_u_id3, a_u_id4]