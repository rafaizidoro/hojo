from __future__ import annotations

from typing import Any, ClassVar, List, Optional, Set
from uuid import UUID

from attr import define
from attr import field as attrfield
from uuid6 import uuid7

from hojo.orm.manager import Manager, ModelDescriptor
from hojo.schema import BaseSchema


class BaseModel(BaseSchema):
    _registry: Set[BaseModel] = []

    objects: ClassVar = ModelDescriptor(Manager())

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "__attrs_attrs__"):
            return

        cls._registry.append(cls)


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


# def define(cls):
#     cls.__annotations__["id"] = UUID
#     # cls.__annotations__["created_at"] = datetime
#     # cls.__annotations__["updated_at"] = datetime

#     setattr(cls, "id", field(primary_key=True, kw_only=True, factory=uuid7))
#     # setattr(cls, "created_at", field(default_factory=datetime.utcnow))
#     # setattr(cls, "updated_at", field(default_factory=datetime.utcnow))

#     cls = attrdefine(cls)

#     return cls
