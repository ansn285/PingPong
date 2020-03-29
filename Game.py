import PingPong
import PingPong2
from tkinter import *

class MainMenu:
    def __init__(self):
        global a
        self.pressedKeys = set()
        self.root = Tk()
        self.root.title("Ping Pong - Main Menu")
        self.root.geometry('640x480')

        def showCanvas(attrib):
            global a
            if attrib == 'pvp':
                a = PingPong.GameWindow()
                
            else:
                a = PingPong2.GameWindow()

        self.canvas = Canvas(self.root, width = 640, height = 480)
        self.canvas.grid()

        self.button1 = Button(self.root, width = 15, height = 3, text = 'Player vs Player', command = lambda: showCanvas('pvp'))
        self.button1.grid()

        self.button2 = Button(self.root, width = 15, height = 3, text = 'Player vs Computer', command = lambda: showCanvas('pve'))
        self.button2.grid()

        self.button3 = Button(self.root, width = 15, height = 3, text = 'How to play', command = lambda: self.showHelp())
        self.button3.grid()

        self.button4 = Button(self.root, width = 15, height = 3, text = 'Quit', command = self.root.destroy)
        self.button4.grid()

        self.canvas.create_window(320, 120, window = self.button1)
        self.canvas.create_window(320, 190, window = self.button2)
        self.canvas.create_window(320, 260, window = self.button3)
        self.canvas.create_window(320, 330, window = self.button4)
        
        self.root.mainloop()

    def showHelp(self):
        root = Tk()
        root.geometry('410x180')
        root.title('How to Play')

        text = Text(root, font = 'Times 15', height = 7, width = 35, wrap = WORD)
        text.insert(INSERT, '1. Player 1 is the Blue paddle and Player 2 is the Green paddle. If you are playing with computer then Red is the bot'+
                            '\n\n2. Control P1 with left or right directional buttons and control P2 with A or D buttons')
    
        text.pack()

        button = Button(root, text = 'Close', command = root.destroy)
        button.pack()
        
m = MainMenu()
