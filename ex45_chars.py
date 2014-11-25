"""This file contains the hero and enemy classes for ex45_main.py as
well as item/weapon/armor information.
"""

import random


class Being(object):
    """This is the parent class for both hero and monsters."""

    def __init__(self):
    # Do I really need this super class?
        pass


class Hero(Being):
    """The user controls the hero class object.

    The hero class should be stronger than than the enemies,
    though this advantage is offset by the number of enemies!
    """

    inventory = {'dagger': "Your trusty dagger. It's pointy and stabby!'",
                 'cloak': ("""Minimal protection, but you kind of look like
                         Batman"""),
                 'torch': "Man, this thing never goes out!"
                 }

    items = {'sword': "Wow, this thing is sharp!",
             'leather': "Sturdy boiled leather armor."
             }

    item_stats = {'dagger': (2, 5),
                  'cloak': (5, 10),
                  'sword': (10, 20),
                  'leather': (15, 30)
                  }

    direction = 0

    def __init__(self):
        super(Hero, self).__init__()
        self.basic_attack = (5,10)
        self.hit_points = 100
        #~ self.weapon_attack = self.item_stats['dagger']
        #~ self.total_attack = self.basic_attack + self.weapon_attack
        self.attack = self.basic_attack

    def __repr__(self):
        return "Derpy McGee"


class GenericMonster(Being):
    """This is a generic monster.

    Change this to something more interesting later.
    """

    def __init__(self, number):
        super(GenericMonster, self).__init__()
        self.attack = (2,5)
        self.hit_points = 10
        self.number = str(number + 1)

    def __repr__(self):
        return " ".join(('generic monster', self.number))


def populate_map(room_map):
    """Places monsters in rooms on the map.

    Given a room_map object containing a dictionary of rooms, this
    function randomly places 1-3 monsters in all rooms except for the
    first, last and healing rooms. The monsters are stored in a list
    in each Room() object.
    """

    for room in room_map.rooms:
        if room_map.rooms[room].other_enemies == 'no':
            continue
        num_monsters = random.randint(1, 3)
        for i in range(0, num_monsters):
            room_map.rooms[room].monsters.append(GenericMonster(i))
    return room_map
