from tkinter import *
from tkinter import messagebox

#-----------------------------------    

class Vector:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

#-----------------------------------    

class GameObject:
    
    def __init__(self, pos):
        self.position = Vector(pos[0], pos[1])
    
    def isCollidingWith(self, otherGameObject):  # Checks collosion between ball
                                                 #   and background and paddles. Returns
                                                 #   True if they are colliding,
                                                 #   False otherwise.
        global x, y, secCount     

        a = Game.canvas.bbox(self.ball.box)
        b = Game.canvas.bbox(otherGameObject.box)
        
        if otherGameObject == self.back:
            if not a[2] in range(b[0], b[2]):   #Right side collision ball with back
                self.xState = False
                return True
            elif not a[0] in range(b[0], b[2]): #Left side collision ball with back
                self.xState = True
                return True
            elif a[1] <= b[1]:                  #1+ score for p2 or enemy, bottom collision with background
                x = 320
                y = 240
                self.score2 += 1
                
                self.p1.velocity = 6
                self.p2.velocity = 6
                self.ball.xVel = 3
                self.ball.yVel = 3
                secCount = 0
                
                self.ball.updatePos([x, y])
                
            elif a[3] >= b[3]:                  #1+ score for p1, upper collision with background
                x=320
                y=240
                self.score1+=1
                
                self.p1.velocity = 6
                self.p2.velocity = 6
                self.ball.xVel = 3
                self.ball.yVel = 3
                secCount = 0
                
                self.ball.updatePos([x,y])                
                return True
            
        else:
            if otherGameObject == self.p1:      #Error handling done here
                if a[0] in range(b[0], b[2]) and a[3] >= b[1]:
                    self.yState = False
                    self.xState = True
                    return True
                
            if a[2] in range(b[0], b[2]) and a[3] in range(b[1], b[3]): 
                self.yState = False
                return True
            if a[0] in range(b[0], b[2]) and a[1] in range(b[1], b[3]):
                self.yState = True
                return True
            if a[1] in range(b[1], b[3]) and a[0] in range(b[0], b[2]): #Exceptional case
                self.xState = True
                return True
            if a[3] in range(b[1], b[3]) and a[2] in range(b[0], b[2]): #Exceptional case
                self.xState = False
                return True
            
            else:
                return False

    #Corner detection for p1 and p2
    def CornerCollision(self, otherGameObject): 
        #Making bounding boxes around the game objects
        a = Game.canvas.bbox(self.ball.box)
        b = Game.canvas.bbox(otherGameObject.box)

        #Checking the collision for p1 separately
        if otherGameObject == self.p1:
            #Detecting collision under left most corner upto 1/4th of the paddle from left
            if a[2] in range(b[0], b[0] + 26) and a[3] >= b[1]:
                self.xState = False
                self.yState = False
                return True
            #Detecting collision under right most corner upto 3/4th of the paddle from left
            if a[0] in range(b[2] - 26, b[2]) and a[3] >= b[1]:
                self.xState = True
                self.yState = False
                return True
            #If no corner collision
            else:
                return False

        #Checking the collision for p2 separately
        elif otherGameObject == self.p2:
            #Detecting collision under left most corner upto 1/4th of the paddle from left
            if a[0] in range(b[0], b[0]+13) and a[1] <= b[3]:
                self.xState = False
                self.yState = True
                return True
            #Detecting collision under left most corner upto 3/4th of the paddle from left
            if a[0] in range(b[2]-13, b[2]) and a[1] <= b[3]:
                self.xState = True
                self.yState = True
                return True
            #If no corner collision
            else:
                return False

    #Exceptional case
    def Draw(self):
         raise
        
#-----------------------------------

class Background(GameObject):
    def __init__(self):
        super().__init__([320, 240])        
        self.back = PhotoImage(master = Game.canvas, file = 'assets\\bg.gif')
        
    def Draw(self):
        self.box = Game.canvas.create_image(self.position.x, self.position.y, image = self.back)

#-----------------------------------
    
class Ball(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.ball = PhotoImage(master = Game.canvas, file = 'assets\\ball.gif')
        self.xVel = 3
        self.yVel = 3

    def Draw(self):
        self.box = Game.canvas.create_image(self.position.x, self.position.y, image = self.ball)
        

    def updatePos(self, pos):
        super().__init__(pos)
    
#-----------------------------------

class Player(GameObject):
    def __init__(self, game, pos, vel, type = 'p1'):
        super().__init__(pos)
        self.type = type
        self.velocity = vel
        if self.type == 'p2':
            self.p = PhotoImage(master = Game.canvas, file = 'assets\\player2.gif')
        else:
            self.p = PhotoImage(master = Game.canvas, file = 'assets\\player1.gif')

    def Draw(self):
        
        self.box = Game.canvas.create_image(self.position.x, self.position.y, image = self.p)
    
#-----------------------------------

class Game:
    canvas = None
    def __init__(self, canvas):
        global x
        global y

        self.yState = True
        self.xState = True
        self.score1 = 0                #Score for player1
        self.score2 = 0                #Score for player2 or enemy
        
        Game.canvas = canvas           # Save canvas for future use
        x = 320
        y = 240
        
        self.back = Background()
        
        self.p1 = Player(self, [320, 450], 6)
        self.p2 = Player(self, [320, 30], 6, 'p2')
        self.ball = Ball([x, y])
        
        self.gameObjects = [self.back, self.p1, self.ball, self.p2]# A list of ALL game objects in the game

                
    def Draw(self):                    # This function draws ALL of the things
        
        global secCount
        
        Game.canvas.delete(ALL)        # First clear the screen 
        
        
        for obj in self.gameObjects:   # Now the objects draw THEMSELVES one by one
            obj.Draw()
            
        self.textScore1 = 'Score:'+str(self.score1)
        self.textScore2 = 'Score:'+str(self.score2)
        self.showScore1 = Game.canvas.create_text(590, 260, text = self.textScore2, fill = 'white', font = 'Times 15 bold')
        self.showScore2 = Game.canvas.create_text(590, 212, text = self.textScore1, fill = 'white', font = 'Times 15 bold')
        
        self.BounceBall()
        
    def LeftKeyPressed(self, player):  
        if player == 'paddle1':
            self.p1.position.x -= self.p1.velocity
    
        else:
            self.p2.position.x -= self.p2.velocity
            
            
    def RightKeyPressed(self, player):
        if player == 'paddle1':
            self.p1.position.x += self.p1.velocity
        else:
            self.p2.position.x += self.p2.velocity
        
    def Update(self):
        global secCount #It keeps record of the total elapsed time
                        #(not displayed anywhere on the game window)

        #Check ball collision with background
        if GameObject.isCollidingWith(self, self.back):
            self.BounceBall()

        #Check ball collision with Player 1
        if GameObject.isCollidingWith(self, self.p1):

            #Checks corner collision
            if GameObject.CornerCollision(self, self.p1):
                self.ball.xVel += 2
                self.ball.yVel -= 1
                self.VariableBallBounce()

            #No corner Collision
            else:
                #Checks if the ball velocities are the basic numbers
                #not 2 added to them
                if self.ball.xVel == (3 + secCount) + (2 * secCount):
                    self.ball.xVel -= 2
                    self.ball.yVel += 1
                self.BounceBall()

        #Check ball collision with Player 2
        if GameObject.isCollidingWith(self, self.p2):

            #Checks corner collision
            if GameObject.CornerCollision(self, self.p2):
                self.ball.xVel += 2
                self.ball.yVel -= 1
                self.VariableBallBounce()

            #No corner collision
            else:
                #Checks if the ball velocities are the basic numbers
                #not 2 added to them
                if self.ball.xVel == (3 + secCount) + (2 * secCount):
                    self.ball.xVel -= 2
                    self.ball.yVel += 1
                self.BounceBall()

    #Bounce the ball normally at 45 degree angle
    def BounceBall(self):
        global x, y

        #Ball moves towards bottom right corner
        if self.yState and self.xState:
            x += self.ball.xVel
            y += self.ball.yVel

        #Ball moves towards upper right corner
        if self.xState and not self.yState:
            x += self.ball.xVel
            y -= self.ball.yVel

        #Ball moves towards bottom left corner
        if not self.xState and self.yState:
            x -= self.ball.xVel
            y += self.ball.yVel

        #Ball moves towards upper left corner
        if not self.xState and not self.yState:
            x -= self.ball.xVel
            y -= self.ball.yVel

        self.ball.updatePos([x, y])

    #Bounce the ball at different angles other than 45
    def VariableBallBounce(self):
        global x, y

        #Ball moves towards bottom right corner
        if self.yState and self.xState:
            x += self.ball.xVel
            y += self.ball.yVel

        #Ball moves towards upper right corner
        if self.xState and not self.yState:
            x += self.ball.xVel
            y -= self.ball.yVel

        #Ball moves towards bottom left corner
        if not self.xState and self.yState:
            x -= self.ball.xVel
            y += self.ball.yVel

        #Ball moves towards upper left corner
        if not self.xState and not self.yState:
            x -= self.ball.xVel
            y -= self.ball.yVel

        self.ball.updatePos([x, y])

    #Checks if any one player has a score of 3 then ends the game
    def CheckWin(self):
        if self.score1 == 3 or self.score2 == 3:
            return True
        else:
            return False

#-----------------------------------


class GameWindow:
    def __init__(self):
        global secCount
        self.pressedKeys = set()
        self.root = Tk()
        self.root.title("Ping Pong")
        self.root.geometry('640x480')

        secCount = 0
        
        self.canvas = Canvas(self.root, width = 640, height = 480)
        self.canvas.grid(column=0, row=0)

        self.canvas.after(1, self.OneSecTimer)
        self.canvas.bind("<KeyPress>", self.KeyPressed)

        self.canvas.bind('<KeyRelease>', self.KeyRelease)
                
        self.canvas.focus_set()
        
        self.game = Game(self.canvas)
        self.root.after(1, self.GameLoop)
        
        self.root.mainloop()

    def KeyPressed(self, event):
        self.pressedKeys.add(event.keysym)
        if len(list(self.pressedKeys)) == 1:
            c = str(event.char)
            if c == 'a':
                self.game.LeftKeyPressed('enemy')
            if c == 'd':
                self.game.RightKeyPressed('enemy')
            if event.keysym == 'Right':
                self.game.RightKeyPressed('paddle1')
            if event.keysym == 'Left':
                self.game.LeftKeyPressed('paddle1')

        else:
            if 'a' in self.pressedKeys and 'Right' in self.pressedKeys:
                self.game.LeftKeyPressed('enemy')
                self.game.RightKeyPressed('paddle1')
            if 'a' in self.pressedKeys and 'Left' in self.pressedKeys:
                self.game.LeftKeyPressed('enemy')
                self.game.LeftKeyPressed('paddle1')
            if 'd' in self.pressedKeys and 'Left' in self.pressedKeys:
                self.game.RightKeyPressed('enemy')
                self.game.LeftKeyPressed('paddle1')
            if 'd' in self.pressedKeys and 'Right' in self.pressedKeys:
                self.game.RightKeyPressed('enemy')
                self.game.RightKeyPressed('paddle1')
            

    def KeyRelease(self, event):
        self.pressedKeys.remove(event.keysym)
    
    def GameLoop(self):
        self.game.Draw()
        self.game.Update()

        if self.game.CheckWin():
            self.ShowWinMessage()
            self.root.destroy()
        
        self.root.after(1000//30, self.GameLoop)        

    def OneSecTimer(self):
        global secCount
        secCount += 1
        if secCount < 15:
            if secCount % 5 == 0:
                self.game.ball.xVel += 1
                self.game.ball.yVel += 1

            if secCount % 10 == 0:
                self.game.p1.velocity += 1
                self.game.p2.velocity += 1
        
        self.canvas.after(1000, self.OneSecTimer)

    def ShowWinMessage(self):
        if self.game.score1 == 3:
            messagebox.showinfo('Congrats', 'Player 2 Wins!')

        else:
            messagebox.showinfo("Congrats", "Player 1 Wins!")
        
#-----------------------------------
