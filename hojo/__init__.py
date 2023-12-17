from hojo.base import BaseModel, define, field
from hojo.config import Config
from hojo.connection import Connection
from hojo.orm.mapper import automap
from hojo.schema import BaseSchema


class Hojo:
    @staticmethod
    def config(key=None, **configs):
        if key:
            return Config.get(key)

        for key, value in configs.items():
            Config.set(key, value)
