"""This file contains the room, game and fight engines. The room
engine handles room creation and passing the user into rooms. The game
engine then handles moving the user between rooms. The fight engine
deals with user-enemy encounters.
"""


import random
import bisect
from ex45_text import clear
from ex45_map import draw_map
from ex45_chars import Hero


class FightEngine(object):
    """
    """

    @staticmethod
    def attack(being_a, being_b):
        attack = random.randint(*being_a.attack)
        print "%s hits for %d!" % (being_a, attack)
        being_b.hit_points -= attack
        return being_b

    @staticmethod
    def battle(hero, monsters):
        monster = monsters.pop(monsters.index(random.choice(monsters)))
        monster = FightEngine.attack(hero, monster)
        if monster.hit_points > 0:
            monsters.append(monster)
        if monsters:
            for monster in monsters:
                hero = FightEngine.attack(monster, hero)
                if hero.hit_points <= 0:
                    print "You died!"
                    exit(0)
            (hero, monsters) = FightEngine.battle(hero, monsters)
        return hero, monsters


import ex45_rooms


class RoomEngine(object):
    """This engine holds the game map and creates rooms.

    An instance of this object first creates a blank dict
    of rooms, which can later be populated through .add_room().
    It also holds all necessary variables for random map generation.

    Later, the game engine calls the fetch_room() method to pass the
    hero into individual rooms.
    """

    # These dummy room types are created at the next_coord location.
    _dummy_rooms = ('EmptyRoom', 'NonRoom', 'FutureRoom', 'CurrentRoom')

    # This list contains all regular (non-first and -last) rooms
    # that are playable to the character. When a generic room is
    # created, its type is randomly selected from this list.
    _standard_rooms = (('TombRoom', 1),
                       ('PlainRoom', 4),
                       ('TortureRoom', 2),
                       ('PrisonRoom', 2),
                       ('HealingRoom', 0.5)
                       )

    # This direction dictionary helps the move-variable in the
    # fetch_room() method point to the next room.
    _direction = {0: (0, -1), # Shift up one row.
                  1: (1, 0),  # Shift right one column.
                  2: (0, 1),  # Shift down one row.
                  3: (-1, 0), # Shift left one column.
                  4: (0, 0)   # Repeat this room.
                  }

    def __init__(self, size):
        self.rooms = {}
        self.size = size
        self.next_coord = None
        self.coord = None
        self.init_coord = None
        self.doors = []

    def _pick_random_room(self):
        """This method picks a random room type based on weighted
        probability values of each room type.
        """

        values, weights = zip(*self._standard_rooms)
        total_weight = 0
        cum_weights = []
        for weight in weights:
            total_weight += weight
            cum_weights.append(total_weight)
        random_point = random.random() * total_weight
        j = bisect.bisect(cum_weights, random_point)
        return values[j]

    def add_room(self, room_type, *args):
        """Adds a dummy or real room to the game map.

        This method will add a room (be it a dummy or real room):
        Real rooms will have doors created. If the room type is
        'generic', then the room type will be assigned on a random
        choice from a randomly generated weighted list.
        """

        # If creating a dummy room, act on next_coord.
        if room_type in self._dummy_rooms:
            room_class = getattr(ex45_rooms, room_type)
            self.rooms[self.next_coord] = room_class()
            return

        # For other room types, the room_number variable is passed
        # into this method.
        room_number = args[0]

        # Pick at randomn a standard room type.
        if room_type == 'generic':
            room_type = self._pick_random_room()

        room_class = getattr(ex45_rooms, room_type)
        self.rooms[self.coord] = room_class(room_number)

        # Create appropriate doors.
        for i in self.doors:
            self.rooms[self.coord].create_door(i)
        return

    def fetch_room(self, a_game, hero):
        """Sends the user into a room and returns the next room.

        The game engine points to this method, which enter()s
        Rooms and returns movement choice from them. Movement
        chocies are then interrogated against the map to
        ensure that they are valid.
        """

        # move receives relative position change from .enter().
        (move, hero) = self.rooms[self.coord].enter(hero)
        move = int(move)
        clear()
        next_coord = (self.coord[0] + self._direction[move][0],
            self.coord[1] + self._direction[move][1])

        self.rooms[self.coord].current_room = False

        try:
            if self.rooms[next_coord].real:
                pass
        except KeyError as e:
            a_game.next_room(self, hero, "Out of bounds!")

        if self.rooms[next_coord].real == True:
            if self.rooms[self.coord].get_door(move):
                # If there is a room and door in this direction, go.
                self.coord = next_coord
                if move < 4:
                    hero.direction = move
                a_game.next_room(self, hero, "Valid door.")
            else:
                a_game.next_room(self, hero, "Door does not exist.")
        else:
            a_game.next_room(self, hero, "Room does not exist.")


class GameEngine(object):
    """Shifts the play between rooms and prints the map.

    This engine starts the player in the first room and handles
    shifting the player between rooms with the RoomEngine.fetch_room()
    method. A map is also printed to help the user navigate the dungeon.
    """

    def start(self, room_map):
        """Start the hero in the starting room"""
        room_map.coord = room_map.init_coord
        room_map.rooms[room_map.coord].current_room = True
        hero = Hero()
        print "Beginning quest!"
        draw_map(room_map)
        print "Currently facing", hero.direction
        print "Monsters:", room_map.rooms[room_map.coord].monsters
        room_map.fetch_room(self, hero)

    def next_room(self, room_map, hero, text):
        """Continue the adventure to the next room as returned by
        room_map.fetch_room().
        """

        print text
        room_map.rooms[room_map.coord].current_room = True
        draw_map(room_map)
        print "Currently facing", hero.direction
        print "Monsters:", room_map.rooms[room_map.coord].monsters
        room_map.fetch_room(self, hero)

