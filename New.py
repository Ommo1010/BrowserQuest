#paint.py
from pygame import *
from random import *
from math import *
from tkinter import *  
width = 1120
height = 840
screen = display.set_mode((width,height))
display.set_caption("Game")
##init()                                  
##mixer.music.load("OMFG - Hello.mp3")      
##mixer.music.play(-1)
##font.init()
##root = Tk()                                 
##root.withdraw()
def makeList(name,name2,start,end):
    directions = []
    for i in range(start,end+1):
        directions.append(image.load(name+"/"+name2+str(i)+".png"))
    return directions

class Boy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        s = Surface((1,1))
        self.mpics = []
        self.apics = []
        self.mpics.append(makeList("firefox","firefox",1,4))
        self.mpics.append(makeList("firefox","firefox",6,9))
        self.mpics.append(makeList("firefox","firefox",11,14))
        self.mpics.append(makeList("firefox","firefox",15,22))
        
        self.apics.append(makeList("firefox","firefoxattack",1,5))
        self.apics.append(makeList("firefox","firefoxattack",1,5))
        self.apics.append(makeList("firefox","firefoxattack",1,5))
        self.apics.append(makeList("firefox","firefoxattack",1,5))
        
        self.mframe = 0
        self.aframe = 0
        self.pressed = 0
        self.direction = 2
        self.attacking = 0
        
    def move(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] or keys[K_DOWN] or keys[K_UP] or keys[K_LEFT]:
            self.pressed = 1
            if keys[K_RIGHT]:
                self.x += 4
                self.mframe += 0.1
                if self.mframe >= 4:
                    self.mframe = 0
                self.direction = 0

            if keys[K_LEFT]:
                self.x -= 4
                self.mframe += 0.1
                if self.mframe >= 4:
                    self.mframe = 0
                self.direction = 1
                
            if keys[K_DOWN]:
                self.y += 4
                self.mframe += 0.1
                if self.mframe >= 4:
                    self.mframe = 0
                self.direction = 2
                
            if keys[K_UP]:
                self.y -= 4
                self.mframe += 0.1
                if self.mframe >= 8:
                    self.mframe = 0
                self.direction = 3
                
             
        else:
            self.mframe = 0
            self.pressed = 0

            
        if self.x > width-60:
            self.x = width-60
        if self.x < 0:
            self.x = 0
        if self.y > height-70:
            self.y = height-70
        if self.y < 0:
            self.y = 0
            
    def attack(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] == 0 and keys[K_DOWN] == 0 and keys[K_UP] == 0 and keys[K_LEFT] == 0:
            if keys[K_x]:
                self.attacking = 1
                self.aframe += 0.1
                if self.aframe >= 5:
                   self.aframe = 0
            else:
                self.attacking = 0
                self.aframe = 0
        

    def mdisplay(self, screen):
        if self.attacking == 0:
            screen.blit(self.mpics[self.direction][int(self.mframe)],(self.x,self.y))
    def adisplay(self, screen):
        if self.attacking == 1:
            print(self.aframe)
            screen.blit(self.apics[self.direction][int(self.aframe)],(self.x,self.y))
    

def game(screen):
    startRect = Rect(500,400,200,100)
    mx,my = 0,0
    myClock = time.Clock()
    board = []
    for i in range(12):
        board.append([0]*16)

        
            



    boy = Boy(width//2,height//2)
    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        #------------------------------------------
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        screen.fill((0))
        for y in range(12):
            for x in range(16):
                board[y][x] = Rect(x*70,y*70,69,69)
                draw.rect(screen,(255,255,255),board[y][x])
        boy.move()
        boy.mdisplay(screen)
        boy.attack()
        boy.adisplay(screen)
        #------------------------------------------
        myClock.tick(60) 
        display.flip()  
    quit()

game(screen)
