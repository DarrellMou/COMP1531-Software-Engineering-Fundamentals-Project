import pytest

from src import create_app

# a new app instance for every test
@pytest.fixture
def app():
	a = create_app()

	yield a # a is a generator 


@pytest.fixture 
def client(app):
	return app.test_client()

