import pytest


@pytest.fixture
def connection_params():
    return {
        "user": "test_user",
        "endpoint": "test_endpoint",
        "port": 5432,
        "name": "test_db",
        "password": "test_password",
    }
