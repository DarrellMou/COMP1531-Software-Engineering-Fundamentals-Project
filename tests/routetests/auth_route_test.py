from src.auth import auth_register_route
from src.server import APP

def test_auth_register_route():
	with APP.test_client as client:
		req = client.post('/register', json={'email':'someonesemail@outlook.com', 'password':'jkdfnkfdsfd1213s', 'first_name':'winston', 'last_name':'lin'})
		json_data = req.get_json() # or req.json

		assert ..... check token and auth user id.