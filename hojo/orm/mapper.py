from dataclasses import MISSING
from enum import EnumType
from typing import get_type_hints

from attr import fields
from pluralizer import Pluralizer
from sqlalchemy import Column, Index, Table
from sqlalchemy.dialects.postgresql import UUID as SQLAlchemyUUID
from sqlalchemy.orm import registry
from sqlalchemy.types import Boolean, Date, DateTime, Float, Integer, String

from hojo.base import BaseModel

MAPPER_REGISTRY = registry()


def automap(registry=None):
    registry = registry or MAPPER_REGISTRY

    for model in BaseModel._registry:
        builder = TableBuilder(registry, model)
        builder.automap()

    return registry


class TypeTranslator:
    def __init__(self, model):
        self.model = model
        self.type_mapping = {
            "int": Integer,
            "float": Float,
            "str": String,
            "bool": Boolean,
            "datetime": DateTime,
            "date": Date,
            "UUID": SQLAlchemyUUID(as_uuid=True),
        }

    def translate(self, field):
        field_type = field.type
        field_type_name = field_type.__name__
        if field_type_name in self.type_mapping:
            return self.type_mapping[field_type_name]
        elif isinstance(field_type, EnumType):
            return String
        else:
            raise TypeError(
                f"Unsupported type: {field_type} for {self.model.__name__}.{field_name}'"
            )


class RelationshipManager:
    def __init__(self):
        self.relationships = {}

    def add_relationship(self, field_name, field_info):
        pass

    def get_relationships(self):
        return self.relationships


class TableBuilder:
    def __init__(self, mapper_registry, model):
        self.mapper_registry = MAPPER_REGISTRY
        self.model = model
        self.translator = TypeTranslator(model)
        self.relationship_manager = RelationshipManager()

    def build_table(self):
        columns = []
        uniques = {}
        indexes = {}

        for field_info in fields(self.model):
            if self._is_relationship_field(field_info):
                self.relationship_manager.add_relationship(field_info.name, field_info)
                continue

            column_type = self.translator.translate(field_info)

            is_primary_key = field_info.name == "id"  # id is the primary key by default
            is_nullable = field_info.default is None

            is_index = self.get_contraint("index", indexes, field_info)
            is_unique = self.get_contraint("unique", uniques, field_info)

            column = Column(
                field_info.name,
                column_type,
                primary_key=is_primary_key,
                nullable=is_nullable,
                index=is_index,
                unique=is_unique,
            )

            columns.append(column)

        for index in indexes:
            idx_fields = sorted(indexes[index])
            index_name = "ix_" + "_".join(idx_fields)
            columns.append(Index(index_name, *idx_fields))

        table = Table(
            Pluralizer().plural((self.model.__name__.lower())),
            self.mapper_registry.metadata,
            *columns,
        )

        return table

    def get_contraint(self, contraint_type, contraints, field_info):
        idx = field_info.metadata.get(contraint_type)
        match idx:
            case bool():
                is_index = idx
            case str():
                is_index = False
                contraints[idx] = contraints.get(idx) or []
                contraints[idx].append(field_info.name)
            case _:
                is_index = False
        return is_index

    def _is_relationship_field(self, field_info):
        info = getattr(field_info, "metadata") or {}
        return info.get("has_many") or info.get("belongs_to") or info.get("has_one")

    def automap(self):
        table = self.build_table()

        MAPPER_REGISTRY.map_imperatively(
            self.model,
            table,
        )

        self.orm_model = self.model
