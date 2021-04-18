# PROJECT-BACKEND: Team Echo
# Written by Kellen Liew

import pytest
from src.data import retrieve_data
from src.error import InputError, AccessError

from src.auth import auth_register_v1
from src.channel import channel_join_v2, channel_details_v2, channel_addowner_v1, channel_removeowner_v1
from src.channels import channels_create_v2, channels_list_v2
from src.other import clear_v1

#Cases start here

# Non-Dream owner gets dropped
def test_owner_to_member():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }
    channel_removeowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])
    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }

# Owner removes themself
def test_remove_self():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }
    channel_removeowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id1['auth_user_id'])
    assert channel_details_v2(a_u_id1['token'], chid1['channel_id']) == {
        'name': 'channel1',
        'is_public': True,
        'owner_members': [
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            },
        ],
        'all_members': [
            {
                'u_id': a_u_id1['auth_user_id'],
                'email': 'temp1@gmail.com',
                'name_first': 'first1',
                'name_last': 'last1',
                'handle_str': 'first1last1'
            },
            {
                'u_id': a_u_id2['auth_user_id'],
                'email': 'temp2@gmail.com',
                'name_first': 'first2',
                'name_last': 'last2',
                'handle_str': 'first2last2'
            }
        ],
    }

# InputError-Channel ID is invalid
def test_invalid_channel():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])
    
    with pytest.raises(InputError):
        channel_removeowner_v1(a_u_id1['token'], -1111, a_u_id2['auth_user_id'])

# InputError-u_id is not an owner
def test_invalid_uid():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member

    with pytest.raises(InputError):
        channel_removeowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id2['auth_user_id'])

# InputError-auth_user is the only current owner
def test_sole_owner():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_join_v2(a_u_id2['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member

    with pytest.raises(InputError):
        channel_removeowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id1['auth_user_id'])

# AccessError-Authorised user is neither an owner of Dreams or the channel
def test_invalid_auth_user():
    clear_v1()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    a_u_id3 = auth_register_v1('temp3@gmail.com','password3','first3','last3') #auth_user_id2 created
    chid1 = channels_create_v2(a_u_id1['token'], 'channel1', True) #Public channel created
    channel_addowner_v1(a_u_id1['token'], chid1['channel_id'], a_u_id3['auth_user_id'])
    
    with pytest.raises(AccessError):
        channel_removeowner_v1(a_u_id2['token'], chid1['channel_id'], a_u_id3['auth_user_id'])
