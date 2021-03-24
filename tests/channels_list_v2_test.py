import pytest
from src.data import reset_data
from src.data import retrieve_data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.channels import channels_list_v2

#Cases start here

#Standard Case, only part of one channel as owner
def test_standard_owner():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1([a_u_id1]['token'], 'channel1', True) #Public channel created
    chid2 = channels_create_v1([a_u_id2]['token'], 'channel2', True) #Public channel created
    
    # Expect a list containing channel 2
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid2['channel_id'],
                'name': 'channel2',
            },
        ],
    }

#Standard Case pt2, only part of one channel as regular member
def test_standard_regmember():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1([a_u_id1]['token'], 'channel1', True) #Public channel created
    chid2 = channels_create_v1([a_u_id1]['token'], 'channel2', True) #Public channel created
    channel_join_v1([a_u_id2]['token'], chid2['channel_id']) #User 2 joins channel 2 as regular member
    
    # Expect a list containing channel 2
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid2['channel_id'],
                'name': 'channel2',
            },
        ],
    }

#Case where a user is a part of multiple channels as owner
def test_multiple_channels_owner():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    channels_create_v1([a_u_id1]['token'], 'channel1', True) #Public channel1 created, owner: user1
    chid2 = channels_create_v1([a_u_id2]['token'], 'channel2', True) #Public channel2 created, owner: user2
    chid3 = channels_create_v1([a_u_id2]['token'], 'channel3', True) #Public channel3 created, owner: user2
    chid4 = channels_create_v1([a_u_id2]['token'], 'channel4', True) #Public channel4 created, owner: user2
    chid5 = channels_create_v1([a_u_id2]['token'], 'channel5', True) #Public channel5 created, owner: user2
    chid6 = channels_create_v1([a_u_id2]['token'], 'channel6', True) #Public channel6 created, owner: user2
    chid7 = channels_create_v1([a_u_id2]['token'], 'channel7', True) #Public channel7 created, owner: user2

    # Expect a list containing channels 2-7
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid2['channel_id'],
                'name': 'channel2',
            },
            {
                'channel_id': chid3['channel_id'],
                'name': 'channel3',
            },
            {
                'channel_id': chid4['channel_id'],
                'name': 'channel4',
            },
            {
                'channel_id': chid5['channel_id'],
                'name': 'channel5',
            },
            {
                'channel_id': chid6['channel_id'],
                'name': 'channel6',
            },
            {
                'channel_id': chid7['channel_id'],
                'name': 'channel7',
            },
        ],
    }

#Case where a user is a part of multiple channels as owner
def test_multiple_channels_regmember():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    channels_create_v1([a_u_id1]['token'], 'channel1', True) #Public channel1 created, owner: user1
    chid2 = channels_create_v1([a_u_id1]['token'], 'channel2', True) #Public channel2 created, owner: user1
    chid3 = channels_create_v1([a_u_id1]['token'], 'channel3', True) #Public channel3 created, owner: user1
    chid4 = channels_create_v1([a_u_id1]['token'], 'channel4', True) #Public channel4 created, owner: user1
    chid5 = channels_create_v1([a_u_id1]['token'], 'channel5', True) #Public channel5 created, owner: user1
    chid6 = channels_create_v1([a_u_id1]['token'], 'channel6', True) #Public channel6 created, owner: user1
    chid7 = channels_create_v1([a_u_id1]['token']], 'channel7', True) #Public channel7 created, owner: user1
    channel_join_v1([a_u_id2]['token'], chid2['channel_id']) #User 2 joins channel 2 as regular member
    channel_join_v1([a_u_id2]['token'], chid3['channel_id']) #User 2 joins channel 3 as regular member
    channel_join_v1([a_u_id2]['token'], chid4['channel_id']) #User 2 joins channel 4 as regular member
    channel_join_v1([a_u_id2]['token'], chid5['channel_id']) #User 2 joins channel 5 as regular member
    channel_join_v1([a_u_id2]['token'], chid6['channel_id']) #User 2 joins channel 6 as regular member
    channel_join_v1([a_u_id2]['token'], chid7['channel_id']) #User 2 joins channel 7 as regular member

    # Expect a list containing channels 2-7
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid2['channel_id'],
                'name': 'channel2',
            },
            {
                'channel_id': chid3['channel_id'],
                'name': 'channel3',
            },
            {
                'channel_id': chid4['channel_id'],
                'name': 'channel4',
            },
            {
                'channel_id': chid5['channel_id'],
                'name': 'channel5',
            },
            {
                'channel_id': chid6['channel_id'],
                'name': 'channel6',
            },
            {
                'channel_id': chid7['channel_id'],
                'name': 'channel7',
            },
        ],
    }

#Test where the user is a part of multiple channels as an owner and regular member
def test_multiple_channels_mixed():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    channels_create_v1([a_u_id1]['token'], 'channel1', True) #Public channel1 created, owner: user1
    chid2 = channels_create_v1([a_u_id1]['token'], 'channel2', True) #Public channel2 created, owner: user1
    chid3 = channels_create_v1([a_u_id1]['token'], 'channel3', True) #Public channel3 created, owner: user1
    chid4 = channels_create_v1([a_u_id1]['token'], 'channel4', True) #Public channel4 created, owner: user1
    chid5 = channels_create_v1([a_u_id2]['token'], 'channel5', True) #Public channel5 created, owner: user2
    chid6 = channels_create_v1([a_u_id2]['token'], 'channel6', True) #Public channel6 created, owner: user2
    chid7 = channels_create_v1([a_u_id2]['token'], 'channel7', True) #Public channel7 created, owner: user2
    channel_join_v1([a_u_id2]['token'], chid2['channel_id']) #User 2 joins channel 2 as regular member
    channel_join_v1([a_u_id2]['token'], chid3['channel_id']) #User 2 joins channel 3 as regular member
    channel_join_v1([a_u_id2]['token'], chid4['channel_id']) #User 2 joins channel 4 as regular member

    # Expect a list containing channels 2-7
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid2['channel_id'],
                'name': 'channel2',
            },
            {
                'channel_id': chid3['channel_id'],
                'name': 'channel3',
            },
            {
                'channel_id': chid4['channel_id'],
                'name': 'channel4',
            },
            {
                'channel_id': chid5['channel_id'],
                'name': 'channel5',
            },
            {
                'channel_id': chid6['channel_id'],
                'name': 'channel6',
            },
            {
                'channel_id': chid7['channel_id'],
                'name': 'channel7',
            },
        ],
    }

#Case where user is a member of no channels
def test_memberless():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created

    # Expect an empty list
    assert channels_list_v2([a_u_id1]['token']) == {
        'channels': [],
    }

# error when listing a channel with an invalid auth_user_id
def test_channels_list_access_error():

    with pytest.raises(AccessError):
        channels_list_v2("invalid a_u_id")