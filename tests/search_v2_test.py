import pytest
from src.data import reset_data, retrieve_data
from src.error import InputError, AccessError
from src.message import message_send_v2
from src.other import search_v2

def setup_user():
    reset_data()

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

def test_search_no_channel():
    users = setup_user()
    channel_id1 = channels_create_v1(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    assert len(search_v2(user['user2']['token'], 'A message in no channels')) == 0

def test_search_standard():
    users = setup_user()
    channel_id1 = channels_create_v1(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'A message in channels')

    dm_id1 = dm_create_v1(users['user2']['token'], users['user3']['auth_user_id'])
    message_senddm_v1(users['user2']['token'], dm_id1['dm_id'], 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'message')) == 3

def test_search_case_sensitive():
    users = setup_user()
    channel_id1 = channels_create_v1(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'Channels')) == 0

def test_search_too_long():
    users = setup_user()
    channel_id1 = channels_create_v1(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    with pytest.raises(InputError):
        search_v2(user['user2']['token'], 'Channels', \
        "To manage the transition from trimesters to hexamesters in 2020, UNSW has \
         established a new focus on building an in-house digital collaboration and \
         communication tool for groups and teams to support the high intensity \
         learning environment.Rather than re-invent the wheel, UNSW has decided that \
         it finds the functionality of Microsoft Teams to be nearly exactly what it \
         needs. For this reason, UNSW has contracted out Penguin Pty Ltd (a small \
         software business run by Hayden) to build the new product. In UNSW's attempt \
         to try and add a lighter not to the generally fatigued and cynical student \
         body, they have named their UNSW-based product UNSW Dreams (or just Dreams \
         for short). UNSW Dreams is the communication tool that allows you to share, \
         communication, and collaborate to (attempt to) make dreams a reality.Penguin \
         Pty Ltd has sub-contracted two software firms: BlueBottle Pty Ltd (two \
         software developers, Andrea and Andrew, who will build the initial web-based \
         GUI), YourTeam Pty Ltd (a team of talented misfits completing COMP1531 in \
         21T1), who will build the backend python server and possibly assist in the \
         GUI later in the project")
