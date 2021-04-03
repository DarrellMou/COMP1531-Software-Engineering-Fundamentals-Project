import pytest
from src.data import reset_data, retrieve_data
from src.error import InputError, AccessError

from src.auth import auth_register_v2
from src.channel import channel_join_v2, channel_details_v2
from src.channel import channel_addowner_v1
from src.channels import channels_create_v2, channels_list_v2

#Cases start here

#Standard Case, pass expected
def test_standard():
    reset_data()
    a_u_id1 = auth_register_v1('temp1@gmail.com','password1','first1','last1') #auth_user_id1 created
    a_u_id2 = auth_register_v1('temp2@gmail.com','password2','first2','last2') #auth_user_id2 created
    chid1 = channels_create_v2(users[a_u_id1]['token'], 'channel1', True) #Public channel created
    channel_join_v2([a_u_id2]['token'], chid1['channel_id']) #User 2 joins channel 1 as regular member
    
    # Expect a list containing channel 1
    assert channels_list_v2([a_u_id2]['token']) == {
        'channels': [
            {
                'channel_id': chid1['channel_id'],
                'name': 'channel1',
            },
        ],
    }