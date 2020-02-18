""" global variables file this will act as a module but is simply
a location for super global variables/objects to be dropped
into. This should be limited to variables that multiple modules
will need to read from or write toin hard to anticipate ways.
for example:

a player character will be a class object with a list of attributes

player
    strength
    dexterity
    constitution
    intelligence
    wisdom
    charisma
    HP
    icon
    animation frame
    animation direction
    currently "busy"
    etc.

Some of these may be sub classes that contain more about the player

as an example to the reason for global container:
Writing an animation module would let us animate the player better,
however if the player was defined in the main scope, animating would
require the animation functions to take the player in and look over its
values, then return the entirety of the players state at once to the
calling function, which would need to dertermine what to change without
overwriting the whole player object, or overwrite the whole player object

The animation logic would be simple to piece together but this issue gets
harder to mitigate as the code gets more complex. It should not be more ideal
to have all code in 1 module for the sake of calling these globals"""

player1     = "not initiated"
player2     = "not initiated"
player3     = "not initiated"
player4     = "not initiated"
party       = "not initiated"
menu        = "not initiated"
battlemenu  = "not initiated"
combat      = "not initiated"
enemy1      = "not initiated"
enemy2      = "not initiated"
enemy3      = "not initiated"
enemy4      = "not initiated"
