# Hojo - An Opinionated ORM on Top of SQL Alchemy

Hojo is a library that simplifies the usage of SQL Alchemy, providing an interface that is familiar to Django users. While it is not an exact replication of the Django ORM API, it strives to be reminiscent of it, making it easier for Django developers to work with SQL Alchemy.

**Please note that this library is currently in Alpha version and is not yet ready for production use.**

## Installation

You can install Hojo using pip:

```bash
pip install hojo
```

## Basic Usage
Here's a basic example of how to use Hojo:


```python
# file: models.py
from hojo import BaseModel, automap
from attr import define

@define
class Soldier(BaseModel):
    name: str
    weapon: str
    level: int

# Create the mappers automatically
automap()


# file: query.py

# Insert the hero into the 'soldiers' table
hero = Soldier.objects.create(name='Cloud Strife', weapon='Buster Sword', level=50)

# Insert the antagonist into the 'soldiers' table
antagonist = Soldier.objects.create(name='Sephiroth', weapon='Masamune', level=99)

# Retrieve a Soldier with the name 'Cloud' from the 'soldiers' table
soldier = Soldier.objects.filter(name='Cloud Strife')

# Retrieve a Soldier filtering by the weapon
soldier = Soldier.objects.filter(weapon__startswith='Buster')

# Retrieve a list of Soldiers filtering by level greater than 10
soldiers = Soldier.objects.filter(level__gt=10)
```