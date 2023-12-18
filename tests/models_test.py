from typing import Optional
from uuid import UUID

import pytest
from pendulum import DateTime

from hojo.base import BaseModel, model
from hojo.errors import ValidationError


@model
class User:
    name: str
    age: Optional[int] = None


def test_decorator():
    payload = {"name": "John", "age": 30}
    user = User(**payload)

    assert issubclass(User, BaseModel)
    assert user.id is not None
    assert user.created_at is not None
    assert user.updated_at is not None
    assert User in BaseModel._registry


def test_load_valid_data():
    payload = {"name": "John", "age": 30}
    user = User.load(payload)

    assert type(user) is User
    assert user.name == "John"
    assert user.age == 30

    assert isinstance(user.id, UUID)
    assert isinstance(user.created_at, DateTime)
    assert isinstance(user.updated_at, DateTime)


def test_load_invalid_data():
    with pytest.raises(ValidationError):
        User.load({"name": "John", "age": "thirty"})  # Age is not an integer


def test_dump():
    payload = {"name": "John", "age": 30}
    user = User.load(payload)

    user_id = str(user.id)
    user_created = user.created_at.to_iso8601_string()
    user_updated = user.updated_at.to_iso8601_string()

    user_dict = user.dump()

    assert user_dict["name"] == "John"
    assert user_dict["age"] == 30
    assert user_dict["id"] == user_id
    assert user_dict["created_at"] == user_created
    assert user_dict["updated_at"] == user_updated
