import pytest

from src.server import create_app
from src.data import reset_data

# a new app instance for every test
@pytest.fixture
def app_for_testing():
    a = create_app()

    yield a # generator


@pytest.fixture
def client(app_for_testing):
    return app_for_testing.test_client()


@pytest.fixture(autouse=True)
def reset():
	reset_data()
