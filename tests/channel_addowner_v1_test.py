import pytest
from src.data import reset_data, retrieve_data
from src.error import InputError, AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v2, channel_details_v1
from src.channel import channel_addowner_v1
from src.channels import channels_create_v1, channels_list_v2

#Cases start here

# Member made owner
def test_member_to_owner():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    # Expect a list containing channel 1
    assert channel_details_v1(a_u_id1['auth_user_id'], chid1['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first1',
                'name_last': 'last1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first2',
                'name_last': 'last2',
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
            }
        ],
    }

# Outsider made owner
def test_outsider_to_owner():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    assert channel_details_v1(a_u_id1['auth_user_id'], chid1['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'name_first': 'first1',
                'name_last': 'last1',
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first2',
                'name_last': 'last2',
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
            }
        ],
    }

# Dream owner can designate owners for servers not owned
def test_dream_owner():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    a_u_id3 = auth_register_v1('temp3@gmail.com','password3','first3','last3') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id2['auth_user_id'], 'channel1', True) #Public channel created
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id3['auth_user_id'])

    assert channel_details_v1(a_u_id2['auth_user_id'], chid1['channel_id']) == {
        'name': 'channel1',
        'owner_members': [
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first2',
                'name_last': 'last2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first3',
                'name_last': 'last3',
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id2['auth_user_id'],
                'name_first': 'first2',
                'name_last': 'last2',
            },
            {
                'u_id': a_u_id3['auth_user_id'],
                'name_first': 'first3',
                'name_last': 'last3',
            }
        ],
    }

# InputError-Channel ID is invalid
def test_invalid_channel():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    with pytest.raises(InputError):
        channel_addowner_v1(a_u_id1['token'], -1111, a_u_id2['auth_user_id'])

# InputError-u_id is already an owner
def test_invalid_uid():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id2['auth_user_id'], 'channel1', True) #Public channel created
    with pytest.raises(InputError):
        channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

# AccessError-Authorised user is neither an owner of Dreams or the channel
def test_invalid_auth_user():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    a_u_id3 = auth_register_v1('temp3@gmail.com','password3','first3','last3') #auth_user_id2 created
    chid1 = channels_create_v1(a_u_id1['auth_user_id'], 'channel1', True) #Public channel created
    with pytest.raises(AccessError):
        channel_addowner_v1(a_u_id2['token'], chid1['channel_id'], a_u_id3['auth_user_id'])