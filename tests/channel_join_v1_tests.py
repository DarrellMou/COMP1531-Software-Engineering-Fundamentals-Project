import pytest
from src.data import reset_data
from src.data import retrieve_data

from src.error import InputError
from src.error import AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v1
from src.channel import channel_details_v1
from src.channels import channels_create_v1
from src.channels import channels_list_v1

#Cases start here

#Standard Case, pass expected
def test_standard():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    channel_join_v1(a_u_id2['auth_user_id'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    
    # Expect a list containing channel 1
    assert channels_list_v1(a_u_id2['auth_user_id']) == {
        'channels': [
            {
                'channel_id': chid1['channel_id'],
                'name': 'channel1',
            },
        ],
    }

#Case where a user joins multiple channels
def test_multiple_channels_joined():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel1 created
    chid2 = channels_create_v1(a_u_id1['auth_user_id'], 'channel2', True) #Public channel2 created
    chid3 = channels_create_v1(a_u_id1['auth_user_id'], 'channel3', True) #Public channel3 created
    chid4 = channels_create_v1(a_u_id1['auth_user_id'], 'channel4', True) #Public channel4 created
    channel_join_v1(a_u_id2['auth_user_id'], chid2['channel_id']) #User 2 joins channel 2 as regular member
    channel_join_v1(a_u_id2['auth_user_id'], chid3['channel_id']) #User 2 joins channel 3 as regular member
    channel_join_v1(a_u_id2['auth_user_id'], chid4['channel_id']) #User 2 joins channel 4 as regular member
    

    # Expecting a list containing channels 2-4
    assert channels_list_v1(a_u_id2['auth_user_id']) == {
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
        ],
    }

#Case where multiple users join one channel
def test_multiple_joiners():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    a_u_id3 = auth_register_v1('temp3@gmail.com','password3','first3','last3') #auth_user_id3 created
    a_u_id4 = auth_register_v1('temp4@gmail.com','password4','first4','last4') #auth_user_id4 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel1 created
    channel_join_v1(a_u_id2['auth_user_id'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_join_v1(a_u_id3['auth_user_id'], chid1['channel_id']) #User 3 joins channel 1 as regular member
    channel_join_v1(a_u_id4['auth_user_id'], chid1['channel_id']) #User 4 joins channel 1 as regular member

    # Expecting a owner members including 1, and all members including 1-4
    assert channel_details_v1(a_u_id1['auth_user_id'], chid1['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first1',
                'name_last': 'last1',
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first1',
                'name_last': 'last1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first2',
                'name_last': 'last2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first3',
                'name_last': 'last3',
            },
            {
                'u_id': a_u_id4['auth_user_id'],
                'name_first': 'first4',
                'name_last': 'last4',
            },
        ],
    }

#Case where user attempts to join a private channel (Access Error)
def test_private_channel():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', False) #Private channel created

    with pytest.raises(AccessError):
        channel_join_v1('auth_user_id2', chid1['channel_id']) #Channel_id1 is a private channel

#Case where channel_join is given the id of a non-existent channel
def test_invalid_channel():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created

    with pytest.raises(InputError):
        channel_join_v1('auth_user_id2', 123) #Channel_id2 doesn't exist

#Assumptions, users who are already in a channel will not join it again