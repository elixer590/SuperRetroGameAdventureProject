# the objective of this will be to create a battle menu
import pygame
import random
import os
import animation
import glb # super globals



class BattleMenu:
    # this will hold the battle menu data for initialization
    """
things this will need to do:
1.) the battle menu should draw the battle background
2.) the battle menu will need to load the stat box (right side)
    a.) Need to determine the list of characters
    b.) Need to output data to correct location and output
3.) an options box should be loaded (bottom or bottom right)
    a.) need to determine what options are available
        i.) Current space allows for maybe 4 options
        ii.) possibly have sub options show in a new window at the bottom
        iii.) remove window at bottom once its not needed        
4.) the battle itself should be drawn
    a.) need to determine character animation state
    b.) need to dtermine and place characters
5.) need to handle battle actions

Will attempt to reuse as much of the menu class already wrote for this
    """

    def __init__(self, size, cursor, battleimage, playerlist, enemylist,
                 actionlist, transparent=False, alphalevel=128, fillcolor=(0,0,255),
                 bordercolor=(255,255,255), borderthickness=5,
                 coords=(0,0), menutext=[["nothing here"]], fontsize=32,
                 optionsfontsize=48, textcolor=(255,255,255)):
        # set instance variables
        self.size               = size # should be a tuple
        self.cursor             = cursor
        self.cursorloc          = 0 # this is an index
        self.background         = pygame.transform.scale(battleimage, self.size)
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
        self.anim_updated       = False #animation updated
        self.things_to_draw     = []
        self.anim_window        = pygame.Surface((int(self.size[0]*0.75), int(self.size[1]*0.75)), pygame.SRCALPHA)
        self.menubackground     = pygame.Surface(self.size)
        self.outputscreen       = pygame.Surface(self.size)
        self.popupscreen        = pygame.Surface((int(self.size[0]*0.75), int(self.size[1] *0.25)), pygame.SRCALPHA)
        self.playerlist         = playerlist # this should be a list of player objects
        self.enemylist          = enemylist # this should be a list of enemy objects
        self.actionlist         = actionlist # list for the action window
        self.timer              = 0
        # output screen will be the menubackground surface, followed
        # by character animations. this will save proc time on redrawing many menus
        self.anim_window.convert_alpha()
        self.popupscreen.convert_alpha()
        # Perform initialization actions
        self.drawbackground()
        self.drawstatwindow()
        self.drawplaystats()
        self.drawactionwindow()
        #self.drawdescription()
        self.drawcursor()
        self.drawblankcombatwindow()
        

    """
    ##--------------------------------------------------------##
    ## Draw background function
    ##--------------------------------------------------------##
    """
    # draws the main window - this will be called in other drawing
    # functions to ensure that if data is drawn to the menu screen it
    # be drawn over a fresh image. also called on __init__ for init
    def drawbackground(self):
        self.menubackground.blit(self.background, (0,0))

    """
    ##--------------------------------------------------------##
    ## Drawmenuoptions function
    ##--------------------------------------------------------##
    """
    #draws options that will be on the right side of the screen
    """def drawmenuoptions(self):
        font        = pygame.font.SysFont("none", self.optionsfontsize)
        width       = int(self.size[0]*0.25)
        height      = int(self.size[1]*0.75)
        optionsbox  = pygame.Surface((width, height), pygame.SRCALPHA)
        optionsbox.convert_alpha()
        # width += 10 # after creating box, move away from vertdiv
        lineheight = font.size("I")[1] # I is tall, works for estimation
        currentheight = 20
        for line in self.menutext:
            rendertext = font.render(line[0], True, self.textcolor)
            rendertext = rendertext.convert_alpha()
            optionsbox.blit(rendertext, (0, currentheight))
            currentheight += 2*lineheight
        self.UpdateDrawList([optionsbox, ((width*3)+10, 0),"drawmenuoptions"])"""
    ###porting this function
    def drawstatwindow(self):
        #make a menu object one quarter the width of the screen of the screen
        width = int(self.size[0]/4)
        height = self.size[1]
        color = self.textcolor
        battlescreen = pygame.Surface((width, height))
        battlescreen.convert()
        battlescreen.fill(self.fillcolor)
        battlescreen.set_alpha(self.alphalevel)
        
        # menuedges is a list of coordinates
        menuedges = [(0,0),
                     (0, height -1),
                     (width -1, height -1),
                     (width -1, 0)]
        bottomsubdiv = [(0, int(height * 0.75)), (width,int(height * 0.75))]
        pygame.draw.lines(battlescreen, self.bordercolor, True, menuedges, 9)
        pygame.draw.lines(battlescreen, self.bordercolor, False, bottomsubdiv, 5)
        # at this point the box is drawn but there is no character data shown
        self.UpdateDrawList([battlescreen, ((int(self.size[0]*0.75)), 0), "drawstatwindow"])

    """
    ##--------------------------------------------------------##
    ## Drawplaystats function
    ##--------------------------------------------------------##
    """
    def drawplaystats(self, size=28):
        playerlist = self.playerlist
        width = int(self.size[0]/4)
        height = int(self.size[1]*0.75)
        color = self.textcolor
        battlescreen = pygame.Surface((width, height), pygame.SRCALPHA)
        battlescreen.convert_alpha()
        # above setup window to draw to
        allplayerstatboxsize = (width, height)
        allplayerstatbox = pygame.Surface((allplayerstatboxsize), pygame.SRCALPHA)
        #allplayerstatbox.set_alpha(0)
        allplayerstatbox.convert_alpha()
        playerstatboxsize = ((width), int(height*0.25))
        playerstatbox = pygame.Surface((playerstatboxsize), pygame.SRCALPHA)
        #playerstatbox.set_alpha(0)
        playerstatbox.convert_alpha()
        drawboxheight = 0
        # now that we have an object the size of the boxes we need to write data to it
        font = pygame.font.SysFont("none", size)
        lineheight = font.size("test")[1]
        currentheight = 10 # start 10 pixels from the top of the box
        for character in playerlist:
            rendername = font.render(character.Name, True, color)
            rendername = rendername.convert_alpha()
            renderhp = font.render("HP: " + str(character.HitPoints)+ "/" + str(character.MaxHitPoints), True, color)
            renderhp = renderhp.convert_alpha()
            renderhpbar = font.render("draw an HP Bar here", True, color)
            renderhpbar = renderhpbar.convert_alpha()
            rendermp = font.render("MP: " + str(character.MP)+ "/" + str(character.MaxMP), True, color)
            rendermp = rendermp.convert_alpha()
            rendermpbar = font.render("draw an MP Bar here", True, color)
            rendermpbar = rendermpbar.convert_alpha()
            playerstatbox.blit(rendername, (20, currentheight))
            currentheight += lineheight
            playerstatbox.blit(renderhp, (20, currentheight))
            currentheight += lineheight
            playerstatbox.blit(renderhpbar, (20, currentheight))
            currentheight += lineheight
            playerstatbox.blit(rendermp, (20, currentheight))
            currentheight += lineheight
            playerstatbox.blit(rendermpbar, (20, currentheight))
            currentheight = 10
            allplayerstatbox.blit(playerstatbox, (0, drawboxheight))
            drawboxheight += playerstatboxsize[1]
            playerstatbox = pygame.Surface((playerstatboxsize), pygame.SRCALPHA)
            #playerstatbox.set_alpha(0)
            playerstatbox.convert_alpha()
        battlescreen.blit(allplayerstatbox,(0,0))
        self.UpdateDrawList([battlescreen, ((int(self.size[0]*0.75)), 0), "drawplaystats"])

        
    """
    ##--------------------------------------------------------##
    ## Drawdescription function
    ##--------------------------------------------------------##
    """
    # draw lower window text
    def drawdescription(self):
        text = self.actionlist[self.cursorloc][1]
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
    ## drawactionwindow function
    ##--------------------------------------------------------##
    """
    def drawactionwindow(self):
        # draws the action window
        # define the screen area
        width = int(self.size[0]*0.25)
        height = int(self.size[1]*0.25)
        actionbox = pygame.Surface((width, height), pygame.SRCALPHA)
        actionbox.convert_alpha()
        font = pygame.font.SysFont("none", self.optionsfontsize)
        lineheight = font.size("I")[1]
        currentheight = 10
        for action in self.actionlist:
            rendertext = font.render(action, True, self.textcolor)
            rendertext = rendertext.convert_alpha()
            actionbox.blit(rendertext, (20, currentheight))
            currentheight += lineheight+2    
        self.UpdateDrawList([actionbox, ((int(self.size[0]*0.75)), int(self.size[1]*0.75)), "drawactionwindow"])
                    
        
    """
    ##--------------------------------------------------------##
    ## Drawcursor function
    ##--------------------------------------------------------##
    """
    def drawcursor(self):
        font = pygame.font.SysFont("none", self.optionsfontsize)
        lineheight = (font.size("I")[1])
        cursorX = self.size[0] - 100
        cursorY = ((self.cursorloc*(lineheight+2))+12) + int(self.size[1]*0.75)
        self.UpdateDrawList([self.cursor, (cursorX, cursorY), "drawcursor"])

    """
    ##--------------------------------------------------------##
    ## Draw_bat_anim_win function
    ##--------------------------------------------------------##
    """
    # draws the character and enemy actions
    def draw_bat_anim_win(self):
        bat_anim_window = pygame.Surface((int(self.size[0]*0.75), int(self.size[1]*0.75)), pygame.SRCALPHA)
        bat_anim_window.convert_alpha()
        drawx = int(self.size[0]/20)-10
        drawy = int(self.size[1]/4)+90
        for character in self.enemylist:
            # check current animation state and reset to idle state if the animation is over
            if character.animate.frame == len(character.animate.frame_dict[character.animate.cur_animation])-1:
                if self.timer - character.animate.lastframetime >= character.animate.animationfreq:
                    character.animate.sel_animation("battle_idle")
            sprite = character.animate.do(self.timer)
            sprite = pygame.transform.scale2x(sprite)
            bat_anim_window.blit(sprite, (drawx, drawy))
            drawx += int(self.size[0]/18)
            drawy += int(self.size[1]/12)
        drawx = int(self.size[0]/2)-90
        drawy = int(self.size[1]/4)+20
        for character in self.playerlist:
            # check current animation state and reset to idle state if the animation is over
            if character.animate.frame == len(character.animate.frame_dict[character.animate.cur_animation])-1:
                if self.timer - character.animate.lastframetime >= character.animate.animationfreq:
                    character.animate.sel_animation("battle_idle")
            sprite = character.animate.do(self.timer)
            sprite = pygame.transform.scale2x(sprite)
            bat_anim_window.blit(sprite, (drawx, drawy))
            drawx += int(self.size[0]/18)
            drawy += int(self.size[1]/12)
        self.anim_window = bat_anim_window
        
    
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
    def refresh(self, timer):
        self.timer = timer
        self.draw_bat_anim_win()
        if self.updated == True:
            # if updated then we need to redraw the background
            self.drawbackground()
            # For each item in the list we will draw it separately
            for item in self.things_to_draw:
                self.menubackground.blit(item[0], item[1])
            self.updated = False
        self.outputscreen.blit(self.menubackground, (0,0))
        self.outputscreen.blit(self.anim_window, (0,0))
        if glb.combat.trigger_ready:
            self.outputscreen.blit(self.popupscreen, ((0, (int(self.size[1]*0.75)-1))))
            
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
                    self.cursorloc = len(self.actionlist)-1
                else:
                    self.cursorloc -= 1
            if key == "K_DOWN":
                if self.cursorloc == len(self.actionlist)-1:
                    self.cursorloc = 0
                else:
                    self.cursorloc += 1
        #self.drawdescription() # currently no description
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
        workingtext     = currenttext[0]
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

    """
    ##--------------------------------------------------------##
    ## drawblankcombatwindow function
    ##--------------------------------------------------------##
    """
    def drawblankcombatwindow(self):
        # make a window at the bottom of the screen
        width       = int(self.size[0]*0.75)
        height      = int(self.size[1] *0.25)+1
        color = self.textcolor
        self.popupscreen = pygame.Surface((width, height), pygame.SRCALPHA)
        self.popupscreen.convert_alpha()
        combatscreen = pygame.Surface((width, height))
        combatscreen.convert()
        combatscreen.fill(self.fillcolor)
        combatscreen.set_alpha(self.alphalevel)
        
        # menuedges is a list of coordinates
        """menuedges = [(0,0),
                     (0, height -1),
                     (width -1, height -1),
                     (width -1, 0)]"""
        menuedges = [(width -1, 0),
                     (0,0),
                     (0, height -1),
                     (width -1, height -1)]
                     
        pygame.draw.lines(combatscreen, self.bordercolor, False, menuedges, 9)
        self.popupscreen.blit(combatscreen, (0,0))
        #self.popupscreen = combatscreen

    """
    ##--------------------------------------------------------##
    ## Drawcombatwindow function
    ##--------------------------------------------------------##
    """        
    # draw lower window text
    def drawcombatwindow(self, text):
        width       = (int(self.size[0]*0.75) - 20)
        height      = (int(self.size[1] *0.25) - 20)
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
        self.popupscreen.blit(lowerbox, (10, 10))

    """
    ##--------------------------------------------------------##
    ## Clearcombatwindow function (maybe not needed, just reinit the window?
    ##--------------------------------------------------------##
    """

     

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

battlescreen = pygame.image.load(os.path.join(os.getcwd(), "Objects", "battleback11.png")).convert()

menuchoices = [["Attack", "You could totes attack if I had built that function by now"],
               ["Magic", "Be all like Gandalf up in this bitch"],
               ["Item", "This ones also not functional, surprised?"],
               ["Flee", "Only works if you are French"]]


actionbox = ["Attack", "Magic", "Item", "Flee"]

'''
##----------------------------------------------##
## TEST CLASS FOR CREATING PARTY
##----------------------------------------------##
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
        dieone = random.randrange(1,6)
        dietwo = random.randrange(1,6)
        diethree = random.randrange(1,6)
        statvalue = dieone + dietwo + diethree
        return statvalue

playerspritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "actor_10.png")).convert()
playerspritesheet.set_colorkey(playerspritesheet.get_at((0,0)))
playerspritesheet.convert_alpha()
playerspritelist = imagecutter(playerspritesheet, 32)

glb.player1 = CharacterContainer("testboy", "test", True)
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52]}
glb.player1.animate = animation.animation(playerspritesheet, player_frame_dict,
                                         "walk_up", tilesize=(32,32))
glb.player2 = CharacterContainer("testboy", "test", True)
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52]}
glb.player2.animate = animation.animation(playerspritesheet, player_frame_dict,
                                         "walk_up", tilesize=(32,32))
glb.player3 = CharacterContainer("testboy", "test", True)
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52]}
glb.player3.animate = animation.animation(playerspritesheet, player_frame_dict,
                                         "walk_up", tilesize=(32,32))
glb.player4 = CharacterContainer("testboy", "test", True)
player_frame_dict = {"walk_down": [0, 1, 2, 1],
                     "walk_left": [12, 13, 14, 13],
                     "walk_right": [24, 25, 26, 25],
                     "walk_up": [36, 37, 38, 37],
                     "attack": [55, 56,68,67],
                     "battle_idle": [51, 52, 53, 52]}
glb.player4.animate = animation.animation(playerspritesheet, player_frame_dict,
                                         "walk_up", tilesize=(32,32))

glb.enemy1 = CharacterContainer("testenemy", "test", False)
enemy1spritesheet = playerspritesheet = pygame.image.load(os.path.join(os.getcwd(), "Objects", "spectre.png")).convert()
enemy1_frame_dict = {"battle_idle": [16,17,18,19,18,17],
                     "enter": [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                     "hide": [13,12,11,10,9,8,7,6,5,4],
                     "hidden": [4,3,2,3]}
glb.enemy1.animate = animation.animation(enemy1spritesheet, enemy1_frame_dict,
                                         "enter", tilesize=(80,70))
glb.enemy2 = CharacterContainer("testenemy", "test", False)
enemy1_frame_dict = {"battle_idle": [16,17,18,19,18,17],
                     "enter": [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                     "hide": [13,12,11,10,9,8,7,6,5,4],
                     "hidden": [4,3,2,3]}
glb.enemy2.animate = animation.animation(enemy1spritesheet, enemy1_frame_dict,
                                         "enter", tilesize=(80,70))
glb.enemy3 = CharacterContainer("testenemy", "test", False)
enemy1_frame_dict = {"battle_idle": [16,17,18,19,18,17],
                     "enter": [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                     "hide": [13,12,11,10,9,8,7,6,5,4],
                     "hidden": [4,3,2,3]}
glb.enemy3.animate = animation.animation(enemy1spritesheet, enemy1_frame_dict,
                                         "enter", tilesize=(80,70))
glb.enemy4 = CharacterContainer("testenemy", "test", False)
enemy1_frame_dict = {"battle_idle": [16,17,18,19,18,17],
                     "enter": [0,1,2,3,4,5,6,7,8,9,10,11,12,13],
                     "hide": [13,12,11,10,9,8,7,6,5,4],
                     "hidden": [4,3,2,3]}
glb.enemy4.animate = animation.animation(enemy1spritesheet, enemy1_frame_dict,
                                         "enter", tilesize=(80,70))


enemylist = [glb.enemy1, glb.enemy2, glb.enemy3, glb.enemy4]
playerlist = [glb.player1, glb.player2, glb.player3, glb.player4]

'''
##----------------------------------------------##
## final init and test loop
##----------------------------------------------##
'''
menu = BattleMenu(screen.get_size(), cursor, battlescreen, playerlist, enemylist, actionbox, fillcolor=(75,75,75), menutext=menuchoices)

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
            if event.key == pygame.K_LEFT:
                keyspressed.append("K_LEFT")
                glb.enemy1.animate.sel_animation("enter")
            if event.key == pygame.K_RIGHT:
                keyspressed.append("K_RIGHT")
                glb.player1.animate.sel_animation("attack")
            if event.key == pygame.K_SPACE:
                keyspressed.append("K_SPACE")
    if keyspressed != []:
        menu.handleinput(keyspressed)
    
    #menu.drawplayinfo()
    menu.refresh(timer)
    timer += timeplayed.tick(60)
    screen.blit(menu.outputscreen, (0,0))
    pygame.display.flip()
    keyspressed = []
pygame.quit()
"""
