import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1, channel_messages_v2
from src.channels import channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.data import reset_data
from src.dm import dm_create_v1
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1, admin_user_remove_v1
from src.user import user_profile_v2

def setup_user():
    reset_data()

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
def test_admin_user_remove_invalid_token():
    users = setup_user()

    with pytest.raises(AccessError):
        admin_user_remove_v1("Invalid owner", users['user1']['u_id'])

# Checks invalid u_id
def test_admin_user_remove_invalid_uid():
    users = setup_user()
    
    with pytest.raises(InputError):
        admin_user_remove_v1(users['user1']['token'], "Invalid user")

# Checks invalid owner access
def test_admin_user_remove_invalid_owner():
    users = setup_user()

    with pytest.raises(AccessError):
        admin_user_remove_v1(users['user1']['token'], users['user2']['u_id'])

# Checks invalid removal as user is the only owner
def test_admin_user_remove_only_owner():
    users = setup_user()
    users['user1']['token']['permission_id'] == 1

    with pytest.raises(InputError):
        admin_user_remove_v1(users['user1']['token'], users['user1']['u_id'])

# Checks invalid removal as user is the only owner
def test_admin_user_remove_only_channel_owner():
    users = setup_user()
    users['user1']['token']['permission_id'] == 1
    users['user2']['token']['permission_id'] == 1
    channel_id1 = channels_create_v1(users['user1']['token'],'Test Channel',True)
    channel_id2 = channels_create_v1(users['user2']['token'],'Test Channel',False)
    channel_join_v1(users['user3']['token'], channel_id1)
    channel_join_v1(users['user1']['token'], channel_id2)

    with pytest.raises(InputError):
        admin_user_remove_v1(users['user1']['token'], users['user2']['u_id'])

# Asserts that user_profile, channel_messages, dm_messages are changed to 'Removed user'
def test_admin_user_remove_only_channel_owner():
    users = setup_user()

    # User 1 and 2 are global owners
    users['user1']['token']['permission_id'] == 1
    users['user2']['token']['permission_id'] == 1

    # User 1 makes channel 1 and User 3 joins. User 1 sends a message
    channel_id1 = channels_create_v1(users['user1']['token'],'Test Channel',True)
    channel_join_v1(users['user3']['token'], channel_id1)
    message_id1 = message_send_v2(users['user1']['token'],channel_id1,'Nice day')

    # User 2 makes channel 2 and User 1 joins. User 1 sends a message
    channel_id2 = channels_create_v1(users['user2']['token'],'Test Channel',False)
    channel_join_v1(users['user1']['token'], channel_id2)
    message_id2 = message_send_v2(users['user1']['token'],channel_id2,'Hello user2')

    # User 1 creates a dm to User 2 and User 3. User 1 sends a message
    dm_id1 = dm_create_v1(users['user1']['token'],[users['user2']['u_id'],users['user3']['u_id']])
    message_dm_id1 = message_senddm_v1(users['user1']['token'],dm_id1,'Hi guys')

    # Set up variables to test function outputs
    user_profile_id1 = user_profile_v2(users['user1']['token'],users['user1']['u_id'])
    messages_channel_id1 = channel_messages_v2(users['user3']['token'],channel_id1,0)
    messages_channel_id2 = channel_messages_v2(users['user2']['token'],channel_id2,0)
    messages_dm_id1 = dm_messages_v1(users['user2']['token'],message_dm_id1,0)
    
    # Ensure the correct output
    assert user_profile_id1['u_id'][0]['first_name'] == "user1_first"
    assert messages_channel_id1['messages'][0]['message'] == "Nice day"
    assert messages_channel_id2['messages'][0]['message'] == "Hello user2"
    assert messages_dm_id1['messages'][0]['message'] == "Hi guys"
    
    # Global User 2 removes Global User 1
    admin_user_remove_v1(users['user2']['token'], users['user1']['u_id'])
    
    # Ensure the correct output after calling admin_user_remove
    assert user_profile_id1['u_id'][0]['first_name'] == "Removed user"
    assert messages_channel_id1['messages'][0]['message'] == "Removed user"
    assert messages_channel_id2['messages'][0]['message'] == "Removed user"
    assert messages_dm_id1['messages'][0]['message'] == "Removed user"
    