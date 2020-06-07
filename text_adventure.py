"""
A text adventure game engine.

"""

import sys
import os
import time
import random
import cmd
import textwrap
import json
import textwrap
from subprocess import call


GAME_FOLDER = "test_game"
STOP_WORDS_FILE = "stop_words"
WELCOME_FILE = os.path.join(GAME_FOLDER, "welcome.msg")
ROOM_FILE = os.path.join(GAME_FOLDER, "rooms.json")
ITEM_FILE = os.path.join(GAME_FOLDER, "items.json")
CHARACTER_FILE = os.path.join(GAME_FOLDER, "characters.json")
FLAG_FILE = os.path.join(GAME_FOLDER, "flags.json")

PROMPT = "\nWhat now? "
#PROMPT = "\n>>> "
#PROMPT = "\n> "

EMPTYLINE_MSG = "Don't be shy. Speak up."
UNKNOWN_MSG = "Sorry, but I don't understand."
MORE_SPECIFIC_MSG = "You need to be more specific."
NOT_HERE_MSG = "You can't do that here."
QUIT_MSG = "Thanks for playing!\n"
FAST_TYPING = 500
SLOW_TYPING = 200
TEXT_WIDTH = 80

STOP_WORDS = []
SYNONYMS = {'west': 'w',
            'east': 'e',
            'north': 'n',
            'south': 's',
            'up': 'u',
            'down': 'd',
            'x': 'examine',
            'q': 'quit',
            'g': 'get',
            'l': 'look',
            'i': 'inv'}

RED = "\033[1;31m"
BLUE = "\033[1;34m"
CYAN = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"


# Game specific
UNLOCKABLE = [(4, 'key', 'portal')]
ENTERABLE = [(4, 'portal')]


def parse_input(input):
    """Parse command input, return parsed command"""
    command = ""
    command_words = list(input.split(" "))
    new_command = []
    for word in command_words:
        if word not in STOP_WORDS:
            if word in SYNONYMS:
                new_command.append(SYNONYMS[word])
            else:
                new_command.append(word)
    for word in new_command[:2]:
        command = command + word + " "
    command = command.strip()
    #print("command issued => " + command)
    return command


def split_input(input):
    """Tokenize parsed command input, return arg"""
    arg = ""
    command_words = list(input.split(" "))
    new_command = []
    for word in command_words:
        new_command.append(word)
    arg += new_command[-1]
    #print("arg returned => " + arg)
    return arg


def to_console(t, typing_speed=SLOW_TYPING):
    """Displays gameplay messages to screen"""
    for l in t:
        sys.stdout.write(l)
        sys.stdout.flush()
        time.sleep(random.random() * 10. / typing_speed)
    sys.stdout.write(RESET)
    print()


def display_output(t, type=''):
    """Displays gameplay messages to screen"""
    if type == 'message':
        print()
        tt = textwrap.fill(t, width=TEXT_WIDTH)
        to_console(tt, typing_speed=FAST_TYPING)
    elif type == 'location':
        print()
        t2 = RED + t
        tt = textwrap.fill(t2, width=TEXT_WIDTH)
        to_console(tt)
    elif type == 'description':
        tt = textwrap.fill(t, width=TEXT_WIDTH)
        to_console(tt)
    elif type == 'item':
        t2 = 'You see ' + GREEN + t + '.'
        tt = textwrap.fill(t2, width=TEXT_WIDTH)
        to_console(tt)
    elif type == 'inv':
        t2 = GREEN + t
        tt = textwrap.fill(t2, width=TEXT_WIDTH)
        to_console(tt)
    elif type == 'character':
        t2 = 'You see ' + BLUE + t + '.'
        tt = textwrap.fill(t2, width=TEXT_WIDTH)
        to_console(tt)
    elif type == 'warning':
        pass
    else:
        print()
        tt = textwrap.fill(t, width=TEXT_WIDTH)
        to_console(tt)


def clear_screen():
    """Clears the screen"""
    _ = call('clear' if os.name == 'posix' else 'cls')
    

def display_welcome():
    """Displays game welcome message"""
    clear_screen()
    filepath = WELCOME_FILE
    with open(filepath) as fp:
        line = fp.readline()
        while line:
            if line.strip() == "":
                pass
            else:
                display_output(line.strip(), 'message')
            line = fp.readline()


def load_stop_words():
    """Load stop words from file"""
    with open(STOP_WORDS_FILE) as f:
        stop_words = [line.rstrip() for line in f]
    global STOP_WORDS
    STOP_WORDS = stop_words


def initialize_rooms():
    """Loads rooms data from single json file and initializes"""
    rooms = {}
    with open(ROOM_FILE) as json_file:
        data = json.load(json_file)
        for p in data['rooms']:
            room = []
            room.append(p['name'])
            room.append(p['description'])
            room.append(p['neighbors'])
            rooms[p['id']] = room
    return rooms


def initialize_items():
    """Loads items data from single json file and initializes"""
    items = {}
    with open(ITEM_FILE) as json_file:
        data = json.load(json_file)
        for p in data['items']:
            item = []
            item.append(p['name'])
            item.append(p['description'])
            item.append(p['location'])
            items[p['nickname']] = item
    return items


def initialize_characters():
    """Loads characters data from single json file and initializes"""
    characters = {}
    with open(CHARACTER_FILE) as json_file:
        data = json.load(json_file)
        for p in data['characters']:
            character = []
            character.append(p['name'])
            character.append(p['description'])
            character.append(p['speech'])
            character.append(p['location'])
            characters[p['nickname']] = character
    return characters


def initialize_flags():
    """Loads conditional flag data from single json file and initializes"""
    flags = {}
    with open(FLAG_FILE) as json_file:
        data = json.load(json_file)
        for p in data['conditions']:
            flags[p['name']] = p['setting']
    return flags


def get_room(id, rooms):
    """Change rooms by creating and returning a new room object"""
    room = rooms[id]
    return Room(id, room[0], room[1], room[2])


class Room():
    """A room (location) in the text adventure game"""

    def __init__(self, id=0, name='A Room', description='An empty room', neighbors={}):

        self.id = id
        self.name = name
        self.description = description
        self.neighbors = neighbors

    def _neighbor(self, direction):
        if direction in self.neighbors:
            return self.neighbors[direction]
        else:
            return None

    def north(self):
        return self._neighbor('n')

    def south(self):
        return self._neighbor('s')

    def east(self):
        return self._neighbor('e')

    def west(self):
        return self._neighbor('w')

    def up(self):
        return self._neighbor('u')

    def down(self):
        return self._neighbor('d')


class Game(cmd.Cmd):
    """The text adventure game class"""

    # Set command prompt
    prompt = PROMPT

    def __init__(self):

        # Start command interpreter
        cmd.Cmd.__init__(self)

        # Load stop words
        load_stop_words()

        # Display a welcome message
        display_welcome()

        # Load and initialize rooms
        self.rooms = initialize_rooms()

        # Load and initialize items
        self.items = initialize_items()

        # Load and initialize characters
        self.characters = initialize_characters()

        # Load and initialize conditional flags
        self.flags = initialize_flags()

        # Get current room info
        self.loc = get_room(1, self.rooms)

        # Display location info
        self.look()


    def check_items(self):
        """Checks for visible items in this location, displays relevant info"""
        for _, value in self.items.items():
            if value[2] == self.loc.id:
                item = value[0]
                display_output(item, 'item')#"You see " + item + ".", color=GREEN, skip=False)
            else:
                pass


    def check_characters(self):
        """Checks for visible characters in this location, displays relevant info"""
        for _, value in self.characters.items():
            if value[3] == self.loc.id:
                character = value[0]
                display_output(character, 'character')
            else:
                pass


    def check_flags(self):
        """Various checks of flags after a particular command is issued, game specific"""
        # If portal is entered, game is over
        if self.flags['portal_entered'] == 'True':
            display_output("Now off to adventures in far off dimensions!")
            display_output(QUIT_MSG)
            exit(0)


    def look(self):
        """Looks around the current location"""
        display_output(self.loc.name, 'location')
        display_output(self.loc.description, 'description')
        self.check_items()
        self.check_characters()


    def move(self, dir):
        """Moves player from location to location"""
        newroom = self.loc._neighbor(dir)
        if newroom is None:
            display_output("You can't go that way.")
        else:
            self.loc = get_room(newroom, self.rooms)
            self.look()


    def default(self, args):
        """Default 'unknown syntax' response"""
        display_output(UNKNOWN_MSG)


    def emptyline(self):
        """Empty line encountered"""
        display_output(EMPTYLINE_MSG)


    def precmd(self, args):
        """Parses input and returns parsed command for interpretation"""
        parsed_input = parse_input(cmd.Cmd.precmd(self, args))
        return parsed_input


    def do_talk(self, args):
        """Talk to someone, or something... or yourself"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            if object_lower in self.characters:
                for key, value in self.characters.items():
                    if value[3] == self.loc.id and key == object_lower:
                        display_output(object.capitalize() + " says: " + value[2])
            else:
                display_output("I don't see " + object + " here.")

 
    def do_get(self, args):
        """Get an item"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            if object_lower in self.items:
                for key, value in self.items.items():
                    if key == object_lower :
                        if value[2] == self.loc.id:
                            value[2] = 0
                            display_output("You got the " + object + ".")
                        elif value[2] == 0:
                            display_output("You already have the " + object + ".")
            else:
                if object_lower in self.characters:
                    display_output("You can't pick that up!")
                else:
                    display_output("I don't see " + object + " here.")


    def do_drop(self, args):
        """Drop an item"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            if object_lower in self.items:
                for key, value in self.items.items():
                    if key == object_lower:
                        if value[2] == 0:
                            value[2] = self.loc.id
                            display_output("You dropped the " + object + ".")
                        else:
                            display_output("You don't have " + object + ".")
            else:
                display_output("You don't have " + object + ".")


    def do_examine(self, args):
        """Closely examine an item or character"""
        object = split_input(args)
        object_lower = object.lower()
        found = False
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            for key, value in self.items.items():
                if key == object_lower and (value[2] == self.loc.id or value[2] == 0):
                    display_output(value[1])
                    found = True
            for key, value in self.characters.items():
                if key == object_lower and value[3] == self.loc.id:
                    display_output(value[1])
                    found = True
            if found == False:
                display_output("You can't examine that here.")
                
                
    def do_inv(self, args):
        """Display items in possession of player"""
        empty = True
        items = []
        for _, value in self.items.items():
            if value[2] == 0:
                empty = False
                items.append(value[0])
        if empty == True:
                display_output("You aren't carrying anything.")
        else:
            display_output("You have the following items:")
            for item in items:
                display_output(item, 'inv')


    def do_unlock(self, args):
        """Unlock something"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            for u in UNLOCKABLE:
                if u[0] == self.loc.id and object_lower == u[2]:
                    for key, value in self.items.items():
                        if key == 'key' and value[2] == 0:
                            if self.flags[u[2]+'_unlocked'] == 'False':
                                self.flags[u[2]+'_unlocked'] = 'True'
                                display_output("You unlocked the " + u[2] + ".")
                            else:
                                display_output("The " + u[2] + " is already unlocked.")
                else:
                    display_output("You don't have anything to unlock it with.")


    def do_enter(self, args):
        """Enter something"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        else:
            for e in ENTERABLE:
                if e[1] == object_lower:
                    if e[0] == self.loc.id:
                        if self.flags[e[1]+'_entered'] == 'False' and self.flags[e[1]+'_unlocked'] == 'True':
                            self.flags[e[1]+'_entered'] = 'True'
                            display_output("You entered the " + e[1] + ".")
                        elif self.flags[e[1]+'_entered'] == 'False' and self.flags[e[1]+'_unlocked'] == 'False':
                            display_output("The " + e[1] + " seems to be locked.")
                    else:
                        display_output("You can't enter that here.")
                else:
                    display_output("You can't enter that here.")
        self.check_flags()

    
    def do_climb(self, args):
        """Climb something"""
        object = split_input(args)
        object_lower = object.lower()
        if object_lower == "":
            display_output(MORE_SPECIFIC_MSG)
        elif object_lower == 'tree' and self.loc.id == 1:
            self.move('u')
        else:
            display_output("You can't climb that here.")


    def do_hit(self, args):
        """Hit something"""
        display_output("No need for beligerence.")


    def do_hello(self, args):
        """Say hello"""
        display_output("Uhhh... hello.")



    def do_look(self, args):
        """Look around"""
        self.look()


    def do_help(self, args):
        """Get help... maybe?"""
        display_output("You're on your own, Sonny.")


    def do_quit(self, args):
        """Leaves the game"""
        display_output(QUIT_MSG)
        return True


    def do_n(self, args):
        """Go north"""
        self.move('n')


    def do_s(self, args):
        """Go south"""
        self.move('s')


    def do_e(self, args):
        """Go east"""
        self.move('e')


    def do_w(self, args):
        """Go west"""
        self.move('w')


    def do_u(self, args):
        """Go up"""
        self.move('u')


    def do_d(self, args):
        """Go down"""
        self.move('d')


if __name__ == "__main__":
    g = Game()
    g.cmdloop()
