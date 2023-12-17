import os

from attr import define

from hojo import BaseModel, automap, field


@define(slots=False)
class Soldier(BaseModel):
    name: str
    weapon: str
    level: int


data = {"name": "Cloud Strife", "weapon": "Buster Sword", "level": 10}

s = Soldier.load(data)

print(s)

# Create the mappers automatically
automap()


hero = Soldier.objects.create(name="Cloud Strife", weapon="Buster Sword", level=50)
