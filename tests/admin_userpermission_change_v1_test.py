# PROJECT-BACKEND: Team Echo
# Written by Nikki Yao

import pytest

from src.channel import channel_addowner_v1, channel_invite_v2, channel_join_v2, channel_details_v2
from src.channels import channels_create_v2
from src.error import InputError, AccessError
from src.data import retrieve_data
from src.dm import dm_create_v1
from src.message import message_send_v2
from src.other import admin_user_remove_v1, admin_userpermission_change_v1

################## Tests admin_userpermission_change #####################
                                                         
#   * uses pytest fixtures from src.conftest                                    
                                                                                                                                                
##########################################################################

# Checks invalid token
def test_admin_userpermission_change_invalid_token(setup_user):
    users = setup_user

    with pytest.raises(AccessError):
        admin_userpermission_change_v1("Invalid owner", users['user1']['auth_user_id'],2)


# Checks invalid u_id
def test_admin_userpermission_change_invalid_uid(setup_user):
    users = setup_user
    
    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user1']['token'], "Invalid user",2)


# Checks invalid owner access
def test_admin_userpermission_change_invalid_owner(setup_user):
    users = setup_user

    with pytest.raises(AccessError):
        admin_userpermission_change_v1(users['user2']['token'], users['user1']['auth_user_id'],2)


# Checks invalid permission_id
def test_admin_userpermission_change_invalid_permissionid(setup_user):
    users = setup_user
    
    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user1']['token'], users['user2']['token'],5)

'''
# Checks invalid removal as user is the only owner
def test_admin_userpermission_change_only_owner(setup_user):
    users = setup_user

    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user1']['token'], users['user1']['auth_user_id'],2)
'''

# Checks basic test of changing a member into owner
def test_admin_userpermission_change_basic(setup_user):
    users = setup_user
    data = retrieve_data()

    admin_userpermission_change_v1(users['user1']['token'], users['user2']['auth_user_id'], 2)

    admin_userpermission_change_v1(users['user1']['token'], users['user2']['auth_user_id'], 1)

    admin_userpermission_change_v1(users['user1']['token'], users['user2']['auth_user_id'], 1)

    assert data['users'][users['user2']['auth_user_id']]['permission_id'] == 1


# Asserts that member turned owner can join private channels and add other owners
def test_admin_userpermission_change_join_private_channels(setup_user):
    users = setup_user

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

    channel_deets_d2 = channel_details_v2(users['user2']['token'],channel_id1['channel_id'])

    assert channel_deets_d2['owner_members'][1]['u_id'] == users['user2']['auth_user_id']
    assert channel_deets_d2['owner_members'][2]['u_id'] == users['user3']['auth_user_id']


# Asserts that member turned owner can change the user permission of the original global owner
def test_admin_userpermission_change_ogowner(setup_user):
    users = setup_user
    data = retrieve_data()

    # Global User 1 changes Member User 2 into Global owner
    admin_userpermission_change_v1(users['user1']['token'],users['user2']['auth_user_id'],1)
    assert data['users'][users['user2']['auth_user_id']]['permission_id'] == 1

    # Global User 2 changes Member User 1 into member
    admin_userpermission_change_v1(users['user2']['token'],users['user1']['auth_user_id'],2)
    assert data['users'][users['user1']['auth_user_id']]['permission_id'] == 2

    '''
    # Global User 2 changes itself into member
    with pytest.raises(InputError):
        admin_userpermission_change_v1(users['user2']['token'], users['user2']['auth_user_id'],2)
    '''
        