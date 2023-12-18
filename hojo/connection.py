import json
import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from hojo.config import Config


class ConnectionCredentialError(RuntimeError):
    pass


class Connection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Connection, cls).__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self._session = None
        self._engine = None
        self.db_uri = Config.get("db_uri") or os.environ.get("DB_URI")

        if not self.db_uri:
            raise ConnectionCredentialError("Invalid database credentials.")

    @property
    def session(self) -> Session:
        if self._session:
            return self._session

        self._session = self.create_session()
        return self._session

    def create_session(self) -> Session:
        session_factory = sessionmaker(
            bind=self._get_engine(), future=True, expire_on_commit=False
        )
        session: Session = scoped_session(session_factory)  # type: ignore
        return session

    @classmethod
    def reset(cls):
        cls._instance = None

    def _get_engine(self):
        if self._engine:
            return self._engine

        self._engine = create_engine(self.db_uri)  # type: ignore

        return self._engine
