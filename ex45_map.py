"""
This file contains the functions and classes necessary to
generate a random, playable map for ex45_main.py
"""


from random import randint
from pprint import pprint


def create_map(room_map):
    """Creates a blank map.

    This function creates a dictionary with keys corresponding
    to map x- and y-coordinates and zeros as values.
    """

    for i in range(room_map.size):
        for j in range(room_map.size):
            room_map.next_coord = (i, j)
            room_map.add_room('EmptyRoom')
    return room_map


def seed_map(room_map):
    """Places a starting room on the map.

    The room map is seeded with a starting room, which
    is not allowed to occur at the edges of the map.
    """

    room_map.init_coord = (randint(1, room_map.size - 2),
        randint(1, room_map.size - 2))

    # 'CurrentRoom' room type uses next_coord to instantiate.
    room_map.next_coord = room_map.init_coord
    room_map.add_room('CurrentRoom')
    return room_map


def get_next(room_map):
    """Checks if the next room is out of bounds.

    This function, given direction i, finds the next coordinate
    by adding i's directional change to the current coordinate.
    If the next coordinate is out of bounds, 'out of bounds' is
    returned.
    """

    # This dict augments the current room coordinates by one,
    # in one direction at a time.
    shift = {0: (0, -1), # Shift up one row.
             1: (1, 0),  # Shift right one column.
             2: (0, 1),  # Shift down one row.
             3: (-1, 0), # Shift left one column.
             }

    # Get the coordinats of the next possible room.
    next_coord = (room_map.coord[0] + shift[room_map.i][0],
        room_map.coord[1] + shift[room_map.i][1])

    # If the next room is in bounds, return the coordinate
    if (next_coord[0] in range(0, room_map.size) and
            next_coord[1] in range(0, room_map.size)):
        room_map.next_coord = next_coord
        return
    else:
        room_map.next_coord = 'out of bounds'
        return


def complete_room(room_map):
    """Adds rooms and doors around the current room.

    For a given coordinate, if the next possible room is in bounds,
    handle it accordingly. If the next room already exists and has a
    door facing this room, a reciprocal door is created. If the next
    room is disallowed, nothing is done. A coin flip is then made to
    determine if the next room should be created. If not, the next
    room is disallowed. If so, a future room and a door to it are
    created.
    """

    # Get the coordinats of the next possible room.
    get_next(room_map)

    # If the next coordinate is Out of Bounds, do nothing.
    if room_map.next_coord == 'out of bounds':
        return room_map

    # If there's already a room here, determine if
    # a reciprocal door should be created
    if room_map.rooms[room_map.next_coord].real == True:
        if room_map.rooms[room_map.next_coord].get_opp_door(room_map.i):
            room_map.doors.append(room_map.i)
        return room_map

    # If the room has been previously disallowed, do nothing.
    if room_map.rooms[room_map.next_coord].room_type == 'NonRoom':
        return room_map

    # Coin flip to decide if there is to be a room.
    # mandatory_rooms overrides coin_flip while > 0.
    coin_flip = randint(0, 1)
    if not coin_flip and room_map.mandatory_rooms <= 0:
        # If the room is not to exist, disallow future creation.
        if room_map.rooms[room_map.next_coord].room_type == 'EmptyRoom':
            room_map.add_room('NonRoom')
        return room_map

    # If there is to be a room, and the space is blank,
    # create a room.
    room_map.add_room('FutureRoom')
    room_map.doors.append(room_map.i)
    room_map.mandatory_rooms -= 1
    return room_map


def check_map(room_map):
    """Check if the map has been fully handled.

    Given room_map, check if there are any rooms remaining
    that need to be created. Return the next room's (x,y) or None
    depending on the result of the check.
    """

    for key, value in room_map.rooms.items():
        if value.room_type == 'FutureRoom':
            return key      # Key is returned to coord-variable.

    return None      # Otherwise return None.


def fill_empty_rooms(room_map):
    """Change empty rooms to non-rooms.

    Given a completed map, all empty rooms are changed to the
    'NonRoom' type, indicating that rooms are not to be created in
    those places.
    """

    for coord, room in room_map.rooms.items():
        if room.room_type == 'EmptyRoom':
            room_map.next_coord = coord
            room_map.add_room('NonRoom')

    return room_map


def generate_map(room_map):
    """Randomly generate a dungeon map on a blank map with a starting room.

    Given a singly seeded square map of arbitrary size,
    this function randomly populates the map with a first room,
    last room, generic rooms, non-rooms, empty rooms and future
    rooms. Non-rooms can never contain a room, empty rooms are
    yet to be handled and future rooms will contain a room. Upon
    completion only first room, last room, generic rooms and non-
    rooms will be present.
    """

    # This variable will force at least this many rooms to be
    # created, including generic and last rooms, but excluding
    # first room.
    room_map.mandatory_rooms = 3

    # Setting initial conditions to create the first room correctly.
    room_type = 'FirstRoom'
    room_number = 1
    room_map.coord = room_map.init_coord

    while True:
        # This room is now being handled
        room_map.next_coord = room_map.coord
        room_map.add_room('CurrentRoom')
        room_map.doors = []

        # Generate doors and surrounding rooms in each direction.
        for room_map.i in range(0, 4):
            room_map = complete_room(room_map)

        # If check_map returns none, there are no rooms after
        # this room.
        check = check_map(room_map)
        if check == None:
            room_type = 'LastRoom'

        # Create and add a room and its doors to room_engine.
        room_map.add_room(room_type, room_number)

        # Exit map generation if the last room has been handled
        if room_type == 'LastRoom':
            room_map = fill_empty_rooms(room_map)
            return room_map

        # Otherwise, the next room's coordinates are in check.
        room_map.coord = check

        # The room type will always be generic after first room,
        # until last room.
        room_type = 'generic'

        # Current room is now fully handled.
        room_number += 1


def draw_map(room_map):
    """Uses pprint to print a navigable map.

    This function, given an object containing a dictionary of room
    objects, will generate a uniformly sized list-of-lists to be
    printed with pprint.
    """

    # Create blank map array.
    map_array = [[0 for y in range(room_map.size)]
                  for x in range(room_map.size)]

    for x in range(room_map.size):
        for y in range(room_map.size):
            map_array[y][x] = room_map.rooms[(x, y)]

    pprint(map_array)
