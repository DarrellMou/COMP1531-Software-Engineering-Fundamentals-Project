from http_tests import *
from src.data import retrieve_data

def test_user_profile(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.get('/user/profile/v2', json={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile == {
            'auth_user_id' : json_data_register['auth_user_id'],
            'email'        : 'example1@outlook.com',
            'name_first'   : 'example_firstname',
            'name_last'    : 'example_lastname',
            'handle_str'   : 'example_firstnameexa'
           }


def test_user_profile_invalid_token(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.get('/user/profile/v2', json={'token' : 'someRandomToken', 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile['name']
	assert json_data_profile['message'] == '<p>invalid token</p>'


def test_user_profile_non_existent_user(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.get('/user/profile/v2', json={'token' : json_data_register['token'], 'u_id' : 1234567890})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile['name']
	assert json_data_profile['message'] == '<p>User doesn\'t exist</p>'


def test_user_profile_setname(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.put('/user/profile/setname/v2', json={'token' : json_data_register['token'], 'name_first' : 'changedFirstname', 'name_last' : 'changedLastname'})
	json_data_setname = response.get_json() # or just json

	assert json_data_setname == {}

	response = client.get('/user/profile/v2', json={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile == {
            'auth_user_id' : json_data_register['auth_user_id'],
            'email'        : 'example1@outlook.com',
            'name_first'   : 'changedFirstname',
            'name_last'    : 'changedLastname',
            'handle_str'   : 'example_firstnameexa'
           }


def test_user_profile_setname_invalid_token(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.put('/user/profile/setname/v2', json={'token' : 'somerandomThing', 'name_first' : 'changedFirstname', 'name_last' : 'changedLastname'})
	json_data_setname = response.get_json() # or just json

	assert json_data_setname['name']
	assert json_data_setname['message'] == '<p>invalid token</p>'



def test_user_profile_setname_invalid_name_length(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.put('/user/profile/setname/v2', json={'token' : json_data_register['token'], 'name_first' : '', 'name_last' : 'changedLastname'})
	json_data_setname = response.get_json() # or just json

	assert json_data_setname['name']
	assert json_data_setname['message'] == '<p>invalid name length</p>'



def test_user_profile_setemail(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.put('/user/profile/setemail/v2', json={'token' : json_data_register['token'], 'email' : 'changedEmail@outlook.com'})
	json_data_setemail = response.get_json() # or just json

	assert json_data_setemail == {}

	response = client.get('/user/profile/v2', json={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile == {
            'auth_user_id' : json_data_register['auth_user_id'],
            'email'        : 'changedEmail@outlook.com',
            'name_first'   : 'example_firstname',
            'name_last'    : 'example_lastname',
            'handle_str'   : 'example_firstnameexa'
           }


def test_user_profile_sethandle_v1(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.put('/user/profile/sethandle/v1', json={'token' : json_data_register['token'], 'handle_str' : 'changedHandle'})
	json_data_setemail = response.get_json() # or just json

	assert json_data_setemail == {}

	response = client.get('/user/profile/v2', json={'token' : json_data_register['token'], 'u_id' : json_data_register['auth_user_id']})
	json_data_profile = response.get_json() # or just json

	assert json_data_profile == {
            'auth_user_id' : json_data_register['auth_user_id'],
            'email'        : 'example1@outlook.com',
            'name_first'   : 'example_firstname',
            'name_last'    : 'example_lastname',
            'handle_str'   : 'changedHandle'
           }


def test_users_all_v1(client):
	response = client.post('/register', json={'email':'example1@outlook.com', 'password':'1234567ABC', 'first_name':'example_firstname', 'last_name':'example_lastname'})
	json_data_register = response.get_json() # or just json

	response = client.get('/users/all/v1', json={'token' : json_data_register['token']})
	json_data_profile_all = response.get_json() # or just json

	assert json_data_profile_all

