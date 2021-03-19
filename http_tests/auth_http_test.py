from src.server import APP
from src.error import InputError
from http_tests import *
import requests

# client and app are pytest fixtures
def test_auth_register_api_valid(client):
	response = client.post('/register', json={'email':'12382193@outlook.com', 'password':'123123kjdfd', 'first_name':'winston', 'last_name':'lin'})
	json_data = response.get_json() # or just json

	assert response.status_code == 201
	assert response.content_type == 'application/json'

	assert json_data['token'] and json_data['token'] != ''
	assert json_data['auth_user_id'] and json_data['auth_user_id'] != -1


def test_auth_register_api_invalid_request(client):
	response = client.post('/register', json={'password':'jkdfnkfdsfd1213s', 'first_name':'winston', 'last_name':'lin'})
	json_data = response.get_json()

	assert response.content_type == 'application/json'
	assert response.status_code == 408
	assert json_data['token'] == ''
	assert json_data['auth_user_id'] == -1

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

	# if credentials don't match
	response_login = client.post('/login', json={'email':'12382193@outlook.com', 'password':'123123kjdfd'})
	assert response_login.content_type == 'application/json'
	assert response_login.status_code == 201

	json_data_login = response_login.get_json()
	assert json_data_login['token']
	assert json_data_login['auth_user_id']
