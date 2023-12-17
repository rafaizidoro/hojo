from __future__ import annotations

import json
from typing import List, Optional, Union
from uuid import UUID

from cattrs.preconf.json import make_converter

SchemaConverter = make_converter()

# UUID converter
SchemaConverter.register_unstructure_hook(UUID, lambda id: str(id))
SchemaConverter.register_structure_hook(UUID, lambda id, _: UUID(id))


class BaseSchema:
    @classmethod
    def load(cls, data: Union[dict, BaseSchema], **kwargs):
        if isinstance(data, BaseSchema):
            data = data.dump()

        return SchemaConverter.structure(data, cls)

    def dump(
        self,
        skip_none: bool = False,
        only: Optional[List[str]] = None,
        exclude: Optional[List[str]] = None,
    ):
        data = SchemaConverter.unstructure(self)

        if only:
            data = {key: val for key, val in data.items() if key in only}
        elif exclude:
            data = {key: val for key, val in data.items() if key not in exclude}

        if skip_none:
            data = {key: val for key, val in data.items() if val is not None}

        return data

    def dumps(self, **kwargs):
        data = self.dump(**kwargs)

        return json.dumps(data)
