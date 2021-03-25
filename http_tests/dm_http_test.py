from http_tests import *
# this is to import fixtures for pytest

def test_dm_create_v1(client):
	# firstly register a new user
	response_register1 = client.post('/register', json={'email':'exampleuser1@outlook.com', 'password':'ABC1234567', 'first_name':'example_firstname1', 'last_name':'jajajaj'})
	json_data1 = response_register1.get_json()
	auth_user_id1 = json_data1['auth_user_id']
	token1 = json_data1['token']
	assert auth_user_id1	# just to be sure auth_user_id is returned
	assert token1			# auth_register does return a token


	# register a second user for the first user to dm 
	response_register2 = client.post('/register', json={'email':'exampleuser2@outlook.com', 'password':'ABC1234567', 'first_name':'example_firstname2', 'last_name':'kakakak'})
	json_data2 = response_register2.get_json()
	auth_user_id2 = json_data2['auth_user_id']


	# now the first user opens a dm to the second user
	u_id_list = [auth_user_id2]		# this is the second argument, a list of users to be dm'ed
	response_dm_create = client.post('/create', json={'token':token1, 'u_ids':u_id_list})
	json_data3 = response_dm_create.get_json()

	# check the two return values of dm_create are indeed sent back
	assert json_data3['dm_id']
	assert json_data3['dm_name']