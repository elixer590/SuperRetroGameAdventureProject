# animation module
# This will be used to handle the animation of character objects
# it should generate a pygame surface with the current screen of
# a characters animation.

# "animation" should occur 4 times per second so it will be visible

# from another module we can call this by saying animate
# [list of animateable objects]

# should have a function to make an object animateable, maybe
# initialize the class instance as an object attribute

# need to standardize the name of the animations. thought
# is that you can pass a dictionary of animation frame list
# numbers, then when animating you can grab those frames
# as needed
# ex. frame_dict = {"battledefault": [0,1,5,12], "walk_up":[0,3,2]}
# current animation will be a text string to indicate what animation
# is currently playing.
import pygame
import glb # for access to super globals

class animation:
    # Need to know what tiles to use
    # what frame of the animation to use
    # if there is an animation in progress
    # how long its been since the last change to a frame
    def __init__(self, tilesheet, frame_dict, cur_animation,
                 tilesize=(32,32), animationfreq=180, flip=False):
        self.tilesheet      = tilesheet # sprite sheet
        self.frame          = 0 # frame counter
        self.busy           = False 
        self.lastframetime  = 0
        self.forceupdate    = True #boolean to ignore lastframetime
        self.tilesize       = tilesize # size of sprite
        self.image          = pygame.Surface((self.tilesize[0], self.tilesize[1]))
        self.animationfreq  = animationfreq # how many miliseconds should pass before updating the animation
        self.frame_dict     = frame_dict # dictionary of lists of tiles for animation
        self.cur_animation  = cur_animation # string name of current animation
        self.loop           = False # if off we want to only play once
        self.flip = flip
        # setting up the tiles needs to happen after class vars are initiated
        self.framelist      = self.imagecutter(self.tilesheet)

    ##----------------------------------------------------------------##
    ## image cutter
    ##----------------------------------------------------------------##
    # this class takes an image, and then cutes the image into smaller tiles
    # based on a specified tilesize. The tiles are then added to a list
    def imagecutter(self, image):
        iconX       = 0
        iconY       = 0
        tileswide   = int(image.get_width() / self.tilesize[0])
        tileshigh   = int(image.get_height() / self.tilesize[1])
        returnlist  = []
        processing  = True
        while processing:
            if iconY > (image.get_height() - self.tilesize[1]):
                return returnlist
            if iconX<= (image.get_width() - self.tilesize[0]):
                #set up the tile cutter and adjust its location
                tilecutter = pygame.Rect((iconX, iconY),
                                         (self.tilesize[0], self.tilesize[1]))
                tile = image.subsurface(tilecutter)
                tile.convert_alpha()
                if self.flip:
                    tile = pygame.transform.flip(tile, True, False)
                returnlist.append(tile)
                iconX +=self.tilesize[0]
            elif iconY <= (image.get_height() - self.tilesize[1]):
                iconX = 0
                iconY += self.tilesize[1]

    ##----------------------------------------------------------------##
    ## do - animate
    ##----------------------------------------------------------------##
    def do(self, timer):
        # if it has been more than a quarter of a second since the last
        # animation, update to a new frame
        # at end of function return the image for the current frame
        # this is a proof of concept at the moment.
        if timer - self.lastframetime >= self.animationfreq or self.forceupdate:
            if self.frame != len(self.frame_dict[self.cur_animation])-1:
                self.frame +=1
                self.forceupdate = False
                self.lastframetime = timer
            else:
                self.frame = 0
                self.forceupdate = False
                self.lastframetime = timer
            self.image = self.framelist[self.frame_dict[self.cur_animation][self.frame]]
        return self.image

    def sel_animation(self, animation):
        if animation != self.cur_animation:
            self.frame          = 0
            self.forceupdate    = True
            self.cur_animation  = animation
            
        








                
