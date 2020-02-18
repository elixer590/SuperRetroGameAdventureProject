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


"""
##--------------------------------------------------------##
## maphandler class
##--------------------------------------------------------##
"""
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
        
        self.load(mapfilename) # this creates the map arrays
        # self.load() will create the following variables
        # self.maplayers    = array = list of map lists that need to be turned into arrays
        # self.width        = integer = tiles wide
        # self.height       = integer = tiles high
        # self.dimensions   = tuple = (width, height)
        # self.collision    = list of walls
        # self.pix_width    = pixel width of map
        # self.pix_height   = pixel height of map
        """self.maplayer0      = self.maplayers[0]
        self.maplayer1      = self.maplayers[1]
        self.maplayer2      = self.maplayers[2]
        self.maplayer3      = self.maplayers[3]"""
        # testing making the map layers generate with the load as well

        # as part of init function, render initial maps
        self.render()

    """
    ##--------------------------------------------------------##
    ## doDraw Function
    ##--------------------------------------------------------##
    """
    # called in the main loop to output the screen to draw
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

    """
    ##--------------------------------------------------------##
    ## render Function
    ##--------------------------------------------------------##
    """
    #converts map from a list to an array, then reduces all values by 1
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

    """
    ##--------------------------------------------------------##
    ## load Function
    ##--------------------------------------------------------##
    """
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

        
        tilesetname = (root.find("tileset").attrib["source"])[:-4] + ".png"
        self.tileset = pygame.image.load(os.path.join(os.getcwd(), "Objects", tilesetname)).convert_alpha()
        
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
        self.maplayer0      = self.maplayers[0]
        self.maplayer1      = self.maplayers[1]
        self.maplayer2      = self.maplayers[2]
        self.maplayer3      = self.maplayers[3]
        # return ((width, height), maplayers, collision) # may not be needed any longer

    """
    ##--------------------------------------------------------##
    ## Decipher Function
    ##--------------------------------------------------------##
    """
    # turns a list representing a map into an array
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

    """
    ##--------------------------------------------------------##
    ## Decipher Function
    ##--------------------------------------------------------##
    """
    # reduces all values in an array by 1 to match tileset index values
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

    """
    ##--------------------------------------------------------##
    ## Drawmap Function
    ##--------------------------------------------------------##
    """
    # draws one layer of the map and returns an image.
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
                try:
                    tiletoreturn = tilelist[tilemap[index_y][index_x]] # the madness of this is that it digs into an array to find what tile to load
                    tiletoreturn.convert_alpha()
                    returnsurface.blit(tiletoreturn, ((index_x * tilesize), (index_y * tilesize)))
                    index_x += 1
                except:
                    print(len(tilelist), len(tilemap))
                    print(index_y, index_x)
                    break
            index_y += 1
            index_x = 0
            if index_y == len(tilemap):
                return returnsurface
            
    """
    ##--------------------------------------------------------##
    ## imagecutter Function
    ##--------------------------------------------------------##
    """
    #cuts a tileset into a list of tile images
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

    """
    ##--------------------------------------------------------##
    ## selectsprite Function
    ##--------------------------------------------------------##
    """
    # Used to change the player avatar on the map
    # Semi hardcoded for the actor_10 sprite at the moment
    # will need logic to handle alpha selection
    def selectsprite(self, spritename, framedict, spritetilesize=32):
        self.spritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", spritename)).convert()
        self.spritesheet.set_colorkey(self.spritesheet.get_at((0,0))) #may need to change this for sprites that do not use color key
        self.spritesheet.convert_alpha()
        #self.spritelist = self.imagecutter(self.spritesheet, spritetilesize)
        self.playersprite.animate = animation.animation(self.spritesheet, framedict, "walk_up",
                                                        tilesize=(spritetilesize,spritetilesize))

    """
    ##--------------------------------------------------------##
    ## Getwalls Function
    ##--------------------------------------------------------##
    """
    # Grabs the walls directly around the player location based off map offset and player location
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

    """
    ##--------------------------------------------------------##
    ## HandleInput Function
    ##--------------------------------------------------------##
    """
    # this is the bulk of the collision handling code
    # will most likely strip this down and pass it to a collision check function to handle each direction
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
            if key == "K_RETURN":
                #self.tileset = pygame.image.load(os.path.join(os.getcwd(), "Objects", "hyptosis_til-art-batch-2.png")).convert_alpha()
                self.load("testCave.tmx")
                self.render()
                

"""
##--------------------------------------------------------##
## playerholder class
##--------------------------------------------------------##
"""

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
    screen.blit(worldmap.doDraw(timer), (0,0))
    timer += timeplayed.tick(60)
    pygame.display.flip()
    keyspressed = []
pygame.quit() # quit pygame after breaking loop








                
