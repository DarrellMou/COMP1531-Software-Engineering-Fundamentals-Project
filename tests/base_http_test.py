import pytest

from src import create_app

# a new app instance for every test
@pytest.fixture
def app_for_testing():
	a = create_app()

	yield a # a is a generator 


@pytest.fixture 
def client(app_for_testing):
	return app_for_testing.test_client()

