import pytest

from src.auth import auth_register_v1
from src.channels import channels_listall_v1
from src.error import InputError, AccessError

def test_channels_create_v1():
    
    ## SET-UP USER ## 

    # owner
    a_u_id_1 = auth_register_v1("bye@teams.com", "asdfg", "Brendan", "Ye")
    
    ##             ##

    # list all channels when there are no channels created
    in_channels = channels_listall_v1(a_u_id_1)
    assert len(in_channels['channels']) == 0, "There are no channels"

    # owner creating a public and private channel
    channel_id_1 = channels_create_v1(a_u_id_1, "Public Channel", True)
    channel_id_2 = channels_create_v1(a_u_id_1, "Private Channel", False)

    # list all channels
    in_channels = channels_listall_v1(a_u_id_1)
    assert len(in_channels['channels']) == 2, "There are two channels"

    # invalid auth_user_id
    with pytest.raises(AccessError):
        channels_listall_v1("Invalid auth_user_id")
