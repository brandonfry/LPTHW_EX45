"""
This file contains functions to aid text adventures in handling both
text output and input.
"""

import os
import textwrap

def clear():
    """This function clears the screen regardless of OS."""
    os.system('cls' if os.name == 'nt' else 'clear')
    return


def newline():
    """Just wanted a way not to type backslash."""
    print "\n"
    return

def wrapit(input_text):
    """Uses textwrap.py to format paragraphs neatly.
    Textwrap outputs an array of lines to be printed.
    Print array entries individually and finish with a new line.
    """

    # Replaced whitespace so that \n would be left behind.
    wrapped = textwrap.wrap(input_text, width=60, replace_whitespace=True)
    for line in wrapped:
        print line
    newline()
    return

def carriage_return():
    """Waits for user to "scroll" the screen by way of clearing it."""
    raw_input(">> PRESS RETURN")
    clear()
    return

def get_input():
    """Grabs user input and returns it as a lowercase string.
       Null responses are disallowed.
    """

    response = raw_input(">> ENTER CHOICE: ")
    if response == '':
        response = get_input()
    return response.lower()


