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

#Standard Case, only one channel joined
def test_standard():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    chid2 = channels_create_v1(a_u_id2['auth_user_id'], 'channel2', True) #Public channel created
    chid3 = channels_create_v1(a_u_id2['auth_user_id'], 'channel3', True) #Public channel created
    #channel_join_v1('auth_user_id2', 'channel_id1')
    
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
        ],
    }
#Case where a user joins multiple channels
def test_multiple_channels():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel1 created
    chid2 = channels_create_v1(a_u_id1['auth_user_id'], 'channel2', True) #Public channel2 created
    chid3 = channels_create_v1(a_u_id1['auth_user_id'], 'channel3', True) #Public channel3 created
    chid4 = channels_create_v1(a_u_id2['auth_user_id'], 'channel4', True) #Public channel3 created
    chid5 = channels_create_v1(a_u_id2['auth_user_id'], 'channel5', True) #Public channel3 created
    chid6 = channels_create_v1(a_u_id2['auth_user_id'], 'channel6', True) #Public channel3 created
    chid7 = channels_create_v1(a_u_id2['auth_user_id'], 'channel7', True) #Public channel3 created
    #channel_join_v1('auth_user_id2', 'channel_id1')
    #channel_join_v1('auth_user_id2', 'channel_id2')
    #channel_join_v1('auth_user_id2', 'channel_id3')

    assert channels_list_v1(a_u_id2['auth_user_id']) == {
        'channels': [
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

#Case where user is valid, but is a member of no channels
def test_memberless():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created

    assert channels_list_v1(a_u_id1['auth_user_id']) == {
        'channels': [],
    }

#Assumptions, users don't have to be in a channel