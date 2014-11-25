"""
This file contains the room classes that can be instantiated
to the game map.
"""


import sys
from ex45_text import get_input
from ex45_engines import FightEngine
from ex45_chars import GenericMonster


def fight_or_flee():

    print "Will you fight or flee?"
    while True:
        choice = get_input()
        print choice
        if 'flee' in choice.lower():
            return 'flee'
        elif 'fight' in choice.lower():
            return 'fight'
        else:
            print "Please enter a valid choice to 'fight' or 'flee'"
    return choice


class Room(object):
    """Parent class for all real rooms.

    This class should not be called directly, but rather is
    a parent class for first, last and generic rooms. First- and
    last-room properties can be assigned. For mapping purposes,
    an instance of this object is passed a room number from an
    incrementally increasing variable. This class also contains
    methods for looking up and adding doors
    """

    # This tuple mirror-maps the door numbers to easily give
    # access to a neighboring room's adjacent door.
    opp_doors = (2, 3, 0, 1)

    def __init__(self, room_number):
        self.doors = [0, 0, 0, 0, 1]    # Fifth 'door' allows player to stay.
        self.room_number = room_number
        self.real = True
        self.current_room = False
        self._first_visit = True
        self.monsters = []

    def __repr__(self):
        return "%02d" % self.room_number

    def create_door(self, direction):
        self.doors[direction] = 1

    def get_door(self, direction):
        return self.doors[direction]

    def create_opp_door(self, direction):
        # Currently not used.
        self.doors[self.opp_doors[direction]]

    def get_opp_door(self, direction):
        return self.doors[self.opp_doors[direction]]

    def which_doors(self):
        """For debugging purposes this method returns the valid
        doors from the current room.
        """

        return "North: %d, East: %d, South: %d, West: %d" % (self.doors[0],
            self.doors[1], self.doors[2], self.doors[3])


class TombRoom(Room):
    """This room contains a sarcophagus. A mummy will pop out of
    it to attack the player.
    """

    def __init__(self, room_number):
        super(TombRoom, self).__init__(room_number)
        self.room_type = 'TombRoom'
        self. sarcophagus = 'closed'
        self.other_enemies = 'no'

    def enter(self, hero):
        # For debugging, have the room tell me where I am and
        # what doors are available.
        print "Tomb room %d" % self.room_number
        if self._first_visit == True:
            self._first_visit = False
            self.sarcophagus = 'open'
            print "There's a mummy crawling out of a sarcophagus!"
            self.monsters.append(GenericMonster(0))
        print self.monsters
        if self.monsters:
            choice = fight_or_flee()
            if choice == 'fight':
                (hero, monsters) = FightEngine.battle(hero, self.monsters)
                print "You have %d hit points remaining" % hero.hit_points
                raw_input("You won! Press enter to continue.")
                move = 4
            if choice == 'flee':
                move = self.opp_doors[hero.direction]
        else:
            print "Valid doors:", self.which_doors()
            move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        #~ elif self._first_visit == True:
            #~ return "xx"
        else:
            return "Tb"


class HealingRoom(Room):
    """This room contains a healing fountain and no monsters.
    The healing fountain restores all health, but can only be
    used once.
    """

    def __init__(self, room_number):
        super(HealingRoom, self).__init__(room_number)
        self.room_type = 'HealingRoom'
        self.other_enemies = 'no'
        self.fountain = 'unused'

    def enter(self, hero):
        # For debugging, have the room tell me where I am and
        # what doors are available.
        self._first_visit = False
        print "Healing room %d" % self.room_number
        print "Valid doors:", self.which_doors()
        move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        elif self._first_visit == True:
            return "xx"
        else:
            return "He"


class PlainRoom(Room):
    """This plain room can contain any sort of monster."""

    def __init__(self, room_number):
        super(PlainRoom, self).__init__(room_number)
        self.room_type = 'PlainRoom'
        self.other_enemies = 'yes'

    def enter(self, hero):
        # For debugging, have the room tell me where I am and
        # what doors are available.
        self._first_visit = False
        print "Plain room %d" % self.room_number
        print "Valid doors:", self.which_doors()
        move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        elif self._first_visit == True:
            return "xx"
        else:
            return "Pl"


class PrisonRoom(Room):
    """This room contains a monster and treasure chest
    in a prison cell. Brave adventures can risk fighting
    the monster for chance at great reward!
    """

    def __init__(self, room_number):
        super(PrisonRoom, self).__init__(room_number)
        self.room_type = 'PrisonRoom'
        self.other_enemies = 'no'
        self.prison_cell = 'closed'

    def enter(self, hero):
        # For debugging, have the room tell me where I am and
        # what doors are available.
        self._first_visit = False
        print "Prison room %d" % self.room_number
        print "Valid doors:", self.which_doors()
        move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        elif self._first_visit == True:
            return "xx"
        else:
            return "Pr"


class TortureRoom(Room):
    """Another room type that can contain any type of monster.
    A bit more gruesome than the plain room.
    """

    def __init__(self, room_number):
        super(TortureRoom, self).__init__(room_number)
        self.room_type = 'TortureRoom'
        self.other_enemies = 'yes'

    def enter(self, hero):
        # For debugging, have the room tell me where I am and
        # what doors are available.
        self._first_visit = False
        print "Torture room %d" % self.room_number
        print "Valid doors:", self.which_doors()
        move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        elif self._first_visit == True:
            return "xx"
        else:
            return "Tr"


class FirstRoom(Room):
    """This is the first room, where our hero begins the adventure.
    There will be no enemies in this room.
    """

    def __init__(self, room_number):
        super(FirstRoom, self).__init__(room_number)
        self.room_type = 'FirstRoom'
        self.first_room = True
        self.other_enemies = 'no'

    def enter(self, hero):
        self._first_visit = False
        print "First room!"
        print "Valid doors:", self.which_doors()
        move = get_input()
        return move, hero

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        else:
            return "Fi"


class LastRoom(Room):
    """This is last room, where the hero ends the quest or possibly
    chooses to descend to a lower, more difficult level. Maybe there
    could be a boss in this room.
    """

    def __init__(self, room_number):
        super(LastRoom, self).__init__(room_number)
        self.room_type = 'LastRoom'
        self.last_room = True
        self.other_enemies = 'no'

    def enter(self, hero):
        self._first_visit = False
        print "Last room!"
        sys.exit(0)

    def __repr__(self):
        if self.current_room == True:
            return "@@"
        elif self._first_visit == True:
            return "xx"
        else:
            return "La"


class EmptyRoom(object):
    """This is a dummy-object, used to fill out the map upon creation."""

    def __init__(self):
        self.room_type = 'EmptyRoom'
        self.real = False

    def __repr__(self):
        return "_e"


class FutureRoom(object):
    """This is a dummy-object, used a place holder for rooms that
    need to be handled.
    """

    def __init__(self):
        self.room_type = 'FutureRoom'
        self.real = False

    def __repr__(self):
        return "_u"


class NonRoom(object):
    """This is a dummy-object, used to make the final map pprint-able."""

    def __init__(self):
        self.room_type = 'NonRoom'
        self.real = False
        self.other_enemies = 'no'

    def __repr__(self):
        return "__"


class CurrentRoom(object):
    """This is a dummy-object, to be put in the place of the current room
    until all doors and neighboor rooms are handled, and the real room
    can be instantiated.
    """

    def __init__(self):
        self.room_type = 'CurrentRoom'
        self.real = False

    def __repr__(self):
        return "_c"
