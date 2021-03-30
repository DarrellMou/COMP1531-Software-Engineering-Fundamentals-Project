import pytest

from src.auth import auth_register_v1
from src.channel import channel_addowner_v1, channel_invite_v2, channel_join_v2, channel_messages_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.data import retrieve_data
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1, admin_user_remove_v1, admin_userpermission_change_v1

def setup_user():
    clear_v1()

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

# Checks invalid token
def test_admin_userpermission_change_invalid_token():
    users = setup_user()

    with pytest.raises(AccessError):
        admin_userpermission_change_v1("Invalid owner", users['user1']['auth_user_id'],2)

# Checks invalid u_id
def test_admin_userpermission_change_invalid_uid():
    users = setup_user()
    
    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user1']['token'], "Invalid user",2)

# Checks invalid owner access
def test_admin_userpermission_change_invalid_owner():
    users = setup_user()

    with pytest.raises(AccessError):
        admin_userpermission_change_v1(users['user2']['token'], users['user1']['auth_user_id'],2)

# Checks invalid removal as user is the only owner
def test_admin_userpermission_change_only_owner():
    users = setup_user()

    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user1']['token'], users['user1']['auth_user_id'],2)

# Checks basic test of changing a member into owner
def test_admin_userpermission_change_basic():
    users = setup_user()
    data = retrieve_data()

    channel_id1 = channels_create_v2(users['user1']['token'],'Test Channel',True)
    channel_id2 = channels_create_v2(users['user2']['token'],'Test Channel',False)
    channel_join_v2(users['user3']['token'], channel_id1['channel_id'])

    admin_userpermission_change_v1(users['user1']['token'], users['user2']['auth_user_id'], 1)

    assert data['users'][users['user2']['auth_user_id']]['permission_id'] == 1

# Asserts that member turned owner can join private channels and add other owners
def test_admin_userpermission_change_join_private_channels():
    users = setup_user()
    data = retrieve_data()

    # User 1 makes channel 1 and User 3 joins. User 1 sends a message
    channel_id1 = channels_create_v2(users['user1']['token'],'Test Channel',False)
    with pytest.raises(AccessError):
        channel_join_v2(users['user2']['token'], channel_id1['channel_id'])

    # Global User 1 changes Member User 2 into Global owner
    admin_userpermission_change_v1(users['user1']['token'],users['user2']['auth_user_id'],1)

    # Global User 2 should be able to join private channel now
    channel_join_v2(users['user2']['token'],channel_id1['channel_id'])

    # Global User 2 invites User 3
    channel_invite_v2(users['user2']['token'],channel_id1['channel_id'],users['user3']['auth_user_id'])

    # Global User 2 makes User 3 an owner of the channel
    channel_addowner_v1(users['user2']['token'],channel_id1['channel_id'],users['user3']['auth_user_id'])

# Asserts that member turned owner can change the user permission of the original global owner
def test_admin_userpermission_change_ogowner():
    users = setup_user()
    data = retrieve_data()

    # Global User 1 changes Member User 2 into Global owner
    admin_userpermission_change_v1(users['user1']['token'],users['user2']['auth_user_id'],1)
    assert data['users'][users['user2']['auth_user_id']]['permission_id'] == 1

    # Global User 2 changes Member User 1 into member
    admin_userpermission_change_v1(users['user2']['token'],users['user1']['auth_user_id'],2)
    assert data['users'][users['user1']['auth_user_id']]['permission_id'] == 2

    # Global User 2 changes itself into member
    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user2']['token'], users['user2']['auth_user_id'],2)
        