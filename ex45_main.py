"""This is the main game file for example 45. From here methods
and functions from supporting files are called to initialize
and play the game.
"""

from sys import argv
from ex45_text import clear
from ex45_engines import GameEngine, RoomEngine
from ex45_map import create_map, seed_map, generate_map
from ex45_chars import populate_map
#~ from ex45_chars import Populate_Map
import readline


def main():
    """When called, main() will run a text adventure game written to
    fulfill the requirements of Learn Python the Hard Way's exercise 45.
    """

    size = int(argv[1])
    clear()
    room_map = RoomEngine(size)

    # Create a blank, square map of zeros.
    room_map = create_map(room_map)

    # Update map with a single, non-edge starting room.
    (room_map) = seed_map(room_map)

    # Randomly generate the rest of the map from the starting room.
    (room_map) = generate_map(room_map)

    # Randomly populate with monsters, based on room type.
    room_map = populate_map(room_map)

    a_game = GameEngine()

    # Start the game from the starting room
    a_game.start(room_map)

    # Give myself a somewhat robust method to debug.
    debug = raw_input("Debug (Y/N)?: ").lower()
    while debug == 'y':
        try:
            print input()
        except KeyboardInterrupt:
            break
        except SyntaxError:
            continue
        except NameError:
            continue

    return


if __name__ == "__main__":
    main()
