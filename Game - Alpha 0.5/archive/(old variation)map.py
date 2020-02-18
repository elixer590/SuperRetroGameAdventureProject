"""map module for handling large maps"""

#lets do some computer science up in this bitch
"""
I need to load a map
then I need to look at a specific portion of this map
    these should be editable on the fly so that I can load into various locations
"""
import random
import glb
import pygame
import os
import largemapinit
import mapinit
import animation
import xml.etree.ElementTree as xmlhandler


"""
##--------------------------------------------------------##
## Define the map class
##--------------------------------------------------------##
"""
# the map class will create the map the player walks on
# it will additionally handle collision and events on the map
# What will we need in this class?

class maphandler:
    def __init__(self, mapfilename, tileset, playercoords,
                 mapoffset, spritesheetname, framedict,
                 screensize, tilesize=32):
        self.filename       = mapfilename
        self.tilesize       = tilesize
        self.tileset = pygame.image.load(os.path.join(os.getcwd(), "Objects", tileset)).convert_alpha()
        """self.tileset        = self.imagecutter(self.tileset, self.tilesize)""" #possibly breaking logic
        self.playercoords   = playercoords
        self.mapoffset      = mapoffset
        self.playerbox      = pygame.Rect((self.playercoords), (self.tilesize,self.tilesize))
        self.screenwidth    = screensize[0]
        self.screenheight   = screensize[1]
        # playerbox will be the collision handler
        self.framedict = framedict
        self.playersprite = playerholder()
        self.selectsprite("actor_10.png", self.framedict, self.tilesize)
        
        maplayers = self.load(mapfilename) # this creates the map arrays
        # self.load() will create the following variables
        # self.maplayers    = array = list of map lists that need to be turned into arrays
        # self.width        = integer = tiles wide
        # self.height       = integer = tiles high
        # self.dimensions   = tuple = (width, height)
        # self.collision    = list of walls
        # self.pix_width    = pixel width of map
        # self.pix_height   = pixel height of map
        self.maplayer0      = maplayers[0]
        self.maplayer1      = maplayers[1]
        self.maplayer2      = maplayers[2]
        self.maplayer3      = maplayers[3]

        # as part of init function, render initial maps
        self.render()

    def doDraw(self, timer):
        # This is the main animation function, it will draw all of
        # the map layers to a single output to be handled in the main loop
        output = pygame.Surface((self.screenwidth, self.screenheight))
        output.convert()
        output.blit(self.layer0, (self.mapoffset))
        output.blit(self.layer1, (self.mapoffset))
        output.blit(self.playersprite.animate.do(timer), (self.playercoords))
        output.blit(self.layer2, (self.mapoffset))
        output.blit(self.layer3, (self.mapoffset))
        return output

    def render(self):
        # convert layer lists to arrays
        self.maplayer0 = self.decipher(self.maplayer0)
        self.maplayer1 = self.decipher(self.maplayer1)
        self.maplayer2 = self.decipher(self.maplayer2)
        self.maplayer3 = self.decipher(self.maplayer3)
        self.collision = self.decipher(self.collision)

        # Decrement maplayers to have correct tilenumbers
        self.maplayer0 = self.decrementarray(self.maplayer0)
        self.maplayer1 = self.decrementarray(self.maplayer1)
        self.maplayer2 = self.decrementarray(self.maplayer2)
        self.maplayer3 = self.decrementarray(self.maplayer3)

        # Draw maplayers
        self.layer0 = self.drawmap(self.tileset, self.maplayer0)
        self.layer1 = self.drawmap(self.tileset, self.maplayer1)
        self.layer2 = self.drawmap(self.tileset, self.maplayer2)
        self.layer3 = self.drawmap(self.tileset, self.maplayer3)

    # loads a map from a specified filename
    # output will be "[(dimesions), [layers], [collision]] (maybe not anymore)
    # dimensions will be a tuple of (tiles wide, tiles high)
    # layers will be an array of maplists that will need to be deciphered
    #     and decremented
    # collision will be a list that needs to be deciphered
    def load(self, mapname):
        mapfile = xmlhandler.parse(os.path.join(os.getcwd(), "Objects", mapname))
        root = mapfile.getroot()

        maplayers = []
        collision = []

        container = []
        width = int(root.attrib["width"])
        height = int(root.attrib["height"])

        for child in root:
            if child.tag == "layer":
                if child.attrib["name"] != "collision":
                    layer = child.findtext("data").replace("\n", "").split(",")
                    for tile in layer:
                        container.append(int(tile))
                    maplayers.append(container)
                    container = []

        for child in root:
            if child.tag == "layer":
                if child.attrib["name"] == "collision":
                    layer = child.findtext("data").replace("\n", "").split(",")
                    for tile in layer:
                        container.append(int(tile))
                    collision = container
                    container = []
        # setup self variables for the class object            
        self.width          = int(width)
        self.height         = int(height)
        self.pix_width      = int(width*self.tilesize)
        self.pix_height     = int(height*self.tilesize)
        self.dimensions     = (int(width), int(height))
        self.maplayers      = maplayers
        self.collision      = collision
        # return ((width, height), maplayers, collision) # may not be needed any longer
        return maplayers

    def decipher(self, original):
        # given a single list this will break it into an array.
        # array will be cut into lengths based on width
        # once the height amount of lists is reached it will return
        width           = self.dimensions[0]
        height          = self.dimensions[1]
        index_width     = 0
        index_height    = 0
        output          = []
        row             = []
        index_original  = 0
        while index_height < height:
            while index_width < width:
                row.append(original[index_original])
                index_width += 1
                index_original += 1
            output.append(row)
            row = []
            index_width = 0
            index_height +=1
        return output


    def decrementarray(self, inputarray):
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

    def drawmap(self, tilesetimage, tilemap, tilesize=32): # take in surface object representing tileset, a map of tiles, and a tilesize
        height = (len(tilemap) * tilesize)
        width = (len(tilemap[0]) * tilesize)
        returnsurface = pygame.Surface((width, height), pygame.SRCALPHA) # SRCALPHA IS IMPORTANT FOR TRANSPARENCY
        returnsurface.convert_alpha()
        tilelist = self.imagecutter(tilesetimage, tilesize)
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
            
    def imagecutter(self, tilesetimage, size=32):
        iconX = 0
        iconY = 0
        tileswide = int(tilesetimage.get_width() / size)
        tileshigh = int(tilesetimage.get_height() / size)
        returnlist = []
        processing = True
        while processing:
            if iconY > (tilesetimage.get_height() - size):
                return returnlist
            if iconX<= (tilesetimage.get_width() - size):
                #set up the tile cutter and adjust its location
                tilecutter = pygame.Rect((iconX, iconY), (size, size))
                tile = tilesetimage.subsurface(tilecutter)
                tile.convert_alpha()
                returnlist.append(tile)
                iconX +=size
            elif iconY <= (tilesetimage.get_height() - size):
                iconX = 0
                iconY += size

    def selectsprite(self, spritename, framedict, spritetilesize=32):
        self.spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", spritename)).convert()
        self.spritesheet.set_colorkey(self.spritesheet.get_at((0,0))) #may need to change this for sprites that do not use color key
        self.spritesheet.convert_alpha()
        #self.spritelist = self.imagecutter(self.spritesheet, spritetilesize)
        self.playersprite.animate = animation.animation(self.spritesheet, framedict, "walk_up",
                                                        tilesize=(spritetilesize,spritetilesize))

    def getwalls(self):
        # first we need to determine where the player is actually
        # this determines the actual tile index number in the array
        playerindexY = int(self.playercoords[1]/32) - int(self.mapoffset[1]/32)
        playerindexX = int(self.playercoords[0]/32) - int(self.mapoffset[0]/32)
        output = []
        # now we need to walk through the array at the specified positions
        Y = playerindexY-1
        X = playerindexX-1
        while Y < playerindexY + 2:
            while X < playerindexX + 2:
                if self.collision[Y][X] == 1:
                    rect = pygame.Rect(((X*self.tilesize)+self.mapoffset[0], (Y*self.tilesize)+self.mapoffset[1]), (self.tilesize,self.tilesize))
                    output.append(rect)
                X += 1
            X = playerindexX-1
            Y+= 1
        return output

    def handleInput(self, keyspressed):
        if keyspressed !=[]:
            walls = self.getwalls()
        for key in keyspressed:
            if key == "K_UP":
                self.playersprite.animate.sel_animation("walk_up") # update animation frame
                self.playerbox.move_ip(0,-32) # move collision detector
                if self.playerbox.collidelist(walls) == -1: # if there is no collision
                    if self.mapoffset[1] >= 0: # if the map is at the top of the screen
                        if self.playercoords[1] >= 32: # if the player is not at the top of the screen
                            self.playercoords = (self.playercoords[0], self.playercoords[1]-32) # move the player up
                            # print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                        else: # if the player was at the top of the screen
                            self.playerbox.move_ip(0,+32) # move the detector rectangle back to the player
                    elif self.mapoffset[1] + self.pix_height <= self.screenheight: # if the map is at the bottom of the screen
                        if self.playercoords[1] > int(self.screenheight/2): #if the player lower than the center of the screen
                            self.playercoords = (self.playercoords[0], self.playercoords[1]-32) # move the player up
                            # print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                        else: #if the player was not below the center of the screen
                            self.mapoffset[1] +=32 # move the map down
                            self.playerbox.move_ip(0,+32)# move the detector back up to the player
                            # print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else: #if the map is not at the top or bottom of the screen
                        self.mapoffset[1] +=32 # move the map down
                        self.playerbox.move_ip(0,+32)# move the dector back to the player
                        # print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else: # there was a collision when attempting to move
                    #print(self.playerbox.collidelist(walls))
                    self.playerbox.move_ip(0,+32)# move dector back to the player
            if key == "K_DOWN":
                self.playersprite.animate.sel_animation("walk_down")
                self.playerbox.move_ip(0,+32)
                if self.playerbox.collidelist(walls) == -1:
                    if self.mapoffset[1] + self.pix_height <= self.screenheight:
                        if self.playercoords[1] <= self.screenheight - 33:
                            self.playercoords = (self.playercoords[0], self.playercoords[1]+32)
                            #print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                        else:
                            self.playerbox.move_ip(0,-32)
                    elif self.mapoffset[1] >= 0:
                        if self.playercoords[1] < int(self.screenheight/2):
                            self.playercoords = (self.playercoords[0], self.playercoords[1]+32)
                            #print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                        else:
                            self.mapoffset[1] -= 32
                            self.playerbox.move_ip(0,-32)
                            #print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else:
                        self.mapoffset[1] -= 32
                        self.playerbox.move_ip(0,-32)
                        #print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else:
                    self.playerbox.move_ip(0,-32)           
            if key == "K_LEFT":
                self.playersprite.animate.sel_animation("walk_left")
                self.playerbox.move_ip(-32,0)
                if self.playerbox.collidelist(walls) == -1:
                    if self.mapoffset[0] >= 0:
                        if self.playercoords[0] >= 32:
                            self.playercoords = (self.playercoords[0]-32, self.playercoords[1])
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                        else:
                            self.playerbox.move_ip(+32,0)
                    elif self.mapoffset[0] + self.pix_width <= self.screenwidth:
                        if self.playercoords[0] > int(self.screenwidth/2):
                            self.playercoords = (self.playercoords[0]-32, self.playercoords[1])
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                        else:
                            self.mapoffset[0] +=32
                            self.playerbox.move_ip(+32,0)
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        self.mapoffset[0] +=32
                        self.playerbox.move_ip(+32,0)
                        #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    self.playerbox.move_ip(+32,0)           
            if key == "K_RIGHT":
                self.playersprite.animate.sel_animation("walk_right")
                self.playerbox.move_ip(+32,0)
                if self.playerbox.collidelist(walls) == -1:
                    if self.mapoffset[0] + self.pix_width <= self.screenwidth+1:
                        if self.playercoords[0] <= self.screenwidth - 33:
                            self.playercoords = (self.playercoords[0]+32, self.playercoords[1])
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                        else:
                            self.playerbox.move_ip(-32,0)
                    elif self.mapoffset[0] >= 0:
                        if self.playercoords[0] < int(self.screenwidth/2):
                            self.playercoords = (self.playercoords[0]+32, self.playercoords[1])
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                        else:
                            self.mapoffset[0] -= 32
                            self.playerbox.move_ip(-32,0)
                            #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        self.mapoffset[0] -= 32
                        self.playerbox.move_ip(-32,0)
                        #print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    self.playerbox.move_ip(-32,0)








"""

def getwalls(collisionarray, mapoffset, playercoords):
    # first we need to determine where the player is actually
    # this determines the actual tile index number in the array
    playerindexY = int(playercoords[1]/32) - int(mapoffset[1]/32)
    playerindexX = int(playercoords[0]/32) - int(mapoffset[0]/32)
    output = []
    # now we need to walk through the array at the specified positions
    Y = playerindexY-1
    X = playerindexX-1
    while Y < playerindexY + 2:
        while X < playerindexX + 2:
            if collisionarray[Y][X] == 1:
                rect = pygame.Rect(((X*32)+mapoffset[0], (Y*32)+mapoffset[1]), (32,32))
                output.append(rect)
            X += 1
        X = playerindexX-1
        Y+= 1
    return output

def decipher(original, width, height):
    # given a single list this will break it into an array.
    # array will be cut into lengths based on width
    # once the height amount of lists is reached it will return
    index_width     = 0
    index_height    = 0
    output          = []
    row             = []
    index_original  = 0
    while index_height < height:
        while index_width < width:
            row.append(original[index_original])
            index_width += 1
            index_original += 1
        output.append(row)
        row = []
        index_width = 0
        index_height +=1
    return output


def drawmap(tilesetimage, tilemap, tilesize=32): # take in surface object representing tileset, a map of tiles, and a tilesize
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

def imagecutter(image, size=32):
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
"""

## borrowing classes for testing
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

class playerholder:
    def __init__(self):
        self.placeholder = "this is to make this a containerclass"


## setup pygame for testing
pygame.init()
screen = pygame.display.set_mode((960,640)) 

player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}

maptiles = "maptiles.png"
mapcoordoffset = [-960, -640]
player_coords = [480,320]

worldmap = maphandler("map2.tmx", "maptiles.png", player_coords, mapcoordoffset, "actor_10.png", player_frame_dict, (960,640), tilesize=32)



"""
## load maptiles and correct them
maptiles0 = mapinit.map0
maptiles1 = mapinit.map1
maptiles2 = mapinit.map2
maptiles3 = mapinit.map3

collisionlist = mapinit.collision
collisionlist = decipher(collisionlist, 60,40)

maptiles0 = decipher(maptiles0, 60,40)
maptiles1 = decipher(maptiles1, 60,40)
maptiles2 = decipher(maptiles2, 60,40)
maptiles3 = decipher(maptiles3, 60,40)

maptiles0 = decrementarray(maptiles0)
maptiles1 = decrementarray(maptiles1)
maptiles2 = decrementarray(maptiles2)
maptiles3 = decrementarray(maptiles3)
"""

## setup the playser object for testing        
"""player_coords = (480,320)
player = pygame.Rect((player_coords), (32,32)) # player collision box
playerstepcount = 0 # step counter for menu
playerspritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "actor_10.png")).convert()
playerspritesheet.set_colorkey(playerspritesheet.get_at((0,0)))
playerspritesheet.convert_alpha()
playerspritelist = imagecutter(playerspritesheet, 32)
glb.player1 = CharacterContainer("testboy", "test", True)"""
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52],
                     "enter": [51, 52, 53, 52]}
"""glb.player1.animate = animation.animation(playerspritesheet, player_frame_dict,
                                         "walk_up", tilesize=(32,32))"""
## Load a tileset (this would be passed to the function)
"""maptiles = pygame.image.load(os.path.join(os.getcwd(), "Objects", "maptiles.png")).convert_alpha()
tilesheet = imagecutter(maptiles)"""

maptiles = "maptiles.png"
mapcoordoffsetx = -960
mapcoordoffsety = -640
"""
maplayer0 = drawmap(maptiles, maptiles0)
maplayer1 = drawmap(maptiles, maptiles1)
maplayer2 = drawmap(maptiles, maptiles2)
maplayer3 = drawmap(maptiles, maptiles3)

mapwidth = maplayer0.get_width()
mapheight = maplayer0.get_height()
screenwidth = screen.get_width()
screenheight = screen.get_height()
"""
timeplayed = pygame.time.Clock()
timer = timeplayed.tick()

pygame.key.set_repeat(150,75)

keyspressed = []

running = True
while running:
    # handle pygame events
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


    worldmap.handleInput(keyspressed)
    
    """
    if keyspressed !=[]:
        walls = getwalls(collisionlist, (mapcoordoffsetx, mapcoordoffsety), player_coords)
    """

    """
    player is a rectangle object that should be in the same location as the
    player avatar. before moving the player avatar it checks and makes sure that
    the player will not colide when moving in any direction

    when the player can move in a direction but the maps moves instead
    the detector needs to be moved back
    """
    """
    for key in keyspressed:
        if key == "K_UP":
            glb.player1.animate.sel_animation("walk_up") # update animation frame
            player.move_ip(0,-32) # move collision detector
            if player.collidelist(walls) == -1: # if there is no collision
                if mapcoordoffsety >= 0: # if the map is at the top of the screen
                    if player_coords[1] >= 32: # if the player is not at the top of the screen
                        player_coords = (player_coords[0], player_coords[1]-32) # move the player up
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else: # if the player was at the top of the screen
                        player.move_ip(0,+32) # move the detector rectangle back to the player
                elif mapcoordoffsety + mapheight <= screenheight: # if the map is at the bottom of the screen
                    if player_coords[1] > int(screenheight/2): #if the player lower than the center of the screen
                        player_coords = (player_coords[0], player_coords[1]-32) # move the player up
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else: #if the player was not below the center of the screen
                        mapcoordoffsety +=32 # move the map down
                        player.move_ip(0,+32)# move the detector back up to the player
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else: #if the map is not at the top or bottom of the screen
                    mapcoordoffsety +=32 # move the map down
                    player.move_ip(0,+32)# move the dector back to the player
                    print(int(mapcoordoffsety/32), int(player_coords[1]/32))
            else: # there was a collision when attempting to move
                print(player.collidelist(walls))
                player.move_ip(0,+32)# move dector back to the player
        if key == "K_DOWN":
            glb.player1.animate.sel_animation("walk_down")
            player.move_ip(0,+32)
            if player.collidelist(walls) == -1:
                if mapcoordoffsety + mapheight <= screenheight:
                    if player_coords[1] <= screenheight - 33:
                        player_coords = (player_coords[0], player_coords[1]+32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else:
                        player.move_ip(0,-32)
                elif mapcoordoffsety >= 0:
                    if player_coords[1] < int(screenheight/2):
                        player_coords = (player_coords[0], player_coords[1]+32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else:
                        mapcoordoffsety -= 32
                        player.move_ip(0,-32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else:
                    mapcoordoffsety -= 32
                    player.move_ip(0,-32)
                    print(int(mapcoordoffsety/32), int(player_coords[1]/32))
            else:
                player.move_ip(0,-32)
       
        if key == "K_LEFT":
            glb.player1.animate.sel_animation("walk_left")
            player.move_ip(-32,0)
            if player.collidelist(walls) == -1:
                if mapcoordoffsetx >= 0:
                    if player_coords[0] >= 32:
                        player_coords = (player_coords[0]-32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        player.move_ip(+32,0)
                elif mapcoordoffsetx + mapwidth <= screenwidth:
                    if player_coords[0] > int(screenwidth/2):
                        player_coords = (player_coords[0]-32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        mapcoordoffsetx +=32
                        player.move_ip(+32,0)
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    mapcoordoffsetx +=32
                    player.move_ip(+32,0)
                    print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
            else:
                player.move_ip(+32,0)
       
        if key == "K_RIGHT":
            glb.player1.animate.sel_animation("walk_right")
            player.move_ip(+32,0)
            if player.collidelist(walls) == -1:
                if mapcoordoffsetx + mapwidth <= screenwidth+1:
                    if player_coords[0] <= screenwidth - 33:
                        player_coords = (player_coords[0]+32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        player.move_ip(-32,0)
                elif mapcoordoffsetx >= 0:
                    if player_coords[0] < int(screenwidth/2):
                        player_coords = (player_coords[0]+32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        mapcoordoffsetx -= 32
                        player.move_ip(-32,0)
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    mapcoordoffsetx -= 32
                    player.move_ip(-32,0)
                    print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
            else:
                player.move_ip(-32,0)
    """
                    
    """
    for key in keyspressed:
            if key == "K_UP":
                glb.player1.animate.sel_animation("walk_up")
                if mapcoordoffsety >= 0:
                    if player_coords[1] >= 32:
                        player_coords = (player_coords[0], player_coords[1]-32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                elif mapcoordoffsety + mapheight <= screenheight:
                    if player_coords[1] > int(screenheight/2):
                        player_coords = (player_coords[0], player_coords[1]-32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else:
                        mapcoordoffsety +=32
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else:
                    mapcoordoffsety +=32
                    print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    
            if key == "K_DOWN":
                glb.player1.animate.sel_animation("walk_down")
                if mapcoordoffsety + mapheight <= screenheight:
                    if player_coords[1] <= screenheight - 33:
                        player_coords = (player_coords[0], player_coords[1]+32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                elif mapcoordoffsety >= 0:
                    if player_coords[1] < int(screenheight/2):
                        player_coords = (player_coords[0], player_coords[1]+32)
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                    else:
                        mapcoordoffsety -= 32
                        print(int(mapcoordoffsety/32), int(player_coords[1]/32))
                else:
                    mapcoordoffsety -= 32
                    print(int(mapcoordoffsety/32), int(player_coords[1]/32))
           
            if key == "K_LEFT":
                glb.player1.animate.sel_animation("walk_left")
                if mapcoordoffsetx >= 0:
                    if player_coords[0] >= 32:
                        player_coords = (player_coords[0]-32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                elif mapcoordoffsetx + mapwidth <= screenwidth:
                    if player_coords[0] > int(screenwidth/2):
                        player_coords = (player_coords[0]-32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        mapcoordoffsetx +=32
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    mapcoordoffsetx +=32
                    print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    
            if key == "K_RIGHT":
                glb.player1.animate.sel_animation("walk_right")
                if mapcoordoffsetx + mapwidth <= screenwidth+1:
                    if player_coords[0] <= screenwidth - 33:
                        player_coords = (player_coords[0]+32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                elif mapcoordoffsetx >= 0:
                    if player_coords[0] < int(screenwidth/2):
                        player_coords = (player_coords[0]+32, player_coords[1])
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                    else:
                        mapcoordoffsetx -= 32
                        print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
                else:
                    mapcoordoffsetx -= 32
                    print(int(mapcoordoffsetx/32), int(player_coords[0]/32))
    """
    """               
    screen.blit(maplayer0, (mapcoordoffsetx, mapcoordoffsety))
    screen.blit(maplayer1, (mapcoordoffsetx, mapcoordoffsety))
    screen.blit(glb.player1.animate.do(timer), (player_coords))
    screen.blit(maplayer2, (mapcoordoffsetx, mapcoordoffsety))
    screen.blit(maplayer3, (mapcoordoffsetx, mapcoordoffsety))
    """
    screen.blit(worldmap.doDraw(timer), (0,0))
    timer += timeplayed.tick(60)
    pygame.display.flip()
    keyspressed = []
pygame.quit() # quit pygame after breaking loop








                
