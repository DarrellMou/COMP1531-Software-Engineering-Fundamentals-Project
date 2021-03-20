from flask import Flask 

import pytest

# a new app instance 
def create_app():
	app = Flask(__name__)

	return app


@pytest.fixture 
def client():
	with create_app().test_client() as client:
		yield client