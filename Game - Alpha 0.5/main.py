# basic hello world of graphic interface
# make it do something
import random # imported to generate randomness
import pygame # this makes screen stuff possible
import os # this will make loading things possible
import glb # super globals
import menu # menuclass
import mapinit # sets up the map variables to save space in main possibly no longer needed
import mapmodule # handles the map functions
import animation # this will handle animation
import battle # battle menu module
import combat


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
        self.attacklist     = ["attack"] # each character should have separate attacks
        # may be wise to initialize attacks as part of character initialization

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

    def get_stats(self):
        return [self.Name,
                self.CharacterClass,
                self.HitPoints,
                self.ArmorClass,
                self.Strength,
                self.Dexterity,
                self.Constitution,
                self.Intelligence,
                self.Wisdom,
                self.Charisma]
    
    def get_stats_string(self):
        return [str(self.Name),
                "Class: " + str(self.CharacterClass),
                "Hit Points: " + str(self.HitPoints),
                "Armor Class: " + str(self.ArmorClass),
                "Strength: " + str(self.Strength),
                "Dexterity: " + str(self.Dexterity),
                "Constitution: " + str(self.Constitution),
                "Intelligence " + str(self.Intelligence),
                "Wisdom: " + str(self.Wisdom),
                "Charisma: " + str(self.Charisma)]

##-------------------------------------------------------------##
##                  Image cutting and drawing                  ##
##-------------------------------------------------------------##

# function to return a drawn screen from a tileset and tilemap
def drawmap(tilesetimage, tilemap, tilesize=16): # take in surface object representing tileset, a map of tiles, and a tilesize
    height = (len(tilemap) * tilesize)
    width = (len(tilemap[0]) * tilesize)
    returnsurface = pygame.Surface((width, height), pygame.SRCALPHA) # SRCALPHA IS IMPORTANT FOR TRANSPARENCY
    returnsurface.convert_alpha()
    tilelist = imagecutter(tilesetimage, tilesize)
    index_x = 0
    index_y = 0
    processing = True
    while processing:
        while index_x < len(tilemap[0]):
            tiletoreturn = tilelist[tilemap[index_y][index_x]] # the madness of this is that it digs into an array to find what tile to load
            tiletoreturn.convert_alpha()
            returnsurface.blit(tiletoreturn, ((index_x * tilesize), (index_y * tilesize)))
            index_x += 1
        index_y += 1
        index_x = 0
        if index_y == len(tilemap):
            return returnsurface

# define a tile cutting function
# it will cut horizontal then drop a tile vertically before dropping again
def imagecutter(image, size=16):
    iconX = 0
    iconY = 0
    tileswide = int(image.get_width() / size)
    tileshigh = int(image.get_height() / size)
    returnlist = []
    processing = True
    while processing:
        if iconY > (image.get_height() - size):
            return returnlist
        if iconX<= (image.get_width() - size):
            #set up the tile cutter and adjust its location
            tilecutter = pygame.Rect((iconX, iconY), (size, size))
            tile = image.subsurface(tilecutter)
            tile.convert_alpha()
            returnlist.append(tile)
            iconX +=size
        elif iconY <= (image.get_height() - size):
            iconX = 0
            iconY += size

# make a random 2d array of data for madness reasons
def arraymadness(start, stop, outerlength, innerlength):
    count_x = 0
    count_y = 0
    returnlist = [[]]
    processing = True
    while processing:
        if count_x < innerlength:
            returnlist[count_y].append(random.randrange(start, stop))
            count_x += 1
        elif count_y < outerlength:
            count_x = 0
            returnlist.append([])
            count_y += 1
        else:
            return returnlist

def rotatearray(inputarray):
    # may need to rotate an array for mapdata
    # this will probably be used for converting maps from editors
    original_x = 0
    original_y = len(inputarray)-1
    currentline = []
    returnline = []
    while original_x < len(inputarray[0]):
        while original_y >= 0:
            currentline.append(inputarray[original_y][original_x])
            original_y -=1
        original_y = len(inputarray) - 1
        returnline.append(currentline)
        currentline = []
        original_x += 1
    return returnline

def decrementarray(inputarray):
    # may need to rotate an array for mapdata
    # this will probably be used for converting maps from editors
    currentline = []
    returnline = []
    lineindex = 0
    for line in inputarray:
        for tile in inputarray[lineindex]:
            currentline.append(tile - 1)
        returnline.append(currentline)
        currentline = []
        lineindex += 1
    return returnline

##-------------------------------------------------------------------------##
## Music and sound functions
##-------------------------------------------------------------------------##

def playstepsound():
    footstepsoundlist[random.randrange(0,9)].play()
    return

##-------------------------------------------------------------------------##

##init test variables
pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init() # start the pygame display
screen = pygame.display.set_mode((960, 640)) # screen is an object. this initializes the screen as 800x600
background = pygame.Surface(screen.get_size()).convert() # background color. converting the image is better for draw performance?
background.fill((128, 255, 128)) # fills the background with a single color (RGB)
screen.blit(background, (0,0)) # fills the screen with the background


# other initializations - this was to test initial image things - mostly only used for a single cursor icon at the moment
gui_icons = pygame.image.load(os.path.join(os.getcwd(), "Objects", "GUI0.png")).convert_alpha() # load image
tilelist = imagecutter(gui_icons)
tilelistindex = 0
tile_to_draw = []
# cursor is at tilelist[69]

# initialization for testing tile drawing function
tilemap0 = mapinit.tilemap0

tilemap1 = mapinit.tilemap1

tilemap2 = mapinit.tilemap2

tilemap0 = decrementarray(tilemap0) # convert tilemap
tilemap1 = decrementarray(tilemap1)
tilemap2 = decrementarray(tilemap2)

filename = "maptiles.png"
maptiles = pygame.image.load(os.path.join(os.getcwd(), "Objects", filename)).convert_alpha()
tilesout = drawmap(maptiles, tilemap0, tilesize=32) # drawn currently on the map screen loop
layer2tiles = drawmap(maptiles, tilemap1, tilesize=32)
layer3tiles = drawmap(maptiles, tilemap2, tilesize=32)

# portrait = pygame.image.load(os.path.join(os.getcwd(), "Objects",  "portrait.jpg")).convert()


# Sound test
# pygame.mixer.init() # this is not being loaded pre pygame.init()
pygame.mixer.music.load(os.path.join(os.getcwd(),"Objects", "battleThemeA.ogg"))
# testing to add menu sounds
menusound = pygame.mixer.Sound(os.path.join(os.getcwd(),"Objects", "Menu1A.ogg"))
menuclosesound = pygame.mixer.Sound(os.path.join(os.getcwd(),"Objects", "Menu1B.ogg"))
menusoundchannel = pygame.mixer.Channel(1)
menusoundplaying = False


## footstepsounds ##
footstep0 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep00.ogg"))
footstep1 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep01.ogg"))
footstep2 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep02.ogg"))
footstep3 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep03.ogg"))
footstep4 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep04.ogg"))
footstep5 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep05.ogg"))
footstep6 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep06.ogg"))
footstep7 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep07.ogg"))
footstep8 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep08.ogg"))
footstep9 = pygame.mixer.Sound(os.path.join(os.getcwd(), "Objects/sound", "footstep09.ogg"))
footstepsoundlist = [footstep0, footstep1, footstep2, footstep3, footstep4, footstep5, footstep6, footstep7, footstep8, footstep9]
footstepsoundindex = 0

#menu text testing
menuoptions = [["Items", "this is where you could look at your items, but i am lazy and you get none"],
               ["Status", "this is where you could look at your character status"],
               ["Equipment", "This is where you could equip your weapons or armor"],
               ["Magic", "This is where you could view or use magic"],
               ["Battle Test", "Test the battle system"],
               ["Back", "Return to the world screen"]]

glb.cursor = pygame.transform.scale(tilelist[69], (32, 32))

"""
#player stat testing for the menu
player1 = CharacterContainer("Major Tom", "Space Pirate", True)
player2 = CharacterContainer("Unit 3000-21", "Synthetic Love machine", True)
player3 = CharacterContainer("Bobbert Plant", "Backdoor Man", True)
"""



## these are needed for the animation system on the map
player_coords = [480, 320]
playerstepcount = 0 # step counter for menu
playerspritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "actor_10.png")).convert()
playerspritesheet.set_colorkey(playerspritesheet.get_at((0,0)))
playerspritesheet.convert_alpha()
playerspritelist = imagecutter(playerspritesheet, 32)

"""playersprite = [[playerspritelist[0], playerspritelist[1], playerspritelist[2], playerspritelist[1]],
                                [playerspritelist[12], playerspritelist[13], playerspritelist[14], playerspritelist[13]],
                                [playerspritelist[24], playerspritelist[25], playerspritelist[26], playerspritelist[25]],
                                [playerspritelist[36], playerspritelist[37], playerspritelist[38], playerspritelist[37]]]
playerdirection = 0 # for index into the player direction
playerstepphase = 0 # what animation frame to be on"""

glb.player1 = CharacterContainer("Dude 1", "test", True)
player1_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
glb.player1.animate = animation.animation(playerspritesheet, player1_frame_dict, "enter", tilesize=(32,32))

glb.player2 = CharacterContainer("Dude 2", "test", True)
player2_frame_dict = {"attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
glb.player2.animate = animation.animation(playerspritesheet, player2_frame_dict, "enter", tilesize=(32,32))

glb.player3 = CharacterContainer("Dude 3", "test", True)
player3_frame_dict = {"attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
glb.player3.animate = animation.animation(playerspritesheet, player3_frame_dict, "enter", tilesize=(32,32))

glb.player4 = CharacterContainer("Dude 4", "test", True)
player4_frame_dict = {"attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
glb.player4.animate = animation.animation(playerspritesheet, player4_frame_dict, "enter", tilesize=(32,32))

glb.enemy1 = CharacterContainer("enemy 1", "test", False)
enemy_frame_dict = {"attack": [28, 4, 16, 40, 28, 4, 16, 40],
                     "battle_idle": [39, 40, 41, 47, 46, 45],
                     "enter": [90, 91, 92, 80, 80, 28, 40]}
glb.enemy1.animate = animation.animation(playerspritesheet, enemy_frame_dict, "enter", tilesize=(32,32))

glb.enemy2 = CharacterContainer("enemy 2", "test", False)
glb.enemy2.animate = animation.animation(playerspritesheet, enemy_frame_dict, "enter", tilesize=(32,32))

glb.enemy3 = CharacterContainer("enemy 3", "test", False)
glb.enemy3.animate = animation.animation(playerspritesheet, enemy_frame_dict, "enter", tilesize=(32,32))

glb.enemy4 = CharacterContainer("enemy 4", "test", False)
glb.enemy4.animate = animation.animation(playerspritesheet, enemy_frame_dict, "enter", tilesize=(32,32))

"""
glb.player2 = CharacterContainer("Archer guy", "Archer", True)
player2spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "archer.png"))
player2_frame_dict = {"battle_idle": [221,221,222,222],
                      "attack": [221,222,223,224,225,226,227,228,229,230,231,232,233],
                      "die": [260,261,262,263,264,265],
                      "enter": [221,221,222,222]}
glb.player2.animate = animation.animation(player2spritesheet, player2_frame_dict,
                                         "battle_idle", tilesize=(64,64))

glb.player3 = CharacterContainer("Caster girl", "Healer", True)
player3spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "caster.png"))
player3_frame_dict = {"battle_idle": [66,66,67,67],
                     "heal": [13,14,15,16,17,18,19],
                     "attack": [169,170,171,172,173,174],
                     "die": [260,261,261,262,262,263,263,264,264,264,264,264],
                     "enter": [66,66,67,67]}
glb.player3.animate = animation.animation(player3spritesheet, player3_frame_dict, "battle_idle", tilesize=(64,64))
glb.enemy1 = CharacterContainer("testenemy", "test", False)
enemy1spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "spectre.png")).convert()
enemy1_frame_dict = {"battle_idle": [16,17,18,19,18,17],
                     "enter": [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                     "hide": [13,12,11,10,9,8,7,6,5,4],
                     "hidden": [4,3,2,3],
                     "attack": [13,12,11,10,9,8,7,6,5,4]}
glb.enemy1.animate = animation.animation(enemy1spritesheet, enemy1_frame_dict,
                                         "enter", tilesize=(80,70), flip=True)

glb.enemy2 = CharacterContainer("Bull thing", "enemy", False)
enemy2spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "bull.png")).convert()
enemy2_frame_dict = {"battle_idle": [0,1,2,3,4,5,4,3,2,1],
                     "enter": [7,7,7,7,6,6,6,5,5,4,3,2,1,0],
                     "die": [6,7,8,9,10,11,12,13,14,15,16],
                     "attack": [6,7,8,9,10,11,12,13,14,15,16]}
glb.enemy2.animate = animation.animation(enemy2spritesheet, enemy2_frame_dict,
                                         "enter", tilesize=(120,100), animationfreq=80)
"""
enemylist = [glb.enemy1, glb.enemy2, glb.enemy3, glb.enemy4 ]
playerlist = [glb.player1, glb.player2, glb.player3, glb.player4]

"""
0, 1, 2 - down [0]
12, 13, 14 - left [1]
24, 25, 26 - right [2]
36, 37, 38 - up [3]
sprites = array
	indexes
	0 down
	1 left
	2 right
	3 up

sprites[index]
	step phase
	0 = step
	1 = center
	2 = step
	3 = center

sprites[0][0] = facing left stepping
"""


"""##class MenuWindow:
    ##def __init__(self, screenwidth, screenheight, return_x=0, return_y=0, alpha=True, fillcolor=(0,0,255)): # will add as time goes on
    ##def drawborders(self, thickness=9, mode="all", color=(255,255,255)):
## menuclass testing
testwindow = MenuWindow(screen.get_width(), screen.get_height())
testwindow.drawborders()"""

#needed to init map
player_coords = [480, 320]
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
worldmap = mapmodule.maphandler("map2.tmx", glb.player1, player_coords,
                                player1_frame_dict, (960,640), tilesize=32)

glb.menu = menu.GameMenu(screen.get_size(), glb.cursor, menutext=menuoptions)


##Battlescreen testing
battlescreen = pygame.image.load(os.path.join(os.getcwd(),"Objects", "battleback1.png")).convert()
battlescreen = pygame.transform.scale(battlescreen, (960, 640))


pygame.key.set_repeat(150,75) # by default pygame will not repeat a key after it is pressed. this lets keys be held
keyspressed = [] # will be used by various screens for the purpose of checking what keys have been pressed

#initialize the battlemenu object
actionbox = ["Attack", "Magic", "Item", "Flee"]
# Battle menu got setup here, but this should be reinitialized each battle
glb.battlemenu = battle.BattleMenu(screen.get_size(), glb.cursor, battlescreen, playerlist, enemylist, actionbox, fillcolor=(75,75,75))

#all three of these are needed to be initialized for the drawing steps
things_to_draw = []
things_to_draw_mid = []
things_to_draw_top = []
timeplayed = pygame.time.Clock()
timer = timeplayed.tick()

# these need to be setup for the menu screens
showtiles = 1
showmenu = 0
showbattle = 0
running = True # variable to determine if main loop is running
while running:

    ## ---------------------------------------------------------------------------------------------
    ## This is the event handler
    ## ---------------------------------------------------------------------------------------------
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

    ## ---------------------------------------------------------------------------------------------
    ## This is the logic section of the loop
    ## ---------------------------------------------------------------------------------------------               

    # this thing is just what should be being drawn to the screen at the moment
    # it will need to be cleaned up later
    things_to_draw.append([background, (0,0)])
    # things_to_draw.append([textbox, (textbox_Xlocation, textbox_Ylocation)])

        ## ---------------------------------------------------------------------------------------------
        ## The tile based map
        ## ---------------------------------------------------------------------------------------------

    if showtiles == 1: #this is a very basic version of the world screen at the moment
        """for key in keyspressed:
            if key == "K_UP":
                glb.player1.animate.sel_animation("walk_up")
                if player_coords[1] >= 32:
                    playstepsound()
                    player_coords = (player_coords[0], player_coords[1]-32)
            if key == "K_DOWN":
                glb.player1.animate.sel_animation("walk_down")
                if player_coords[1] <= screen.get_height() - 32:
                    playstepsound()
                    player_coords = (player_coords[0], player_coords[1]+32)
            if key == "K_LEFT":
                glb.player1.animate.sel_animation("walk_left")
                if player_coords[0] >= 32:
                    playstepsound()
                    player_coords = (player_coords[0] - 32, player_coords[1])
            if key == "K_RIGHT":
                glb.player1.animate.sel_animation("walk_right")
                if player_coords[0] <= screen.get_width() - 32:
                    playstepsound()
                    player_coords = (player_coords[0] + 32, player_coords[1])
            if key == "K_RETURN":
                showtiles = 0
                showmenu = 1
                menusound.play()

            if key == "K_SPACE":
                """"""

        keyspressed = [] # reset the list of keys that need to be checked

        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(os.path.join(os.getcwd(), "Objects", "TownTheme.ogg"))
            pygame.mixer.music.play(-1)
        
        if menusoundchannel.get_busy() == 0: # are these even used anymore?
            menusoundplaying = False
        # tilesout = drawmap(maptiles, tilemap0, tilesize=32) #  this line was originally to draw the tiles to the screen each frame, but its drawing the tile frame
        # moving the call to draw the tilesout object to outside the main render window for performance testing
        things_to_draw.append([tilesout, (0,0)])
        things_to_draw.append([layer2tiles, (0,0)])
        # things_to_draw.append([playersprite[playerdirection][playerstepphase], player_coords])
        things_to_draw.append([glb.player1.animate.do(timer), player_coords])
        things_to_draw_mid.append([layer3tiles, (0,0)])
        # things_to_draw_top.append(currencybox([("FPS", str(timeplayed.get_fps())[:4])]))"""
        if pygame.mixer.music.get_busy() == False:
            pygame.mixer.music.load(os.path.join(os.getcwd(), "Objects", "TownTheme.ogg"))
            pygame.mixer.music.play(-1)

        # check for inputs not related to movement or map interaction  
        for key in keyspressed:
            if key == "K_RETURN":
                showtiles = 0
                showmenu = 1
                menusound.play()

        # handle inputs
        things_to_do = worldmap.handleInput(keyspressed)
        if things_to_do == "step":
            playstepsound()
                
        # output screen to be drawn        
        things_to_draw.append([worldmap.doDraw(timer), (0,0)])

        ## ---------------------------------------------------------------------------------------------
        ## This is the menuscreen section of the loop
        ## ---------------------------------------------------------------------------------------------
        
    if showmenu == 1: # this will be the menu function - it will likely be its own module and be passed all information
        for key in keyspressed:
            glb.menu.handleinput(keyspressed) # sends the key to the menu to handle its input
            if key == "K_UP":
                menusound.play()
                                    
            if key == "K_DOWN":
                menusound.play()
                    
            if key == "K_LEFT":
                """"""

                
            if key == "K_RIGHT":
                """"""

                
            if key == "K_RETURN":
                """"""
                #showtiles = 1
                #showmenu = 0

                
            if key == "K_SPACE":
                #If we are selecting the battlesystem option
                if glb.menu.cursorloc == len(glb.menu.menutext) - 2:
                    menusound.play()
                    showmenu = 0
                    #next two lines initialize the battle system by making a new battle system
                    glb.battlemenu = battle.BattleMenu(screen.get_size(), glb.cursor, battlescreen, playerlist, enemylist, actionbox, fillcolor=(75,75,75))
                    glb.combat = combat.Combat(playerlist, enemylist)
                    
                    showbattle = 1
                    #for changing to battle music need music to be stopped
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(os.path.join(os.getcwd(), "Objects", "battleThemeA.ogg"))
                    pygame.mixer.music.play(-1)
                if glb.menu.cursorloc == len(glb.menu.menutext) - 1:
                    showmenu = 0
                    showtiles = 1
                    menuclosesound.play()
                #elif menu_screen_xstate != 6:
                    # menu_screen_xstate = 6
                #else:
                    #menu_screen_xstate = cursorindex xstate was a plan for how to show context window that was not good

                    
        keyspressed = []
        if menusoundchannel.get_busy() == 0:
            menusoundplaying = False

        #draw menu to screen
        glb.menu.refresh()
        things_to_draw.append([glb.menu.menubackground, glb.menu.coords])

        ## ---------------------------------------------------------------------------------------------
        ## This is the battlescreen section of the loop
        ## ---------------------------------------------------------------------------------------------

    if showbattle == 1: # this will be the battle function - it will likely be its own module and be passed all information
        glb.battlemenu.handleinput(keyspressed)
        glb.battlemenu.refresh(timer)
        glb.combat.do(timer, keyspressed)
        for key in keyspressed:
            if key == "K_UP":
                """"""                    
            if key == "K_DOWN":
                """"""
            if key == "K_LEFT":
                """"""
            if key == "K_RIGHT":
                """"""
            if key == "K_SPACE":
                """"""
            if key == "K_RETURN":
                showtiles = 1
                showbattle = 0
                # to change back to other music when leaving this screen need to stop music
                pygame.mixer.music.stop()
            #if pygame.mixer.music.get_busy() == False: # this should probably get handled as part of a function when switching into battle
                #pygame.mixer.music.load(os.path.join(os.getcwd(),"battleThemeA.ogg"))
                #pygame.mixer.music.play()
        #after handling input what do I need to do for the battle logic
        keyspressed = []

        # need to draw after battle logic
        
        things_to_draw.append([glb.battlemenu.outputscreen, (0,0)])
        """things_to_draw.append([battlebackground, (0,0)])
        things_to_draw.append([drawchars, (0,0)])
        things_to_draw.append([battlemenu, (screen.get_width() - battlemenu.get_width(),0)])
        things_to_draw_top.append([battlestatswindow(playerlist),(screen.get_width() - battlemenu.get_width(),0)])"""



    ## ---------------------------------------------------------------------------------------------
    ## This is the render and draw section of the code
    ## ---------------------------------------------------------------------------------------------

    # Maybe have multiple lists that get added to, like layers to draw
    
    # drawloop test - there are three layers that can be drawn to. They will draw over the previous
    for thing in things_to_draw:
        screen.blit(thing[0], thing[1])

    if things_to_draw_mid != []:
        for thing in things_to_draw_mid:
            screen.blit(thing[0], thing[1])

    if things_to_draw_top != []:
        for thing in things_to_draw_top:
            screen.blit(thing[0], thing[1])
                    
    pygame.display.flip() # this tells the game to actually update the screen image.
    #think of it like two identical screens. One shows an output and one is drawn to.
    #then when you flip it outputs the drawn part
    timer += timeplayed.tick()

    # some cleanup of variables that are appended to
    things_to_draw = []
    things_to_draw_mid = []
    things_to_draw_top = []
    keyspressed = []
pygame.quit() # after the loop stop pygame

