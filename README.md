# Text Adventure Game Engine

A simple and easily modifiable and expandable text adventure game engine.

## Creating a game

Folder `test_game` includes a simple example game, which you can play and examine to see how it works.

To play the example game (or any game, really):

`python text_adventure.py`

![](https://i.ibb.co/RY1yvVm/text-adventure-play.jpg)

To create a game, a new folder should include the following files

* `rooms.json` - The locations in the game. A single room entry looks like this:

`{
    "id": 1,
    "name": "Town Square",
    "description": "You are standing in the town square. To the west is an old saloon. Looks like there could be trouble in there. To the east is a seedy hotel. A sturdy yet relatively short tree is in the middle of the square.",
    "neighbors": {
        "w": 2,
        "e": 3,
        "u": 6
    }
}`

* `items.json` - The items in the game. A single item entry looks like this:

`{
    "name": "an interdimensional key",
    "nickname": "key",
    "description": "It's a key alright. But it sure is odd looking.",
    "location": 5
}`

* `characters.json` - The characters in the game. A single character entry looks like this:

`{
    "name": "a talking horse",
    "nickname": "horse",
    "description": "I'm not sure what you expect me to say. It's a talking horse.",
    "speech": "I'm a talking horse. And I haven't got a thing to say...",
    "location": 1
}`

* `flags.json` - Game-dependant flags for tracking state during play. A single flag entry looks like this:

`{
    "name": "portal_unlocked",
    "setting": "False"
}`

Basic actions are coded in the game (move, get, drop, inventory, etc.), and some basic flag-related logic is also automated to some degree (search `UNLOCKABLE` and `EDITABLE` variables for details). Pay particular attention to the names of the items, the suffixes in the `flags.json` file, and the logic in the `do_unlock()` and `do_enter()` methods. Plans to extend the automation of additional logic exist.

Currently, parsing of user input consists of removing stop words, tokenzing what input is left, and returning the first 2 tokens to be interpreted for gameplay. This means that commands are limited to word pairs at this point ('get lamp', 'move east'), but plans to extend this exist.

The built-in Python module [`cmd`](https://docs.python.org/3/library/cmd.html) is used for command line interpretation, making this easily extensible.

No modules outside of the standard Python library are required.

Further development and instruction to come.

### Sources of inspiration and ideas came from:

* [Jeff Armstrong's 2013 PyOhio Talk](https://github.com/ArmstrongJ/pyohio2013/blob/master/src/game.py)
* [Building a Text-Based RPG Engine in Python](https://levelup.gitconnected.com/building-a-text-based-rpg-engine-in-python-e571c94500b0)
* [How should I parse user input in a text adventure game?](https://gamedev.stackexchange.com/questions/27004/how-should-i-parse-user-input-in-a-text-adventure-game)
