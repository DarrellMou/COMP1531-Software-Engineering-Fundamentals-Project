import pytest

from src.server import APP
from src.error import InputError
from tests.base_http_test import *

def test_auth_register_route(client):
	response = client.post('/echo', data={'email':'someonesemail@outlook.com', 'password':'jkdfnkfdsfd1213s', 'first_name':'winston', 'last_name':'lin'})
	json_data = response.get_json() # or req.json

	assert response.content_type == 'application/json'
	assert response.status_code == 201

	assert json_data['token']
	assert json_data['auth_user_id']

def test_auth_register_invalid_request(client):
	response = client.post('/register', json={'password':'jkdfnkfdsfd1213s', 'first_name':'winston', 'last_name':'lin'})
	
	assert response.content_type == 'application/json'
	assert response.status_code == 400

def test_auth_register_dup_error_route(client):

	client.post('/register', json={'email':'test12345@gmail.com', 'password':'dskfjnsdkjf', 'first_name':'winston', 'last_name':'lin'})
	with pytest.raises(InputError):
		response = client.post('/register', json={'email':'test12345@gmail.com', 'password':'dskfjnsdkjf', 'first_name':'winston', 'last_name':'lin'})

