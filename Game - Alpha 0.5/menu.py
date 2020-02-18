## this will be a menu module to handle graphics classes
## more things to come up here
import pygame
import os
import glb # super globals

class GameMenu:
    # this will be a top level menu class for creating menus
    # the objective will to be to feed in selections for menu type and
    # return menu objects, as well as to be able to call on functions
    # to display these 

    def __init__(self, size, cursor, transparent=False, alphalevel=128,
                 fillcolor=(0,0,255), bordercolor=(255,255,255),
                 borderthickness=5, coords=(0,0), menutext=[["nothing"]],
                 fontsize=32, optionsfontsize=48, textcolor=(255,255,255)):
        # set instance variables
        self.size               = size
        self.transparent        = transparent
        self.alphalevel         = alphalevel
        self.fillcolor          = fillcolor
        self.bordercolor        = bordercolor
        self.borderthickness    = borderthickness
        self.coords             = coords
        self.menutext           = menutext
        self.fontsize           = fontsize
        self.optionsfontsize    = optionsfontsize
        self.textcolor          = textcolor
        self.updated            = False
        self.things_to_draw     = []
        self.cursorloc          = 0 # this is an index
        self.cursor             = cursor
        self.menubackground     = pygame.Surface(self.size)
        # self.updated will be a boolean that will report if the screen
        # has been updated since the update to menubackground. if so the
        # function that checks this will need to update the menubackground
        # using the things_to_draw list.
        # things_to_draw will be a list of objects passed back by other
        # draw functions this will have the downside of needing to be
        # cleared periodically. Potentially have adding to this list
        # be its own function, and have the functions calling it pass
        # a name back, the new draw call could check if the name is in
        # the list of things to be drawn on the menu, and if so replace
        # the object at that level

        # Perform initialization actions
        self.drawbackground()
        self.drawmenuoptions()
        self.drawdescription()
        self.drawcursor()
        
    """
    ##--------------------------------------------------------##
    ## Draw background function
    ##--------------------------------------------------------##
    """
    # draws the main window - this will be called in other drawing
    # functions to ensure that if data is drawn to the menu screen it
    # be drawn over a fresh image. also called on __init__ for init
    def drawbackground(self):
        if self.transparent == True:
            self.menubackground.convert_alpha()
            self.menubackground.setalpha(self.alphalevel)
        else:
            self.menubackground.fill(self.fillcolor)
            self.menubackground.convert()

        # coordinates for drawing lines from corner to corner
        topleftcrn  = (0,0)
        toprightcrn = (self.size[0]-1, 0)
        btmleftcrn  = (0, self.size[1]-1)
        btmrightcrn = (self.size[0]-1, self.size[1]-1)
        hrzndivleft = (0, int(self.size[1]*0.75))
        hrzndivright= (int(self.size[0]*0.75), int(self.size[1]*0.75))
        vertdivtop  = (int(self.size[0]*0.75), 0)
        vertdivbtm  = ((int(self.size[0]*0.75)),
                       self.size[1])

        #list of coordinates to draw lines
        menuedges   = [topleftcrn,
                       btmleftcrn,
                       btmrightcrn,
                       toprightcrn]
        
        # horizontal line
        hrzndiv     = [hrzndivleft, hrzndivright]
        vertdiv     = [vertdivtop, vertdivbtm]

        # draw outer border
        pygame.draw.lines(self.menubackground, self.bordercolor,
                          True, menuedges, (self.borderthickness*2)-1)
        # draw inner dividers
        pygame.draw.lines(self.menubackground, self.bordercolor,
                          False, hrzndiv, self.borderthickness)
        pygame.draw.lines(self.menubackground, self.bordercolor, False,
                          vertdiv, self.borderthickness)

    """
    ##--------------------------------------------------------##
    ## Drawmenuoptions function
    ##--------------------------------------------------------##
    """
    #draws options that will be on the right side of the screen
    def drawmenuoptions(self):
        font        = pygame.font.SysFont("none", self.optionsfontsize)
        width       = int(self.size[0]*0.25)
        height      = int(self.size[1]*0.75)
        optionsbox  = pygame.Surface((width, height), pygame.SRCALPHA)
        optionsbox.convert_alpha()
        # width += 10 # after creating box, move away from vertdiv
        lineheight = font.size("I")[1]
        currentheight = 20
        for line in self.menutext:
            rendertext = font.render(line[0], True, self.textcolor)
            rendertext = rendertext.convert_alpha()
            optionsbox.blit(rendertext, (0, currentheight))
            currentheight += 2*lineheight
        self.UpdateDrawList([optionsbox, ((width*3)+10, 0),"drawmenuoptions"])
        
    """
    ##--------------------------------------------------------##
    ## Drawdescription function
    ##--------------------------------------------------------##
    """
    # draw lower window text
    def drawdescription(self):
        text = self.menutext[self.cursorloc][1]
        width       = int((self.size[0]*0.75) - 20)
        height      = int(self.size[1] *0.25)
        lowerbox    = pygame.Surface((width, height), pygame.SRCALPHA)
        lowerbox.convert_alpha()
        font        = pygame.font.SysFont("none", self.fontsize)
        currentheight = 2
        lineheight  = font.size("I")[1]+2
        linestodraw = self.wordwrap(width, text, self.fontsize)
        for line in linestodraw:
            rendertext = font.render(line, True, self.textcolor)
            rendertext = rendertext.convert_alpha()
            lowerbox.blit(rendertext, (10,currentheight))
            currentheight += lineheight
        self.UpdateDrawList([lowerbox, (10, (int(self.size[1]*0.75)+10)), "drawdescription"])


    """
    ##--------------------------------------------------------##
    ## Drawplayinfo function
    ##--------------------------------------------------------##
    """
    def drawplayinfo(self):
        # To avoid redrawing the screen for clock updates this will make a borderless
        # box that fits inside the bottom right quarter of the screen and draws directly
        # to the menubackground
        font = pygame.font.SysFont("none", self.fontsize)
        lineheight = font.size("I")[1] + 2
        playinfobox = pygame.Surface(((int(self.size[0]*0.25) - 20), (int(self.size[1]*0.25) -20)))
        playinfobox.fill(self.fillcolor)
        index = 0
        info_to_draw = ["gold:" + str(tatertot.gold),"steps:" + str(tatertot.steps)] 
        while index < len(info_to_draw):
            rendertext = font.render(info_to_draw[index], True, self.textcolor)
            playinfobox.blit(rendertext, (0, lineheight*index))
            index += 1
        # to draw we need to determine the xy for the corner of the
        # playinfo window
        pib_x = int(self.size[0]*0.25)
        pib_y = int(self.size[1]*0.25)
        x_gap = int((pib_x-playinfobox.get_width()) /2)
        y_gap = int((pib_y-playinfobox.get_height()) /2)
        self.menubackground.blit(playinfobox, (((self.size[0]*0.75)+x_gap), ((self.size[1]*0.75)+y_gap)))

    ## Currency box here for porting purposes
    def currencybox(thingone, size=32):
        # will go in the lower right of the menu
        boxout = pygame.Surface(((int(screen.get_width()/4)-20), (int(screen.get_height()/4)-20)), pygame.SRCALPHA)
        boxout.convert_alpha()
        # we will accept a list of string tuples in now instead
        currencyindex = 0
        while currencyindex < len(thingone):    
            textone = writelongword(thingone[currencyindex][0], size, (255,255,255), (int(screen.get_width()/4)-20), (int(screen.get_height()/4)-20))
            texttwo = rightjustifiedtext(thingone[currencyindex][1], size-2)
            boxout.blit(textone, (0,(currencyindex*texttwo.get_height())+(4*currencyindex)))
            boxout.blit(texttwo, ((boxout.get_width()-texttwo.get_width()), (currencyindex * texttwo.get_height())+ 4 + (currencyindex*4)))
            currencyindex += 1
        return [boxout, (((int(screen.get_width()/4)*3)+10), ((int(screen.get_height()/4)*3)+10))]
        

    """
    ##--------------------------------------------------------##
    ## Drawcursor function
    ##--------------------------------------------------------##
    """

    def drawcursor(self):
        font = pygame.font.SysFont("none", self.optionsfontsize)
        lineheight = 2*(font.size("I")[1])
        self.UpdateDrawList([self.cursor, ((self.size[0] - 42),
                                      ((self.cursorloc*lineheight)+20)),
                             "drawcursor"])
    
    """
    ##--------------------------------------------------------##
    ## UpdateDrawList function
    ##--------------------------------------------------------##
    """
    def UpdateDrawList(self, itemtodraw):
        item_in_list = False
        index = 0
        while index < len(self.things_to_draw):
            if self.things_to_draw[index][2] == itemtodraw[2]:
                self.things_to_draw[index] = itemtodraw
                item_in_list = True
                self.updated = True
            index += 1
        if item_in_list == False:
            self.things_to_draw.append(itemtodraw)
            self.updated = True
            
    """
    ##--------------------------------------------------------##
    ## Refresh  function
    ##--------------------------------------------------------##
    """
    def refresh(self):
        if self.updated == True:
            # if updated then we need to redraw the background
            self.drawbackground()
            # For each item in the list we will draw it separately
            for item in self.things_to_draw:
                self.menubackground.blit(item[0], item[1])
            self.updated = False
            
    """
    ##--------------------------------------------------------##
    ## handle input  function
    ##--------------------------------------------------------##
    """
    # handle input will accept a list of 1 or more keys pressed and perform any draws as needed
    # likely the control logic for the menu should be handled by the logic portion of the game
    # with the class maintainging it all. This function may not be needed
    def handleinput(self, keyspressed):
        for key in keyspressed:
            if key == "K_UP":
                if self.cursorloc == 0:
                    self.cursorloc = len(self.menutext)-1
                else:
                    self.cursorloc -= 1
            if key == "K_DOWN":
                if self.cursorloc == len(self.menutext)-1:
                    self.cursorloc = 0
                else:
                    self.cursorloc += 1
        self.drawdescription()                  
        self.drawcursor()
        self.updated = True
            
    """
    ##--------------------------------------------------------##
    ## Wordwrap function
    ##--------------------------------------------------------##
    """
    # the wordwrapfunction will be used for handling longer amounts of
    # text. It will determine how much text will fit on a line in a text
    # box, then return a list of lines. Fontsize should be passed 
    def wordwrap(self, width, text, fontsize):
        font            = pygame.font.SysFont("none", fontsize)
        currenttext     = text.split()
        testtext        = currenttext[0]
        Workingtext     = currenttext[0]
        returntext      = []
        index           = 1
        processing      = True
        if len(currenttext) == 1:
            processing = False
            returntext = [workingtext] # handles single word strings
        while processing:
            if font.size(testtext)[0] > width:
                if workingtext[-1] == " ":
                    returntext.append(workingtext[:-1])
                else:
                    returntext.append(workingtext)
                testtext = ""
                workingtext = ""
                index -= 1
            else:
                if testtext != "":
                    workingtext = (testtext + " ")
                testtext = workingtext + currenttext[(index)]
                index += 1
            if index == len(currenttext):
                if font.size(testtext)[0] > width:
                    returntext.append(workingtext)
                    returntext.append(currenttext[index-1])
                else:
                    returntext.append(testtext)
                processing = False
        return returntext

'''
##----------------------------------------------##
## TESTING BEGINS HERE
##----------------------------------------------##
'''
"""
#initialize pygame
pygame.init()
screen = pygame.display.set_mode((960, 640))


# get cursor icon - image cutter will be replaced later
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
gui_icons = pygame.image.load(os.path.join(os.getcwd(), "Objects", "GUI0.png")).convert_alpha() # load image
tilelist = imagecutter(gui_icons)
tilelistindex = 0
cursor = pygame.transform.scale(tilelist[69], (32, 32))
cursorindex = 0

menuchoices = [["Items", "this is where you could look at your items, but i am lazy and you get none"],
               ["Status", "this is where you could look at your character status"],
               ["Gear", "This is where you could equip your weapons or armor"],
               ["Magic", "This is where you could view or use magic"],
               ["Options", "configure settings"],
               ["Battle Test", "Test the battle system"],
               ["Back", "Closes the menu"]]
menu = GameMenu(screen.get_size(), cursor, menutext=menuchoices)

#class for testing passing things
class player:
    def __init__(self):
        self.inventory = [["this is test inventory", "test inventory"]]
        self.gold = 0
        self.steps = 100
        self.stat = 100
tatertot = player()

keyspressed = []
timeplayed = pygame.time.Clock()
timer = timeplayed.tick()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_UP:
                keyspressed.append("K_UP")                                        
            if event.key == pygame.K_DOWN:
                keyspressed.append("K_DOWN")
            if event.key == pygame.K_SPACE:
                keyspressed.append("K_SPACE")
    if keyspressed != []:
        menu.handleinput(keyspressed)
    
    menu.drawplayinfo()
    menu.refresh()
    screen.blit(menu.menubackground, menu.coords)
    pygame.display.flip()
    keyspressed = []
pygame.quit()
"""
