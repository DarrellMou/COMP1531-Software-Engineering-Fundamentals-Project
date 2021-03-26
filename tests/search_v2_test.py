import pytest
from src.data import retrieve_data
from src.error import InputError, AccessError
from src.channel import channel_invite_v1 #channel_leave_v1
from src.channels import channels_create_v2
from src.dm import dm_create_v1, dm_leave_v1
from src.message import message_send_v2, message_senddm_v1
from src.other import clear_v1, search_v2

#################################################################################
#                                 Tests search                                  #
#   * uses pytest fixtures from src.conftest                                    #
#                                                                               #                                                                      #
#################################################################################

# Testing for query when a user is not in the channel
def test_search_no_channel(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    assert len(search_v2(user['user2']['token'], 'A message in no channels')) == 0

# Testing the standard case in returning queries for a user in both a channel and a dm
def test_search_standard(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'A message in channels')

    dm_id1 = dm_create_v1(users['user2']['token'], users['user3']['auth_user_id'])
    message_senddm_v1(users['user2']['token'], dm_id1['dm_id'], 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'message')) == 3

# Assumption: search_v2 is case sensitive
# Testing the function returns nothing evne when its the same letters
def test_search_case_sensitive(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'A message in no channels')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'Channels')) == 0

# Testing a query of more than 1000 characters
def test_search_too_long(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
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

# Testing that search_v2 no longer returns the query in the channel the user left
def test_search_leave_channel(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'Welcome to channel')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'Hi channel')

    channel_join_v2(users['user3']['token'], channel_id1)
    message_send_v2(users['user3']['token'], channel_id1, 'Hi channel!')

    dm_id1 = dm_create_v1(users['user2']['token'], users['user3']['auth_user_id'])
    message_senddm_v1(users['user2']['token'], dm_id1['dm_id'], 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'channel')) == 4

    #channel_leave_v1(users['user2']['token'], channel_id1)

    #assert len(search_v2(user['user2']['token'], 'channel')) == 1

# Testing that search_v2 no longer returns the query in the dm the user left
def test_search_leave_dm(setup_user):
    users = setup_user
    channel_id1 = channels_create_v2(users['user1']['token'], "Public Channel", True)
    message_send_v2(users['user1']['token'], channel_id1, 'Welcome to channel')

    channel_invite_v2(users['user1']['token'], channel_id1, users['user2']['auth_user_id'])
    message_send_v2(users['user2']['token'], channel_id1, 'Hi channel')

    channel_join_v2(users['user3']['token'], channel_id1)
    message_send_v2(users['user3']['token'], channel_id1, 'Hi channel!')

    dm_id1 = dm_create_v1(users['user2']['token'], users['user3']['auth_user_id'])
    message_senddm_v1(users['user2']['token'], dm_id1['dm_id'], 'A message in channels')

    assert len(search_v2(user['user2']['token'], 'channel')) == 4

    dm_leave_v1(users['user2']['token'], dm_id1)

    assert len(search_v2(user['user2']['token'], 'channel')) == 3