import pytest

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channels import channels_create_v1, channels_listall_v1
from src.error import InputError, AccessError
from src.data import reset_data

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

# listing channels with invalid token
def test_message_senddm_not_dmmember():

    users = setup_user()

    dm1 = dm_create_v1(users['user1']['token'], users['user2'])

    with pytest.raises(AccessError):
        message_senddm_v1(users['user3']['token'], dm1['dm_id'], "Hello World")

# Message more than 1000 characters
def test_message_senddm_too_long():

    users = setup_user()

    dm1 = dm_create_v1(users['user1']['token'], users['user2'])

    with pytest.raises(InputError):
        message_senddm_v1(users['user1']['token'], dm1['dm_id'], \
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

# Standard send dm
def test_message_senddm_standard():

    users = setup_user()

    dm1 = dm_create_v1(users['user1']['token'], users['user2'])

    with pytest.raises(InputError):
        message_senddm_v1(users['user1']['token'], dm1['dm_id'], "Hello World")
