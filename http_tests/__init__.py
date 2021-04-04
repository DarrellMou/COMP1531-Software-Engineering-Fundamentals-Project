import pytest
import requests
import json
from src import config

@pytest.fixture
def reset():
    requests.delete(config.url+'clear/v1')

@pytest.fixture
def setup_user_dict(reset):

    a_u_id1 = {
        'email': 'user1@email.com',
        'password': 'user1_pass!',
        'name_first': 'user1_first',
        'name_last': 'user1_last'
    }

    a_u_id2 = {
        'email': 'user2@email.com',
        'password': 'user2_pass!',
        'name_first': 'user2_first',
        'name_last': 'user2_last'
    }

    a_u_id3 = {
        'email': 'user30@email.com',
        'password': 'user3_pass!',
        'name_first': 'user3_first',
        'name_last': 'user3_last'
    }

    a_u_id4 = {
        'email': 'user4@email.com',
        'password': 'user4_pass!',
        'name_first': 'user4_first',
        'name_last': 'user4_last'
    }
    a_u_id5 = {
        'email': 'user5@email.com',
        'password': 'user5_pass!',
        'name_first': 'user5_first',
        'name_last': 'user5_last'
    }

    return {
        'user1_dict': a_u_id1,
        'user2_dict': a_u_id2,
        'user3_dict': a_u_id3,
        'user4_dict': a_u_id4,
        'user5_dict': a_u_id5
    }


@pytest.fixture
def setup_user_data(setup_user_dict):
    
    user1 = setup_user_dict['user1_dict']
    user1_details = requests.post(config.url + "auth/register/v2", json=user1).json()

    user2 = setup_user_dict['user2_dict']
    user2_details = requests.post(config.url + "auth/register/v2", json=user2).json()

    user3 = setup_user_dict['user3_dict']
    user3_details = requests.post(config.url + "auth/register/v2", json=user3).json()

    user4 = setup_user_dict['user4_dict']
    user4_details = requests.post(config.url + "auth/register/v2", json=user4).json()

    user5 = setup_user_dict['user5_dict']
    user5_details = requests.post(config.url + "auth/register/v2", json=user5).json()
    
    return {
        'user1' : user1_details,
        'user2' : user2_details,
        'user3' : user3_details,
        'user4' : user4_details,
        'user5' : user5_details
    }
