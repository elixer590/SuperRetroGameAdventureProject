#End goal of this will be to handle combat
import pygame
import random
import glb
# what needs to happen for simple combat
"""
I need a list of things in combat
I need to have conditions for combat starting/ending
    something like enemy party has no health
    in battle animation maybe have something that changes a variable so that the players default should be dead instead of idle
I will need to determine a turnorder
    should be able to look over all the characters in the two lists at the start of a battle and determine who goes first.
To attack I will need to be able to select to attack and then target an enemy
    needs to be implimented in battle as well
For magic I will need to create a list of magics the specific character has then show that tot the battle menu screen
    this will need a menu built
    this will need to transition to the target selection menu
    any option should be allowed to target any character
Once an option is chosen the attack should go through
Will need to impliment some sort of "busy system" so that an attack needs to go through before another can begin
"""

class Combat:
    """this class will be to handle the mechanical parts of combat outside of the menu"""
    def __init__(self, enemylist, playerlist):
        self.enemylist      = enemylist
        self.playerlist     = playerlist
        self.currentturn    = 0 # index to relate to the allcharacters list
        

        # run init functions
        self._roll_initiative()

    def _roll_initiative(self):
        #for initializing the list of combatants
        self.allcharacters =[]
        index = 0
        while index < len(playerlist):
            self.allcharacters.append(self.playerlist[index])
            index += 1
        index = 0
        while index < len(enemylist):
            self.allcharacters.append(self.enemylist[index])
            index += 1
        self.allcharacters.sort(key=lambda character: character.Dexterity
                                +(random.randrange(1,20)), reverse = True)

        





'''
##--------------------------------------------------------------------##
##TESTING
##--------------------------------------------------------------------##
'''

class CharacterContainer:
    def __init__(self, name, characterClass, controllable):
        self.Strength       = self.calculatestats() #int
        self.Dexterity      = self.calculatestats() #int
        self.Constitution   = self.calculatestats() #int
        self.Intelligence   = self.calculatestats() #int
        self.Wisdom         = self.calculatestats() #int
        self.Charisma       = self.calculatestats() #int
        self.MaxHitPoints   = int((self.Constitution - 10) / 2 + 8) #int
        self.HitPoints      = self.MaxHitPoints
        self.ArmorClass     = int((self.Dexterity - 10) / 2 + 10) #int
        self.MaxMP          = self.calculatestats()
        self.MP             = self.MaxMP # this will hold an MP value later. Likely will base it off sorcery point conversions or something
        self.Name           = name #string
        self.CharacterClass = characterClass #currently string - likely an object later?
        self.Controllable   = controllable #boolean - maybe not needed anymore?

    def calculatestats(self):
        dieone      = random.randrange(1,6)
        dietwo      = random.randrange(1,6)
        diethree    = random.randrange(1,6)
        diefour     = random.randrange(1,6)
        stats       = [dieone, dietwo, diethree, diefour]
        stats.sort(reverse=True)
        stats.pop()
        statvalue   = 0
        for roll in stats:
            statvalue += roll
        return statvalue

player1 = CharacterContainer("person A", "test", True)
player2 = CharacterContainer("person B", "test", True)
player3 = CharacterContainer("person C", "test", True)
player4 = CharacterContainer("person D", "test", True)
player5 = CharacterContainer("person E", "test", True)

enemy1 = CharacterContainer("Enemy A", "test", False)
enemy2 = CharacterContainer("Enemy B", "test", False)
enemy3 = CharacterContainer("Enemy C", "test", False)
enemy4 = CharacterContainer("Enemy D", "test", False)
enemy5 = CharacterContainer("Enemy E", "test", False)

playerlist = [player1, player2, player3, player4, player5]
enemylist = [enemy1, enemy2, enemy3, enemy4, enemy5]

test = Combat(enemylist, playerlist)
"""for character in test.allcharacters:
    print(character.Name, character.Dexterity)"""



'''
##--------------------------------------------------------------------##
## Things that have to be setup
##--------------------------------------------------------------------##
'''
pygame.init() # we will need the input system for this test, though possibly will not need this later
screen = pygame.display.set_mode((840,640))
wait_for_player = True # are we waiting on the player
message_output = False # have we output text to the player that we are waiting
current_turn = 0 # will be an index on allcharacters list
allcharacters = test.allcharacters
timeplayed = pygame.time.Clock()
timer = timeplayed.tick()
timedelay = True # boolean - forces a wait in logic
lastturntime = 0
# begin hardcoding of battle system

wait_for_player = allcharacters[current_turn].Controllable
running = True
while running:
    # check input
    
    for event in pygame.event.get(): # returns a list of events. This will clear the event list each time so all event get objects should typially be handled here
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    keyspressed.append("K_UP")
                                        
                if event.key == pygame.K_DOWN:
                    keyspressed.append("K_DOWN")
                                                           
                if event.key == pygame.K_LEFT:
                    keyspressed.append("K_LEFT")
                    
                if event.key == pygame.K_RIGHT:
                    keyspressed.append("K_RIGHT")
                    
                if event.key == pygame.K_RETURN:
                    keyspressed.append("K_RETURN")
                    
                if event.key == pygame.K_SPACE:
                    keyspressed.append("K_SPACE")

    # check if all players or enemies are alive
    index = 0
    while index < len(enemylist):
        if enemylist[index].HitPoints > 0:
            #print(enemylist[index].Name)
            break
        if index == len(enemylist) -1:
            print("You broke'em jim") #victory
        index +=1
    index = 0
    while index < len(playerlist):
        if playerlist[index].HitPoints > 0:
            #print(playerlist[index].Name)
            break
        if index == len(playerlist) -1:
            print("you ded") #defeat
        index +=1

    # need to make a delayed action so turns can only happen every 2 seconds
    if timer - lastturntime > 1999:
        timedelay = False
            
    # player action
    if not timedelay:
        if wait_for_player:
            if not message_output:
                print("waiting on " + allcharacters[current_turn].Name)
                message_output = True
            if keyspressed != []: # a key was pressed
                print(allcharacters[current_turn].Name + " did something")
                lastturntime = timer
                message_output = False
                timedelay = True
                if current_turn == len(allcharacters)-1: # set next players turn
                    current_turn = 0
                else:
                    current_turn += 1
        else:
            print(allcharacters[current_turn].Name + " did something")
            lastturntime = timer
            timedelay = True
            if current_turn == len(allcharacters)-1: # set next players turn
                current_turn = 0
            else:
                current_turn += 1
    wait_for_player = allcharacters[current_turn].Controllable
    # end loop. Closing bits
    keyspressed = []
    timer += timeplayed.tick()
pygame.quit()
