import os

import pytest

from hojo import Config, Hojo
from hojo.connection import Connection, ConnectionCredentialError, scoped_session


# Test class for Connection
class TestConnection:
    def setup_method(self, connection_params):
        Connection.reset()

    def test_initialization_with_parameters(self, config):
        connection = Connection()
        assert connection.db_uri is not None

    def test_missing_credentials_error(self):
        Config.reset()

        with pytest.raises(ConnectionCredentialError):
            Connection()

    def test_initialization_with_env_vars(self):
        conn = "postgresql+pg8000://user:pass@localhost:5432/db"
        os.environ["DB_URI"] = conn
        connection = Connection()

        assert connection.db_uri == conn

    def test_session_creation(self, config):
        connection = Connection()
        session = connection.session
        assert isinstance(session, scoped_session)

    def test_singleton_pattern(self, config):
        connection1 = Connection()
        connection2 = Connection()
        assert connection1 is connection2
