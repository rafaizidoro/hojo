import os

import pytest

from hojo.connection import Connection, ConnectionCredentialError, scoped_session


# Test class for Connection
class TestConnection:
    def setup_method(self):
        Connection.reset()

    def test_initialization_with_parameters(self, connection_params):
        connection = Connection(**connection_params)
        assert connection.db_uri == connection_params["db_uri"]

    def test_missing_credentials_error(self):
        with pytest.raises(ConnectionCredentialError):
            Connection()

    def test_initialization_with_env_vars(self):
        conn = "postgresql+pg8000://test:name@127.0.0.1:5432/user"
        os.environ["DB_URI"] = conn
        connection = Connection()

        assert connection.db_uri == conn

    def test_session_creation(self, connection_params):
        connection = Connection(**connection_params)
        session = connection.session
        assert isinstance(session, scoped_session)

    def test_singleton_pattern(self, connection_params):
        connection1 = Connection(**connection_params)
        connection2 = Connection()
        assert connection1 is connection2
