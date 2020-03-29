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
        global x, y, x2, y2, secCount   

        a = self.ball.bbox
        b = otherGameObject.bbox
        
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
                x2 = 320
                y2 = 50
                self.score2 += 1

                self.p1.velocity = 6
                self.p2.velocity = 6
                self.ball.xVel = 3
                self.ball.yVel = 3
                secCount = 0
                
                self.ball.updatePos([x, y])
                self.enemy.updatePos([x2, y2])
                
            elif a[3] >= b[3]:                  #1+ score for p1, upper collision with background
                x=320
                y=240
                x2 = 320
                y2 = 50
                
                self.score1+=1

                self.p1.velocity = 6
                self.p2.velocity = 6
                self.ball.xVel = 3
                self.ball.yVel = 3
                secCount = 0
                
                self.ball.updatePos([x,y])
                self.enemy.updatePos([x2, y2])
            
        else:
            if otherGameObject == self.enemy:
                if a[0] in range(b[0], b[2]) or a[2] in range(b[0], b[2]):
                    if a[1] <= b[3]:
                        self.yState = True
                        return True
                    
            if a[2] in range(b[0], b[2]) and a[3] in range(b[1], b[3]):
                self.yState = False
                return True
            elif a[0] in range(b[0], b[2]) and a[1] in range(b[1], b[3]):
                self.yState = True
                return True
            elif a[1] in range(b[1], b[3]) and a[0] in range(b[0], b[2]):
                self.xState = True
                return True
            elif a[3] in range(b[1], b[3]) and a[2] in range(b[0], b[2]):
                self.xState = False
                return True
            else:
                return False
            
    #Corner detection for p1
    def CornerCollision(self):
        a = self.ball.bbox
        b = self.p1.bbox

        #Detecting collision under left most corner upto 1/4th of the paddle
        if a[2] in range(b[0], b[0] + 26) and a[3] >= b[1]:
            self.xState = False
            self.yState = False
            return True

        #Detecting collision under left most corner upto 3/4th of the paddle
        if a[0] in range(b[2] - 26, b[2]) and a[3] >= b[1]:
            self.xState = True
            self.yState = False
            return True

        #If no corner collision
        else:
            return False

    def OutRange(self):         #Returns true if ball gets out of range of
                                #the bot paddle
        a = Game.canvas.bbox(self.enemy.box)
        b = Game.canvas.bbox(self.ball.box)

        #If ball gets out of left boundary of bot
        if b[0] <= a[0]:
            self.negState = True
            self.posState = False
            return True

        #If ball gets out of right boundary of bot
        elif b[2] >= a[2]:
            self.posState = True
            self.negState = False
            return True

        #Within the boundaries
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
        self.bbox = Game.canvas.bbox(self.box)

#-----------------------------------
    
class Ball(GameObject):
    def __init__(self, pos):
        super().__init__(pos)
        self.ball = PhotoImage(master = Game.canvas, file = 'assets\\ball.gif')
        self.xVel = 3
        self.yVel = 3

    def Draw(self):
        self.box = Game.canvas.create_image(self.position.x, self.position.y, image = self.ball)
        self.bbox = Game.canvas.bbox(self.box)

    def updatePos(self, pos):
        super().__init__(pos)
    
#-----------------------------------

class Player(GameObject):
    def __init__(self, game, pos, vel, type = 'p1'):
        super().__init__(pos)
        self.type = type
        self.velocity = vel
        if self.type == 'e':
            self.p = PhotoImage(master = Game.canvas, file = 'assets\\enemy.gif')
        else:
            self.p = PhotoImage(master = Game.canvas, file = 'assets\\player1.gif')

    def Draw(self):
        self.box = Game.canvas.create_image(self.position.x, self.position.y, image = self.p)
        self.bbox = Game.canvas.bbox(self.box)        

    def updatePos(self, pos):   #Updating the position of the Bot paddle
        
        super().__init__(pos)
        self.bbox = Game.canvas.bbox(self.box)
    
#-----------------------------------

class Game:
    canvas = None
    def __init__(self, canvas):
        global x, y, x2, y2

        self.yState = True
        self.xState = True
        self.score1 = 0                #Score for player1
        self.score2 = 0                #Score for player2 or enemy
        
        Game.canvas = canvas           # Save canvas for future use
        x = 320
        y = 240
        x2 = 320
        y2 = 30
        
        self.back = Background()
        
        self.p1 = Player(self, [320, 450], 6)
        self.enemy = Player(self, [x2, y2], 7, 'e')
        self.ball = Ball([x, y])
        
        self.gameObjects = [self.back, self.p1, self.ball, self.enemy]# A list of ALL game objects in the game

                
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
        
    def LeftKeyPressed(self):  
        self.p1.position.x -= self.p1.velocity            
            
    def RightKeyPressed(self):
        self.p1.position.x += self.p1.velocity
        
    def Update(self):
        global secCount #It keeps record of the total elapsed time
                        #(not displayed anywhere on the game window)

        #Check ball collision with background
        if GameObject.isCollidingWith(self, self.back):
            self.BounceBall()

        #Check ball collision with Player
        if GameObject.isCollidingWith(self, self.p1):

            #Checks corner collision
            if GameObject.CornerCollision(self):
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

        #Check ball collision with bot
        if GameObject.isCollidingWith(self, self.enemy):
            #Checks if the ball velocities are the basic numbers
            #not 2 added to them
            if self.ball.xVel == (3 + secCount) + (2 * secCount):
                self.ball.xVel -= 3
                self.ball.yVel += 1
            self.BounceBall()        

        #If ball goes out of range of the bot, move bot
        if GameObject.OutRange(self):
            self.MoveEnemy()

        
    #Moves the bot paddle if ball is out of its bounds
    def MoveEnemy(self):
        global x2, y2 #paddle's x, y axes

        #Ball is on the left side of the paddle
        if self.negState:
            x2 -= self.enemy.velocity

        #Ball is on the right side of the paddle
        else:
            x2 += self.enemy.velocity
            
        self.enemy.updatePos([x2, y2])

    #Checks if any one player has a score of 3 then ends the game
    def CheckWin(self):
        if self.score1 == 3 or self.score2 == 3:
            return True
        else:
            return False

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

        #Moves the ball towards the upper left corner
        if not self.xState and not self.yState:
            x -= self.ball.xVel
            y -= self.ball.yVel

        self.ball.updatePos([x, y])

#-----------------------------------


class GameWindow:
    def __init__(self):
        global secCount
        self.root = Tk()
        self.root.title("Ping Pong")
        self.root.geometry('640x480')

        secCount = 0

        self.canvas = Canvas(self.root, width = 640, height = 480)
        self.canvas.grid(column=0, row=0)

        self.canvas.after(1, self.OneSecTimer)
        self.canvas.bind("<KeyPress>", self.KeyPressed)
        
        self.canvas.focus_set()
        

        self.game = Game(self.canvas)
        self.root.after(1000//30, self.GameLoop)

        
        self.root.mainloop()
    
    def KeyPressed(self, event):
        c = str(event.char)
        if event.keysym == 'Right':
            self.game.RightKeyPressed()
        if event.keysym == 'Left':
            self.game.LeftKeyPressed()            
    
    def GameLoop(self):
        self.game.Draw()
        self.game.Update()

        if self.game.CheckWin():
            if self.game.score2 == 3:
                self.ShowWinMessage()
                self.root.destroy()
            else:
                self.ShowLoseMessage()
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
                self.game.enemy.velocity += 1
            
        self.canvas.after(1000, self.OneSecTimer)

    def ShowWinMessage(self):
        messagebox.showinfo('Congrats', 'You Win!')
        
    def ShowLoseMessage(self):
        messagebox.showinfo('Hard luck', 'You lose!')
        
#-----------------------------------
