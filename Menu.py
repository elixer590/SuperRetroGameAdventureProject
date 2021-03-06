import pygame
import EventHandler

class Window:
    """
    Window Class will represent a screen object that can hold text
    __init__:
    """

    def __init__(self, tplSize=(256, 256), blTransparent=False, intalphalevel=128,
                 tplFillColor=(0,0,255), tplBorderColor=(255,255,255), intBorderThickness=5,
                 lstText=[], textcolor=(255,255,255), idxCursor=0):
        self.tplSize            = tplSize
        self.blTransparent      = blTransparent
        self.intAlphaLevel      = intalphalevel
        self.tplFillColor       = tplFillColor
        self.tplBorderColor     = tplBorderColor
        self.intBorderThickness = intBorderThickness

        self.lstText            = lstText
        self.tplTextColor       = textcolor
        self.idxCursor          = idxCursor

        self.Calculate_Size()
        self.objScreen = pygame.Surface(self.tplSize)
        self.draw_background()
        self.Draw_Text()

    def Calculate_Size(self):
        font = pygame.font.SysFont("none", 32)
        intLength = 0
        intNumberOfItems = len(self.lstText)
        intFontHeight = font.size("I")[1]
        for menuItem in self.lstText:
            intCurrent = font.size("-" + menuItem[0])[0]
            if intCurrent > intLength:
                intLength = intCurrent
        intLength += (self.intBorderThickness * 4)
        intHeight = (intFontHeight * intNumberOfItems)
        intHeight += ((self.intBorderThickness * 2) * (intNumberOfItems+1))
        intHeight += (self.intBorderThickness * 2)
        if intNumberOfItems != 0:
            self.tplSize = (intLength, intHeight)




    def draw_background(self):
        if self.blTransparent:
            """"""
            # self.objScreen.convert_alpha()
            # self.objScreen.setalpha(self.intAlphaLevel)
        else:
            self.objScreen.fill(self.tplFillColor)
            self.objScreen.convert()

            # coordinates for drawing lines from corner to corner
            topleftcrn      = (0, 0)
            toprightcrn     = (self.tplSize[0] - 1, 0)
            btmleftcrn      = (0, self.tplSize[1] - 1)
            btmrightcrn     = (self.tplSize[0] - 1, self.tplSize[1] - 1)

            # list of coordinates to draw lines
            menuedges = [topleftcrn,
                         btmleftcrn,
                         btmrightcrn,
                         toprightcrn]

            # horizontal line
            #hrzndiv = [hrzndivleft, hrzndivright]
            #vertdiv = [vertdivtop, vertdivbtm]

            # draw outer border
            pygame.draw.lines(self.objScreen, self.tplBorderColor,
                              True, menuedges, (self.intBorderThickness * 2) - 1)

            """
            # draw inner dividers
            pygame.draw.lines(self.objScreen, self.tplBorderColor,
                              False, hrzndiv, self.intBorderThickness)
            pygame.draw.lines(self.objScreen, self.tplBorderColor, False,
                              vertdiv, self.intBorderThickness)
                              """
    def Draw_Text(self):
        # ["one", "two", "three"]
        font = pygame.font.SysFont("none", 32) #32 is a font size - figure out where this should be provided
        width = int(self.tplSize[0])
        height = int(self.tplSize[1])
        padding = self.intBorderThickness * 2
        objTextBox = pygame.Surface((width, height), pygame.SRCALPHA)
        objTextBox.convert_alpha()
        # width += 10 # after creating box, move away from vertdiv
        lineheight = font.size("I")[1]
        currentheight = padding
        idxLine = 0 # this will tell us which line we are rendering text for
        for option in self.lstText:
            if self.idxCursor == idxLine:
                rendertext = font.render(("-" + option[0]), True, self.tplTextColor)
            else:
                rendertext = font.render(option[0], True, self.tplTextColor)
            rendertext = rendertext.convert_alpha()
            objTextBox.blit(rendertext, (0, currentheight))
            currentheight += lineheight + padding
            idxLine += 1
        self.objScreen.blit(objTextBox,(padding, padding))

    def UpdateCursor(self, newCursorIndex):
        self.idxCursor = newCursorIndex
        self.draw_background()
        self.Draw_Text()


class WindowContainer:

    def __init__(self,eventhandler=EventHandler.EventHandler, intMarginSize=20, parent=None, lstMenus=[], intPadding=10):
        self.objEventHandler = eventhandler  # EventHandler.EventHandler
        self.intMarginSize  = intMarginSize
        self.intPadding     = intPadding

        # sub window should contain a tuple like such
        # ((posX, posY), WindowContainerObject)
        self.SubWindow = (None, None)

        # parent is a pointer back to this windows parent
        self.parent = parent

        # self.control will tell the window which sub window to pass commands to
        # if -1 this is in control
        self.control = True

        #list of menu lists
        self.lstMenus = lstMenus

        # objWindow is the pygame screen for this window
        self.objWindow = Window(lstText=lstMenus, intBorderThickness=(self.intPadding//2))
        self.idxCursor = 0  # this is an index into the menu list

    def CreateNewSubWindow(self, lstMenus, offset=(0,0)):
        if self.control:
            # self.lstSubWindows.append(WindowContainer(addedtext))
            self.SubWindow = (offset, WindowContainer(self.objEventHandler, lstMenus=lstMenus, parent=self, intPadding=self.intPadding))
            self.control = False
        else:
            # self.lstSubWindows[self.control].CreateNewSubWindow(addedtext)
            self.SubWindow[1].CreateNewSubWindow(lstMenus)

    def CreateDrawList(self, tplOffset=(0, 0)):
        # create a list of window objects to draw
        # navigate to the top level menu first and build list as backing up
        # this will leave the bottom layer at the bottom of the list
        tplOffset = ((tplOffset[0] + self.intMarginSize), (tplOffset[1] + self.intMarginSize))

        output = []
        if not self.control:
            tplOffset2 = ((tplOffset[0] + self.SubWindow[0][0]), (tplOffset[1] + self.SubWindow[0][1]))
            output = self.SubWindow[1].CreateDrawList(tplOffset2)
        output.append((self.objWindow.objScreen, tplOffset))
        return output

    def KillChild(self):
        self.SubWindow = (None, None)
        self.control = True

    def DestroyWindow(self):
        if self.control:
            if self.parent is not None:
                self.parent.KillChild()
        else:
            self.SubWindow[1].DestroyWindow()

    def ShowWindowPath(self):
        print(self.text)
        if self.SubWindow is not None:
            self.SubWindow[0].ShowWindowPath()

    def HandleInput(self, lstInput=[]):

        if not self.control:
            self.SubWindow[1].HandleInput(lstInput)
        else:
            for input in lstInput:
                if input == "K_UP":
                    self.idxCursor -= 1
                    if self.idxCursor < 0:
                        self.idxCursor = len(self.lstMenus) - 1
                    self.objWindow.UpdateCursor(self.idxCursor)
                    #print(self.lstMenus[self.idxCursor][0])
                if input == "K_DOWN":
                    self.idxCursor += 1
                    if self.idxCursor == len(self.lstMenus):
                        self.idxCursor = 0
                    self.objWindow.UpdateCursor(self.idxCursor)
                    #print(self.lstMenus[self.idxCursor][0])
                if input == "K_LEFT":
                    self.DestroyWindow()
                if input == "K_RIGHT":
                    #print("K_RIGHT")
                    if len(self.lstMenus[self.idxCursor][1]) != 0 : #if list of submenus is not empty
                        font = pygame.font.SysFont("none", 32)
                        offsetX = font.size("-" + self.lstMenus[self.idxCursor][0])[0]  # determine length idx
                        offsetY = font.size("I")[0] * self.idxCursor # get vertical location
                        offsetY += (self.intPadding*self.idxCursor) #+ (self.intPadding * 2)
                        self.CreateNewSubWindow(self.lstMenus[self.idxCursor][1],
                                                offset=(offsetX,offsetY))
                    else:
                        objFiredEvent = str(self.lstMenus[self.idxCursor][2])
                        objFiredEventDetails = str(self.lstMenus[self.idxCursor][3])
                        # line below is for debugging
                        print("Event Fired: " + str(self.lstMenus[self.idxCursor][2])
                              + " - " + self.lstMenus[self.idxCursor][0])
                        self.objEventHandler.RaiseEvent(EventHandler.Event(objFiredEvent, objFiredEventDetails))


class MenuItem:
    """
    MenuItem class will be used to hold a selectable option in a text window
    """
    def __init__(self, strText, lstSubMenuItems=[], blAction=False, objEvent=None):
        self.strOptionText      = strText # string for displayed output
        self.lstSubMenuItems    = lstSubMenuItems # this will be a list of menuitems
        self.blAction           = blAction # indicator if this line is an action
        self.objEvent           = objEvent # this will be an event object with information about the event being triggered


if __name__ == "__main__":

    class TESTCLASS:

        def __init__(self, eventhandler):
            self.eventhandler = eventhandler
            self.eventhandler.EventListener("Attack", self.testFunction)
            self.eventhandler.EventListener("Black Magic", self.black_magic)
            self.eventhandler.EventListener("White Magic", self.white_magic)

        def testFunction(self, event):
            print("Attack Event Recieved - Event Details: " + str(event))
        def black_magic(self, event):
            print("Black Magic Event Recieved - Event Details: " + str(event))
        def white_magic(self, event):
            print("White Magic Event Recieved - Event Details: " + str(event))

    """initialize variables"""
    pygame.init()
    objScreen = pygame.display.set_mode((640, 640))
    test = Window(tplSize=(640, 640), tplFillColor=(128, 128, 128))

    # TODO - make a function or class that will generates menu items easier
    # that will be needed to populate this data on the fly
    lstTestList =   [
                        ["Attack", [], "Attack", 101]
                        ,["Magic",
                            [
                                ["Black Magic",
                                    [
                                        ["Flare", [],"Black Magic", 201]
                                    ], 0
                                ],
                                ["White Magic",
                                    [
                                        ["Cure", [], "White Magic", 301],
                                        ["Esuna",[], "White Magic", 302],
                                        ["Holy",[], "White Magic", 303]
                                    ], 0
                                ],
                                ["Alex Magic",
                                    [
                                        ["The Best Magic Goes Here", [], 205, 205]
                                    ], 0
                                ]
                            ], 0
                        ]
                        ,["Items", [], 301, 205]
                        ,["Flee", [], 404, 205] #NOT FOUND XD
                    ]

    objEventHandler = EventHandler.EventHandler()
    testwindow = WindowContainer(objEventHandler, lstMenus=lstTestList)
    objEventHandlingTest = TESTCLASS(objEventHandler)
    keyspressed = []
    blRunning = True

    while blRunning:
        # boilerplate input handling
        for event in pygame.event.get():
            """
            returns a list of events. This will clear the event list each time 
            so all event get objects should typically be handled here
            """
            if event.type == pygame.QUIT:
                blRunning = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    blRunning = False
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
        #handle keys pressed
        if len(keyspressed) > 0:
            testwindow.HandleInput(keyspressed)
        #handle events
        #objEventHandler.HandleEvents()
        drawlist = testwindow.CreateDrawList()
        objScreen.blit(test.objScreen, (0, 0))
        for screen in drawlist[::-1]:
            objScreen.blit(screen[0], screen[1])
        pygame.display.flip()
        keyspressed = []

    pygame.quit()