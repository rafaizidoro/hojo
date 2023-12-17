from typing import Optional

import pytest

from hojo import define
from hojo.errors import ValidationError
from hojo.schema import BaseSchema


@define
class User(BaseSchema):
    name: str
    age: Optional[int] = None


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"name": "John", "age": 30}, {"name": "John", "age": 30}),  # Valid data
        (
            {"name": "Jane"},
            {"name": "Jane", "age": None},
        ),  # Missing age, but it's optional
        (
            {"name": "Jane", "surname": "Hellen"},
            {"name": "Jane", "age": None},
        ),  # Invalid fields, ignore by default
    ],
)
def test_load_valid_data(data, expected):
    user = User.load(data)
    assert user.dump() == expected


def test_load_invalid_data():
    with pytest.raises(ValidationError):
        User.load({"name": "John", "age": "thirty"})  # Age is not an integer


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"name": "John", "age": 30}, {"name": "John", "age": 30}),
    ],
)
def test_dump_data(data, expected):
    user = User(**data)
    dumped_data = user.dump()
    assert dumped_data == expected


@pytest.mark.parametrize(
    "data, expected",
    [
        ({"name": "John", "age": 30}, {"name": "John", "age": 30}),
        (
            {"name": "Jane", "age": None},
            {"name": "Jane"},
        ),  # age=None should be excluded in dump
    ],
)
def test_dump_with_pydantic_options(data, expected):
    user = User(**data)
    dumped_data = user.dump(skip_none=True)

    assert dumped_data == expected


def test_dump_with_pydantic_exclude():
    data = {"name": "John", "age": 30}

    user = User.load(data)
    dumped_data = user.dump(exclude=["age"])

    assert {"name": "John"} == dumped_data
