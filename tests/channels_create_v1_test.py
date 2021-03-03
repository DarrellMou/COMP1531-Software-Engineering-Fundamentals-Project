import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from error import InputError, AccessError

def test_channels_create_v1():
    
    ## SET-UP USER ## 

    # owner
    a_u_id_1 = auth_register_v1("bye@teams.com", "asdfg", "Brendan", "Ye")
    
    ##             ##

    # owner creating a public and private channel
    channel_id_1 = channels_create_v1(a_u_id_1, "Public Channel", True)
    channel_id_2 = channels_create_v1(a_u_id_1, "Private Channel", False)

    # error when creating a channel name longer than 20 characters
    with pytest.raises(InputError):
        channels_create_v1(a_u_id_1, "This is longer than 20", True)

    # error when creating a channel with an invalid auth_user_id
    with pytest.raises(AccessError):
        channels_create_v1("invalid a_u_id", "Channel", True)

