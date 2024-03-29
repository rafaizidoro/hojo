import pytest

from hojo import Hojo


@pytest.fixture
def config():
    DB_ENDPOINT = "127.0.0.1"
    DB_USER = "postgres"
    DB_PORT = "54322"
    DB_NAME = "postgres"
    DB_PASSWORD = "postgres"

    db_uri = "postgresql+pg8000://{}:{}@{}:{}/{}".format(
        DB_USER, DB_PASSWORD, DB_ENDPOINT, DB_PORT, DB_NAME
    )

    Hojo.config(db_uri=db_uri)
