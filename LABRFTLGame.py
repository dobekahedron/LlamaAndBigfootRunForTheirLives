#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 09:33:10 2021

@author: bekah and nolanjw

Program Title: Llama and Bigfoot Run for their Lives!
This game is a match between two iconic figures of new world legend.
It is a battle of finger twister and mental gymnaastics.

Players compete to reach the opposite top corner box, while the forward key
changes after each use.

Splash Screens: A screen is created with logo, game rules, and buttons.
A person can click the buttons to begin the game or end the program
An end splash screen is displayed to state the winner and start a new game

Visuals: A Llama and Bigfoot must traverse a grassy landscape and avoid a 
spreading wildfire. The game has an introductory splash screen with a logo of 
stacking Bigfoot and llama hands/hooves as well as a “dancing” flame!

Initialization: Click “Run”

Objectives: The Llama starts in the bottom left corner, and Bigfoot starts in 
the bottom right corner. Llama is trying to get to the Goal in the upper right, 
and Bigfoot is trying to get to the Goal in the upper left. First one to reach 
their goal wins. 

Rules and Interactions: 2 Players. Each controls one of the characters. The 
players can control which direction their character faces [Up, down, or right/left 
(depending on the character)] by clicking “q”, “a”, and “z” (for Llama) or “p”, 
“;”, and “.” (for Bigfoot). The game randomly prints keys that each player must 
click in order to move their character forward. Once they have clicked the key 
and their character has moved, a new key is generated/printed. 

Challenges: It is Keyboard Twister! In trying to click their assigned keys, 
players will inevitably get in each other’s way. If either player at any point 
clicks the wrong key, the fire spreads. If a character touches the fire, that 
player is sent back to their starting position. Also, the constantly changing 
keys will keep players on their toes! 

Notes: Initially, we planned on having mountain obstacles in the game. However, 
the fire proved challenging enough, so we removed the mountains. 

"""
import turtle
import random, time

# ================ DEFINE CLASSES =========================
class GameStarter():
    '''This class is instantiated when the program loads. Sets up panel and 
    triggers splash screen method.
    '''
    def __init__(self):
        self.panel = turtle.Screen()
        self.w = 1275
        self.h = 850
        self.panel.setup(width=self.w, height=self.h)
        self.panel.listen()
        turtle.colormode(255) # accept 0-255 RGB values
        turtle.tracer(0) # turn off turtle's animation

        self.introduce()
        
    def introduce(self):
        '''runs splash screen'''
        SplashScreen(self.panel)
        self.panel.update
    
# ================ DEFINE SPLASH SCREEN CLASSES =========================
class SplashScreen():
    '''This class manages the Splash Screen. It sets up a panel with logo and 
    rules, and buttons for the user to control game begin and end.
    '''
    def __init__(self, panel): # sets up the panel
        self.panel = panel
        self.running = True # this variable is for the splash screen animation
        self.setup() # calls the method which sets up the panel
    
    def setup(self):
        '''Sets up panel and logo and writes rules'''
        self.panel.setup(width=1275, height=850)
        self.panel.bgcolor(53,40,30)
        self.panel.listen()
        
        #-------Draw order 1: Game Title-------
        self.titledrawer = Title(self.panel) # instantiates the Title class to draw the game name and rules, happens after logo is drawn
        self.titledrawer.titles() 
        self.titledrawer.oval() 
        
        self.logoImages = ["bfhandlt.gif", "llfootrt.gif", "bfhandrt.gif", "llfootlt.gif"] # create a list of the logo images
        self.xlocation = -30
        self.ylocations = [-160, -50, 30, 145]
        
        #-------Draw order 2: Logo-------
        self.logodrawers = [] # create an empty list for the logo drawing objects 
        for i in range(len(self.logoImages)): # fill the list with logodrawers, give location and image
            self.logodrawers.append(BNlogo(self.panel,self.xlocation,self.ylocations[i],self.logoImages[i]))
            time.sleep(.2)
            self.panel.update()
        
        #-------Draw order 3: Rules-------
        self.titledrawer.rules()   # calls the rules method to write the rules on the panel
        self.panel.update()

        self.splash()
        
    def splash(self): 
        '''Creates interactive elements of splash screen (buttons and fire)''' 
        #-------Draw order 4: Buttons-------
        self.playtext = "Play"
        self.stoptext = "Stop"
        self.x = 380 # coordinate locations of the buttons
        self.playy = -100
        self.stopy = -200
        
        self.playbutt = Button(self.x, self.playy, self.panel, self.playtext) # instantiates the class that creates buttons, gives button text as arguement
        self.stopbutt = Button(self.x, self.stopy, self.panel, self.stoptext)
        
        #-------Draw order 5: Update Screen-------
        self.panel.update() # all of the title and rules text and buttons appear at once on the screen. Yes, no, maybe?
            
        #-------Draw order 6: Fire------
        self.hoppingfire = Flame(self.panel) # little fire image shows a glimpse of the peril to come.
            
        while self.running:   
            self.hoppingfire.fireMove()
            
class BNlogo(turtle.Turtle):
    '''This class inherits turtle and adds logo images to its shape. 
    The logo images are taken to the desired locations to achieve a
    teamwork hand-stacking logo animation with llama and bigfoot.
    '''
    def __init__(self, panel, x, y, image="llamafoot.gif"):
        super().__init__(visible=True)
        self.up()
        self.panel = panel
        self.x = x
        self.y = y
        
        self.picture = image
        self.panel.addshape(self.picture)
        self.shape(self.picture)
        
        self.logo() #automatically call the next function once instantiated
        
    def logo(self):
        '''Executes individual step of the hand stacking animation - takes logo to position'''
        self.goto(self.x, self.y)    # takes the logo turtle to go to its place
        
class Title(turtle.Turtle):
    '''This class writes the game title and list of rules of the game onto the 
    panel, and draws an oval to contain the logo animation. 
    
    methods:        oval()
                    titles()
                    rules()
    '''
    def __init__(self, panel, x=0, y=0, text ="Llama and Bigfoot Run For Their Lives!"):
        super().__init__(visible=False)
        self.panel = panel
        self.up()
        
        #creating lists with the rules so that they can be written on multiple lines more easily
        self.welcometext = ["Use keyboard to move your player to safety.", 
                            "Forward movement key changes after each use.", "Don't get burned!"]
        self.llamarules = ["Llama turn keys:", "up = q", "side = a", "down = z", 
                           "move forward = key in upper RIGHT box"]
        self.bigfootrules = ["Bigfoot turn keys:", "up = p", "side = ;", "down = .", 
                             "move forward = key in upper LEFT box"]
        self.rulesposx = -590
        self.rulesposy = 180
        self.fontspacer = 30
        
    def oval(self):
        '''Draws an oval for the logo'''
        self.width(5)
        self.goto(105,-207)
        self.pencolor(247, 92, 3)
        self.fillcolor("white")
        self.down()
        self.begin_fill()
        self.seth(45) # this tilts the turtle so that oval is upright
        for i in range(2):
            self.circle(290, 90) # drawing an oval: https://pythonturtle.academy/tutorial-drawing-an-oval-with-python-turtle/
            self.circle(170, 90)
        self.end_fill()
        self.up()    
    
    def titles(self):
        '''draws the title of the game'''
        self.gamename = "Llama and Bigfoot Run for their Lives!"
        self.pencolor(5, 5, 5) #160, 92, 3)
        self.goto(-350,275) # go to the top left to write title
        self.write(self.gamename, font=("Comic Sans",40,"bold")) #uses the style from the init method to write the title
        self.pencolor(247, 92, 3)
        self.goto(-351,276)
        self.write(self.gamename, font=("Comic Sans",40,"bold"))
    
    def rules(self):
        '''this method sets up the splash screen font and draws the rules'''
        self.pencolor(247, 157, 38)
        self.goto(self.rulesposx, self.rulesposy)
        
        #Setup as a for loop so rules can easily be added above and written in new locations here
        for t in range(len(self.welcometext)):
            self.write(self.welcometext[t], font=("Helvetica",18)) 
            self.rulesposy -= self.fontspacer
            self.goto(self.rulesposx, self.rulesposy)
            
        self.rulesposy -=40
        self.pencolor(100, 131, 64) #55, 154, 103)
        self.goto(self.rulesposx, self.rulesposy)
        
        for u in range(len(self.llamarules)):
            self.write(self.llamarules[u], font=("Helvetica",20)) 
            self.rulesposy -= self.fontspacer
            self.goto(self.rulesposx, self.rulesposy)
            
            
        self.rulesposy -=40
        self.goto(self.rulesposx, self.rulesposy)
        
        for v in range(len(self.bigfootrules)):
            self.write(self.bigfootrules[v], font=("Helvetica",20)) 
            self.rulesposy -= self.fontspacer
            self.goto(self.rulesposx, self.rulesposy)
            
            
        self.goto(self.rulesposx, self.rulesposy - self.fontspacer)
        self.pencolor(247, 157, 38)
        self.write("Win by reaching the top opposite corner. Press play when ready.", font=("Helvetica",18))
              
class Button(Title):
    '''This class draws a button with text for the user to click to control program.
    Inherits the Title class, to use turtle settings and font style.
    
    methods:        writeText()
                    clickaction()   Controls the click function
                    play()   This starts the game manager so they can play
                    stop()   This closes the program altogher
    '''
    
    def __init__(self, x, y, panel, text="Play"):  # enables polymorphism; multiple buttons w/ different text
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.butttext = text # text for button will be "play" or "stop"
        self.panel = panel
        self.button = turtle.Turtle(shape='square') # make a square-shaped turtle for button
        self.button.shapesize(3, 3, 1)
        self.button.color(100, 131, 64) #0, 204, 102)
        self.button.up()
        self.button.goto(self.x, self.y) # take the button to its location
        
        self.writeText()
        self.button.onclick(self.clickaction) # when I am clicked, call the clickaction function
        
    def writeText(self):
        '''Write text next to button'''
        self.goto(self.x+50,self.y-30) # take turtle to go to the button turtle to write text on it
        self.pencolor(247, 92, 3)
        self.write(self.butttext, font=("Helvetica",30,"bold"))
        
    def clickaction(self, x, y): 
        '''This method determines the text value of the button, and sends you to that method when clicked'''
        if self.butttext=="Play":
            self.play()
        elif self.butttext=="Stop":
            self.stop()
            
    def play(self): 
        '''Method which imports the game play script'''
        self.panel.clear()
        LandscapeSetup(self.panel)

    def stop(self): 
        '''Method which ends the program'''
        turtle.bye()
 
class Flame(turtle.Turtle):
    '''This little turtle draws a fire image which marches around until the user clicks play'''
        
    def __init__(self, panel):
        super().__init__()  
        self.panel = panel
        self.fireIMG = "Fire.gif"
        self.panel.addshape(self.fireIMG)
        self.shape(self.fireIMG)
        
    def fireMove(self):
        '''Marque animation'''
        self.up()
        self.goto(random.randint(-500,500),355) # jumping fire is constrained to top of screen above title
        time.sleep(.4)
        self.panel.update()

# ================ DEFINE GAMEPLAY CLASSES =========================
        
class LandscapeSetup(turtle.Turtle): #Sets up the playing field
    '''Creates turtles for background landscaping and setting up player goal boxes
    '''
    def __init__(self, panel):
        super().__init__(visible = False)
        turtle.colormode(255) # accept 0-255 RGB values
        turtle.tracer(0) # turn off turtle's animation
        self.panel = panel
        self.landscapeIMG = "Landscape.gif"
        self.panel.addshape(self.landscapeIMG)
        self.shape(self.landscapeIMG)
        self.stamp()
        self.goalBox() # would maybe be cleaner to use arguements for color and location here,
        self.gameManager = GameManager(self.panel)
        
    def goalBox(self): #, x, y, color):
        '''Draws the playing field'''
        #Draws bigfoot goal box
        self.up()
        self.color(53,40,30)
        self.goto(-637.5,325)
        self.down()
        self.begin_fill()
        for i in range(4):
            self.forward(100)
            self.left(90)
        self.end_fill()
        
        #Draws llama goal box
        self.up()
        self.goto(627.5,325)
        self.color(255,253,208)
        self.right(180)
        self.down()
        self.begin_fill()
        for i in range(4):
            self.forward(100)
            self.right(90)
        self.end_fill()
        self.panel.update()
        
class GameManager():
    '''This class contains all interaction methods for the game. 
    Creates objects:    llama
                        bigfoot
                        llamaScribe
                        bigfootScribe
                        
    Methods:            wrongClick()
                        burnCheck()
    
    Controls vars:      burnZone
                        llamaKey
                        bigfootKey
                        
    '''
    def __init__(self, panel):
        self.panel = panel
        self.llama = Player(self.panel)
        self.bigfoot = Player(self.panel, creatureImage="Bigfoot.gif",startPoint=(590,-375),startDirection=180,
                 upKey="p",sideKey=";",downKey=".",winXCor=-537.5)
        self.burnZone = []
        self.spark = Fire(self.panel,self.burnZone)
        self.burnZone.append(self.spark)
        
        self.selectLlamaKey()
        self.selectBigfootKey()
        
        self.llamaScribe = turtle.Turtle()
        self.bigfootScribe = turtle.Turtle()
        self.llamaScribe.hideturtle()
        self.llamaScribe.up()
        self.llamaScribe.color(53,40,30)
        self.bigfootScribe.hideturtle()
        self.bigfootScribe.up()
        self.bigfootScribe.color(255,253,208)

        self.writeLlamaKey()
        self.writeBigfootKey()
        
        self.panel.update()
        
        #----------What happens when keys are pressed in the game------------
        # if correct key is pressed, go to click action method        
        self.panel.onkey(self.llamaClickActions,self.llamaKey)  
        self.panel.onkey(self.bigfootClickActions,self.bigfootKey)
        
        # if any of the wrong keys are pressed, call the wrongClick method to spread the fire

        for wl in self.wrongLlamaKey: 
            self.panel.onkey(self.wrongClick,wl)
            
        for wb in self.wrongBigfootkey:
            self.panel.onkey(self.wrongClick,wb)
        
    def llamaClickActions(self):
        ''' When llama player presses the correct key, these actions happen:
                Move forward in the current direction
                Check if on fire
                Check if win
                Generate a new key
                Send llama's scribe to write the newly generated key
                Un-bind keys to functions
                Re-bind keys to functions using new target keys
        '''
        
        self.llama.run()
        self.llama.winCheck()
        if self.burnCheck(self.llama):
            self.llama.goto(-600,-375)
        
        #Unbind keys/functions
        self.panel.onkey(None,self.llamaKey)
        
        for ul in self.wrongLlamaKey:
            self.panel.onkey(None,ul)

        #     self.panel.onkey(None,self.wrongLlamaKey[ul])
        
        self.selectLlamaKey() # key has been used, so call the method that generates a new one
        
        #Rebind functions with new keys
        for rl in self.wrongLlamaKey:
            self.panel.onkey(self.wrongClick, rl)
        
        self.writeLlamaKey()
        self.panel.onkey(self.llamaClickActions,self.llamaKey)
        self.panel.update()
        
    def bigfootClickActions(self):
        '''  When bigfoot player presses the correct key, these actions happen:
                Move forward in the current direction
                Check if on fire
                Check if win
                Generate a new key
                Send bigfoot's scribe to write the newly generated key
                Un-bind keys to functions
                Re-bind keys to functions using new target keys
        '''
        self.bigfoot.run()
        self.bigfoot.winCheck()
        if self.burnCheck(self.bigfoot):
            self.bigfoot.goto(590,-375)        
        
        #Unbind keys/functions
        self.panel.onkey(None,self.bigfootKey)
        
        for ub in self.wrongBigfootKey:
            self.panel.onkey(None,ub)
        
        self.selectBigfootKey() # key has been used, so call the method that generates a new one
        
        #Rebind keys/functions
        for rb in self.wrongBigfootKey:
            self.panel.onkey(self.wrongClick,rb)
        
        self.writeBigfootKey()
        self.panel.onkey(self.bigfootClickActions,self.bigfootKey)
        self.panel.update()
        
    def wrongClick(self):
        '''When a key that is not the target key is pressed, the fire spreads and it checks whether 
        Llama or Bigfoot are on fire using burnCheck()'''
        for i in range(len(self.burnZone)):
            self.burnZone[i].spread()
        if self.burnCheck(self.llama):
            self.llama.goto(-600,-375)
        if self.burnCheck(self.bigfoot):
            self.bigfoot.goto(590,-375)
        self.panel.update()
            
    def burnCheck(self,turt,buffer=30):
        '''Checks whether a player is touching fire'''
        self.target = self.burnZone
        self.x = turt.xcor()
        self.y = turt.ycor()
        for i in range(len(self.target)): # source: collisionBubbles.py in class repo
            self.targX = self.target[i].xcor()
            self.targY = self.target[i].ycor()
            if round(self.targX)-buffer<=round(self.x)<=round(self.targX)+buffer and round(self.targY)-buffer<=round(self.y)<=round(self.targY)+buffer:
                return True, i # collision detected. Return True *and position in list* and stop running the method.
        return False # no collision detected in list. Return False and stop running the method.
        self.panel.update()
        
    def selectLlamaKey(self):
        '''Randomly selects the Llama Target Key'''
        self.llamaList = ["w","r","y","i","d","g","j","l","x","v","n"]
        self.llamaKey = random.choice(self.llamaList)
        self.wrongLlamaKey = self.llamaList
        self.wrongLlamaKey.remove(self.llamaKey)

    def selectBigfootKey(self):
        '''Randomly selects the Bigfoot Target Key'''
        self.bigfootList = ["e","t","u","o","s","f","h","k","c","b","m"]
        self.bigfootKey = random.choice(self.bigfootList)
        self.wrongBigfootKey = self.bigfootList
        self.wrongBigfootKey.remove(self.bigfootKey)
        
    def writeLlamaKey(self):
        '''Writes the Target Llama Key in the Llama Goal Box'''
        self.llamaScribe.clear()
        self.llamaScribe.goto(577,355)
        self.llamaScribe.down()
        self.llamaScribe.write(self.llamaKey,font=("Arial",30,"normal"))
        self.llamaScribe.up()
        
    def writeBigfootKey(self):
        '''Writes the Target Bigfoot Key in the Bigfoot Goal Box'''
        self.bigfootScribe.clear()
        self.bigfootScribe.goto(-596,355)
        self.bigfootScribe.down()
        self.bigfootScribe.write(self.bigfootKey,font=("Arial",30,"normal"))
        self.bigfootScribe.up()
        
        
class Player(turtle.Turtle):
    '''This class creates player objects that are trying to win the game.
    Methods to control player:          run
                                        turnUp
                                        turnSide
                                        turnDown                                #FOR WHAT!
    Methods controling win conditions:
                                    winCheck
    '''
    
    def __init__(self, panel, creatureImage="Llama.gif",startPoint=(-600,-375),startDirection=0,
                 upKey="q",sideKey="a",downKey="z",winXCor=527.5):
        super().__init__()
        self.creatureIMG = creatureImage
        self.panel = panel
        self.panel.addshape(self.creatureIMG)
        self.shape(self.creatureIMG)
        self.startPt = startPoint
        self.upKey = upKey
        self.sideKey = sideKey
        self.downKey = downKey
        self.up()
        self.goto(self.startPt)
        self.startD = startDirection
        self.seth(self.startD)
        self.winXCor = winXCor
        self.name = None
        
        self.panel.onkey(self.turnUp,self.upKey)
        self.panel.onkey(self.turnSide,self.sideKey)
        self.panel.onkey(self.turnDown,self.downKey)

    def run(self):
        '''Moves the players'''
        self.forward(50)
        self.xPos = self.xcor()
        self.yPos = self.ycor()
        if 627.5<=self.xPos or self.xPos<=-637.5 or 426<=self.yPos or self.yPos<=-426:
            self.back(50)
        
    def turnUp(self):
        '''Sets orientation of player upward'''
        self.seth(90)
        
    def turnSide(self):
        '''Sets player orientaiton to the side in the direction of that player's respective goal'''
        self.seth(self.startD)
        
    def turnDown(self): #FOR WHAT!
        '''Sets the player orientation downward'''
        self.seth(270)
        
    def winCheck(self):
        '''Checks whether a player has reached its goal box. If a player has reached its goal box, 
        the name of the player is saved and used to display a customized win screen before restarting the game'''
        self.playerX = self.xcor()
        self.playerY = self.ycor()
        if abs(self.playerX)>abs(self.winXCor) and self.playerY>325:
            self.name = self.creatureIMG[:-4] # removes file extension characters from creature image file name and saves to winner name variable
            self.winner = turtle.Turtle(visible=False) # create a new turtle to wish the winner a good game
            self.winner.up()
            self.winner.goto(-380,320)
            self.winner.color(53,40,30)
            self.winner.write("CONGRATULATIONS WINNER!", font=("Helvetica", 40, "normal"))
            
            if self.name == "Llama":
                self.llamabig = "BigLlama.gif" # large copy of llama
                self.panel.addshape(self.llamabig)
                self.winner.shape(self.llamabig)
                
            elif self.name == "Bigfoot":
                self.bigfootbig = "BigBigfoot.gif" # large copy of bigfoot
                self.panel.addshape(self.bigfootbig)
                self.winner.shape(self.bigfootbig)
                
            self.winner.goto(-50,0) 
            self.winner.stamp()
            self.panel.update()
            time.sleep(8)
            self.panel.clear()
            
            SplashScreen(self.panel) # after clearing the panel, go back to display the splash screen again
            self.panel.update()
            
class Fire(turtle.Turtle):
    '''This class creates fire objects, with a method to allow them to spread in random directions
    '''
    def __init__(self, panel, burnZone):
        super().__init__()
        self.panel = panel
        self.burnZone = burnZone
        self.up()
        self.seth(random.randint(0,360))
        self.fireIMG = "Fire.gif"
        self.panel.addshape(self.fireIMG)
        self.shape(self.fireIMG)
        
    def spread(self):
        '''Causes the fire to randomly move out in 4 directions'''
        self.forward(random.randint(50,90))
        self.burnZone.append(Fire(self.panel,self.burnZone))
    

# ================ EXECUTION =========================
if __name__=='__main__':
    GameStarter()
    turtle.mainloop()  # allows for user interactions; handles cleanup