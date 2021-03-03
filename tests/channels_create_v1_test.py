import pytest

from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.error import InputError, AccessError

def setup():
    a_u_id_1 = auth_register_v1("bye@teams.com", "asdfg", "Brendan", "Ye")

# error when creating a channel with an invalid auth_user_id
def test_channels_create_access_error():
    with pytest.raises(AccessError):
        channels_create_v1("invalid a_u_id", "Channel", True)

# error when creating a channel name longer than 20 characters
def test_channels_create_input_error():
    with pytest.raises(InputError):
        channels_create_v1("a_u_id_1", "This is longer than 20", True)

# assert channel id is an integer
def test_channels_create_return_value():
    channel_id_1 = channels_create_v1("a_u_id_1", "Public Channel", True)
    assert isinstance(channel_id_1['channel_id'], int)

'''
    # owner creating a public and private channel
    channel_id_1 = channels_create_v1(a_u_id_1, "Public Channel", True)
    channel_id_2 = channels_create_v1(a_u_id_1, "Private Channel", False)

'''
    

    

