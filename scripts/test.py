# import json
# from datetime import date, datetime
# from enum import Enum
# from typing import Optional
# from uuid import uuid4

# from uuid6 import uuid7

# from hojo import BaseModel, automap, define, field


# class GameType(Enum):
#     RPG = "RPG"
#     ACTION = "ACTION"


# @define
# class Game(BaseModel):
#     name: str
#     game_type: GameType
#     created: datetime
#     updated: Optional[date] = field(default=None)


# # ff = Game(name="Final Fantasy", game_type=GameType.RPG)
# # ff_dict = unstructure(ff)
# # print(ff_dict)

# uid = str(uuid7())

# print(uid)

# ff = Game.load({"name": "Tifa", "game_type": "ACTION", "created": "2023-01-01"})

# print(ff)
