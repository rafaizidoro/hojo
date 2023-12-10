import os

import pytest

from hojo.connection import Connection, ConnectionCredentialError, scoped_session


@pytest.fixture
def env_vars():
    envs = {
        "DB_USER": "env_user",
        "DB_ENDPOINT": "env_endpoint",
        "DB_PORT": "5432",
        "DB_NAME": "env_db",
        "DB_PASSWORD": "env_password",
    }

    for key, val in envs.items():
        os.environ[key] = val

    return envs


@pytest.fixture
def invalid_env_vars():
    envs = {
        "DB_USER": None,
        "DB_ENDPOINT": None,
        "DB_PORT": None,
        "DB_NAME": None,
        "DB_PASSWORD": None,
    }
    return envs


# Test class for Connection
class TestConnection:
    def test_initialization_with_parameters(self, connection_params):
        connection = Connection(**connection_params)
        assert connection.user == connection_params["user"]
        assert connection.endpoint == connection_params["endpoint"]
        assert connection.port == connection_params["port"]
        assert connection.name == connection_params["name"]
        assert connection.password == connection_params["password"]

    def test_missing_credentials_error(self):
        with pytest.raises(ConnectionCredentialError):
            Connection()

    def test_initialization_with_env_vars(self, env_vars):
        connection = Connection()
        assert connection.user == env_vars["DB_USER"]
        assert connection.endpoint == env_vars["DB_ENDPOINT"]
        assert int(connection.port) == int(env_vars["DB_PORT"])
        assert connection.name == env_vars["DB_NAME"]
        assert connection.password == env_vars["DB_PASSWORD"]

    # def test_invalid_env_vars_raise_error(self, invalid_env_vars):
    #     for key, val in invalid_env_vars.items():
    #         os.environ[key] = val
    #     with pytest.raises(ConnectionCredentialError):
    #         Connection()

    def test_session_creation(self, connection_params):
        connection = Connection(**connection_params)
        session = connection.session
        assert isinstance(session, scoped_session)

    def test_get_connection_string(self, connection_params):
        connection = Connection(**connection_params)
        expected_conn_string = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
            connection_params["user"],
            connection_params["password"],
            connection_params["endpoint"],
            connection_params["port"],
            connection_params["name"],
        )
        assert connection.get_connection_string() == expected_conn_string

    def test_singleton_pattern(self, connection_params):
        connection1 = Connection(**connection_params)
        connection2 = Connection()
        assert connection1 is connection2
