from datetime import date, datetime
from enum import IntEnum, StrEnum
from uuid import UUID

import pendulum
from cattrs import Converter

SchemaConverter = Converter()

# UUID converter
SchemaConverter.register_unstructure_hook(UUID, lambda id: str(id))
SchemaConverter.register_structure_hook(UUID, lambda id, _: UUID(id))


# StrEnum converter
def _unstructure_strenum(enum_value: StrEnum | str):
    if type(enum_value) == str:
        return enum_value
    return enum_value.value


def _structure_strenum(value, enum_type):
    return enum_type(value)


SchemaConverter.register_unstructure_hook(StrEnum, _unstructure_strenum)
SchemaConverter.register_structure_hook(StrEnum, _structure_strenum)


# IntEnum converter
def _unstructure_strenum(enum_value: IntEnum | int):
    if type(enum_value) == int:
        return enum_value
    return enum_value.value


def _structure_strenum(value, enum_type):
    return enum_type(value)


SchemaConverter.register_unstructure_hook(IntEnum, _unstructure_strenum)
SchemaConverter.register_structure_hook(IntEnum, _structure_strenum)

# pendulum.Date converter
SchemaConverter.register_unstructure_hook(pendulum.Date, lambda dt: dt.to_date_string())
SchemaConverter.register_structure_hook(
    pendulum.Date, lambda dt, _: pendulum.parse(dt).date()
)


# pendulum.DateTime converter
def _unstructure_pendulum_datetime(pdt: pendulum.DateTime | datetime):
    if type(pdt) == datetime:
        return pendulum.instance(pdt).to_iso8601_string()

    return pdt.to_iso8601_string()  # type: ignore


def _structure_pendulum_datetime(value, _):
    return pendulum.parse(value)


SchemaConverter.register_unstructure_hook(
    pendulum.DateTime, _unstructure_pendulum_datetime
)

SchemaConverter.register_structure_hook(pendulum.DateTime, _structure_pendulum_datetime)
