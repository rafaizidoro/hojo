from typing import Any, ClassVar, List, Optional, Type
from uuid import UUID

from attrs import define
from attrs import field as attrfield
from attrs import make_class
from pendulum import DateTime, now
from uuid6 import uuid7

from hojo.orm.manager import Manager, ModelDescriptor
from hojo.schema import BaseSchema


class BaseModel(BaseSchema):
    _registry: List["BaseModel"] = []

    objects: ClassVar = ModelDescriptor(Manager())


def field(
    primary_key: bool = False,
    index: bool = False,
    unique: bool = False,
    has_many: Optional[BaseModel] = None,
    belongs_to: Optional[BaseModel] = None,
    has_one: Optional[BaseModel] = None,
    **kwargs,
) -> Any:
    custom_metadata = {
        "primary_key": primary_key,
        "index": index,
        "unique": unique,
        "has_many": has_many,
        "belongs_to": belongs_to,
        "has_one": has_one,
    }

    # If metadata already exists in kwargs, update it; otherwise, create it
    if "metadata" in kwargs:
        kwargs["metadata"].update(custom_metadata)
    else:
        kwargs["metadata"] = custom_metadata

    return attrfield(**kwargs)


def model(cls, slots=False) -> Type[BaseModel]:
    klass = define(cls)

    class_fields = {
        "id": attrfield(type=UUID, factory=uuid7, kw_only=True),
        "created_at": attrfield(
            type=DateTime, factory=lambda: now("UTC"), kw_only=True
        ),  # type: ignore
        "updated_at": attrfield(
            type=DateTime, factory=lambda: now("UTC"), kw_only=True
        ),  # type: ignore
    }

    class_name = cls.__name__
    ProxyModel = make_class(
        class_name, class_fields, bases=(klass, BaseModel), cmp=False, slots=slots
    )

    ProxyModel.__name__ = cls.__name__
    ProxyModel.__qualname__ = cls.__qualname__
    ProxyModel.__module__ = cls.__module__
    ProxyModel.__doc__ = cls.__doc__

    BaseModel._registry.append(ProxyModel)

    return ProxyModel
