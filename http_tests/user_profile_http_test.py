import requests
import pytest 
import json
from src import config
from src.data import retrieve_data

@pytest.fixture(autouse=True)
def reset():
	requests.delete(config.url + 'clear/v1', params={})


def test_user_profile():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = json.loads(resp_profile.text)

	assert json_data_profile == {'user' : 
				{
	            'auth_user_id' : json_data_register['auth_user_id'],
	            'email'        : 'exampleUserEmail@email.com',
	            'name_first'   : 'FIRSTNAME',
	            'name_last'    : 'LASTNAME',
	            'handle_str'   : 'firstnamelastname'
	            }
           }


def test_user_profile_invalid_token():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : 'someRandomToken', 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = json.loads(resp_profile.text)
	assert json_data_profile

	assert json_data_profile['name']
	assert json_data_profile['code']
	assert json_data_profile['message'] == '<p>invalid token</p>'


def test_user_profile_non_existent_user():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : json_data_register['token'], 'u_id' : 'someRandomAuthID'})
	json_data_profile = json.loads(resp_profile.text)
	assert json_data_profile

	assert json_data_profile['name']
	assert json_data_profile['code']
	assert json_data_profile['message'] == '<p>User doesn\'t exist</p>'


def test_user_profile_setname():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_setname = requests.put(config.url + 'user/profile/setname/v2', json={'token' : json_data_register['token'], 'name_first' : 'changedFirstname', 'name_last' : 'changedLastname'})
	json_data_setname = json.loads(resp_setname.text)
	assert json_data_setname == {}

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = json.loads(resp_profile.text)
	assert json_data_profile == {'user' : 
				{	
	            'auth_user_id' : json_data_register['auth_user_id'],
	            'email'        : 'exampleUserEmail@email.com',
	            'name_first'   : 'changedFirstname',
	            'name_last'    : 'changedLastname',
	            'handle_str'   : 'firstnamelastname'
	            }
           }


def test_user_profile_setname_invalid_token():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_setname = requests.put(config.url + 'user/profile/setname/v2', json={'token' : 'someRandomToken', 'name_first' : 'changedFirstname', 'name_last' : 'changedLastname'})
	json_data_setname = json.loads(resp_setname.text)
	assert json_data_setname['name']
	assert json_data_setname['message'] == '<p>invalid token</p>'
	assert json_data_setname['code']


def test_user_profile_setname_invalid_name_length():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_setname = requests.put(config.url + 'user/profile/setname/v2', json={'token' : json_data_register['token'], 'name_first' : '', 'name_last' : 'changedLastname'})
	json_data_setname = json.loads(resp_setname.text)
	assert json_data_setname['name']
	assert json_data_setname['code']
	assert json_data_setname['message'] == '<p>invalid name length</p>'


def test_user_profile_setemail():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_setname = requests.put(config.url + 'user/profile/setemail/v2', json={'token' : json_data_register['token'], 'email' : 'changedEmail@outlook.com'})
	json_data_setemail = json.loads(resp_setname.text)
	assert json_data_setemail == {}

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = json.loads(resp_profile.text)

	assert json_data_profile == {'user' : 
				{
	            'auth_user_id' : json_data_register['auth_user_id'],
	            'email'        : 'changedEmail@outlook.com',
	            'name_first'   : 'FIRSTNAME',
	            'name_last'    : 'LASTNAME',
	            'handle_str'   : 'firstnamelastname'
	            }
           }


def test_user_profile_sethandle_v1():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_sethandle = requests.put(config.url + 'user/profile/sethandle/v2', json={'token' : json_data_register['token'], 'handle_str' : 'changedHandle'})
	json_data_sethandle = json.loads(resp_sethandle.text)
	assert json_data_sethandle == {}

	resp_profile = requests.get(config.url + 'user/profile/v2', params={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = json.loads(resp_profile.text)

	assert json_data_profile == {'user' :
				{
            	'auth_user_id' : json_data_register['auth_user_id'],
            	'email'        : 'exampleUserEmail@email.com',
            	'name_first'   : 'FIRSTNAME',
            	'name_last'    : 'LASTNAME',
            	'handle_str'   : 'changedHandle'
            	}
           }


def test_users_all_v1():
	resp_register = requests.post(config.url + 'auth/register/v2', json={'email':'exampleUserEmail@email.com', 'password':'ExamplePassword', 'name_first':'FIRSTNAME', 'name_last':'LASTNAME'})
	json_data_register = json.loads(resp_register.text)
	assert json_data_register

	resp_users_all = requests.get(config.url + 'users/all/v1', params={'token' : json_data_register['token']})
	json_data_users_all = json.loads(resp_users_all.text)
	assert json_data_users_all