from src.error import InputError
from http_tests import *
import requests
import time
from src.auth import blacklist, auth_decode_token, auth_token_ok

# client and app are pytest fixtures
def test_auth_register_api_valid(client):

	response = client.post('/register', json={'email':'12382193@outlook.com', 'password':'123123kjdfd', 'first_name':'winston', 'last_name':'lin'})
	json_data = response.get_json() # or just json

	assert response.status_code == 201
	assert response.content_type == 'application/json'

	assert json_data['token'] and json_data['token'] != ''
	assert json_data['auth_user_id'] and json_data['auth_user_id'] != -1

def test_auth_register_api_invalid_missing_args(client):
	response = client.post('/register', json={'password':'jkdfnkfdsfd1213s', 'first_name':'winston', 'last_name':'lin'})
	json_data = response.get_json()

	assert response.content_type == 'application/json'
	assert response.status_code == 408
	assert json_data['token'] == ''
	assert json_data['auth_user_id'] == -1

# testing the somewhat redundant exception handler
def test_auth_register_api_invalid_exception(client):
	response_register = client.post('/register', json={'email' : '12382193@outlook.com', 'password':'123', 'first_name':'winston', 'last_name':'lin'})
	json_data = response_register.get_json()
	assert response_register.status_code == 400

	assert response_register.content_type == 'application/json'
	assert json_data['code'] == 400# exception 
	assert json_data['name'] == 'System Error'
	assert json_data['message']	# just '<p></p>'


def test_auth_login_api_valid(client):
	# register first 
	response_register = client.post('/register', json={'email':'1238293@outlook.com', 'password':'123123kjdfd', 'first_name':'winston', 'last_name':'lin'})
	json_data_register = response_register.get_json() # or just json
	assert response_register.status_code == 201
	assert response_register.content_type == 'application/json'

	response_login = client.post('/login', json={'email':'1238293@outlook.com', 'password':'123123kjdfd'})
	assert response_login.content_type == 'application/json'
	assert response_login.status_code == 201

	json_data_login = response_login.get_json()
	assert json_data_login['token']
	assert json_data_login['auth_user_id'] == json_data_register['auth_user_id']


def test_auth_login_api_invalid(client):
	# field missing from request
	response_login = client.post('/login', json={'email':'12382193@outlook.com'})
	assert response_login.content_type == 'application/json'
	assert response_login.status_code == 408

	json_data_login = response_login.get_json()
	assert json_data_login['token'] == ''
	assert json_data_login['auth_user_id'] == -1

	# register 
	response_register = client.post('/register', json={'email':'12382193@outlook.com', 'password':'123123kjdfd', 'first_name':'winston', 'last_name':'lin'})
	json_data_register = response_register.get_json() # or just json
	assert response_register.status_code == 201
	assert response_register.content_type == 'application/json'
	assert json_data_register['token']

	# if credentials don't match, handled by customized exception handler 
	response_login = client.post('/login', json={'email':'12382193@outlook.com', 'password':'123123kjdf'})
	assert response_login.content_type == 'application/json'
	assert response_login.status_code == 400

	json_data_login = response_login.get_json()
	assert json_data_login['code'] == 400 # this is just status_code
	assert json_data_login['name'] == 'System Error'
	assert json_data_login['message']


def test_auth_logout_api(client):
	# register
	response_register = client.post('/register', json={'email':'testing123@gmail.com', 'password':'1234567ABC', 'first_name':'winston', 'last_name':'lin'})
	json_data_register = response_register.get_json() # or just json
	assert response_register.content_type == 'application/json'
	assert response_register.status_code == 201
	token_kept_by_client = json_data_register['token']

	# logout
	response_logout = client.post('/logout', json={'token':token_kept_by_client})
	assert response_logout.status_code == 201
	assert response_logout.json['is_success'] == True

	# logout again with the same token, blacklisted since we've already logged out
	response_logout2 = client.post('/logout', json={'token':token_kept_by_client})
	assert response_logout2.json['is_success'] == False
	assert response_logout2.status_code == 408


def test_auth_logout_api_logging_back(client):
	# register
	response_register = client.post('/register', json={'email':'testing123@gmail.com', 'password':'1234567ABC', 'first_name':'winston', 'last_name':'lin'})
	json_data_register = response_register.get_json() # or just json
	assert response_register.content_type == 'application/json'
	assert response_register.status_code == 201
	token_kept_by_client = json_data_register['token']
	auth_user_id = auth_decode_token(token_kept_by_client)

	# logout
	response_logout = client.post('/logout', json={'token':token_kept_by_client})
	assert response_logout.status_code == 201
	assert response_logout.json['is_success'] == True

	# log back in
	response_login = client.post('/login', json={'email':'testing123@gmail.com', 'password':'1234567ABC'})
	assert response_login.content_type == 'application/json'
	assert response_login.status_code == 201

	# assert the user is no longer in the blacklist and token is valid again
	assert auth_user_id not in blacklist
	assert auth_token_ok(token_kept_by_client) == True
