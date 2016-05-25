#paint.py
from pygame import *
from random import *
from math import *
from tkinter import *  
width = 1260
height = 980
screen = display.set_mode((width,height))
display.set_caption("Game")
##init()                                  
##mixer.music.load("OMFG - Hello.mp3")      
##mixer.music.play(-1)
##font.init()
##root = Tk()                                 
##root.withdraw()
gridScale = 70

gamemap = image.load("gamemap.png")
def makeList(name,name2,start,end):
    directions = []
    for i in range(start,end+1):
        directions.append(image.load(name+"/"+name2+str(i)+".png"))
    return directions
def grid(board,screen):
    for y in range(14):
        for x in range(18):
            board[y][x] = Rect(x*gridScale,y*gridScale,gridScale-1,gridScale-1)
            draw.rect(screen,(255,255,255),board[y][x])
def border(x,y):
    if x > 17:
        x = 17
    if x < 0:
        x = 0
    if y > 13:
        y = 13
    if y < 0:
        y = 0

    return x,y

def collide(xb,yb,xm,ym):
    if xb == xm and yb == ym:
        return True
    return False

def collideTrue(movex,movey,stillx,stilly,oldmovex,oldmovey):
    if collide(movex,movey,stillx,stilly) == True:
        movex = oldmovex
        movey = oldmovey
    return movex,movey

def checkcollide(movex,movey,blocklist,oldmovex,oldmovey):
    for i in range(0,len(blocklist),2):
        newmovex,newmovey = collideTrue(movex,movey,blocklist[i],blocklist[i+1],oldmovex,oldmovey)
        if newmovex != movex or newmovey != movey:
            return newmovex,newmovey
    return movex,movey

class Boy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.mpics = []
        self.apics = []
        self.mpics.append(makeList("firefoxr","firefoxr",0,3))
        self.mpics.append(makeList("firefoxl","firefoxl",0,3))
        self.mpics.append(makeList("firefoxd","firefoxd",0,3))
        self.mpics.append(makeList("firefoxu","firefoxu",0,7))
        
        self.apics.append(makeList("firefoxattackr","firefoxattackr",0,4))
        self.apics.append(makeList("firefoxattackl","firefoxattackl",0,4))
        self.apics.append(makeList("firefoxattackd","firefoxattackd",0,4))
        self.apics.append(makeList("firefoxattacku","firefoxattacku",0,4))
        
        self.mframe = 0
        self.aframe = 0
        self.framespeed = 0.5
        self.pressed = 0
        self.wait = 70
        self.direction = 2
        self.attacking = 0
        self.oldx = self.x
        self.oldy = self.y
        self.moveunitsx = 15
        self.moveunitsy = 0
        
    def move(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] or keys[K_DOWN] or keys[K_UP] or keys[K_LEFT]:
            self.oldx = self.x
            self.oldy = self.y
            self.pressed = 1
            if keys[K_RIGHT]:
                self.x += 1
                self.moveunitsx = 0
                self.moveunitsy = -3
                self.mframe += self.framespeed
                if self.mframe >= 3:
                    self.mframe = 0
                self.direction = 0

            if keys[K_LEFT]:
                self.x -= 1
                self.moveunitsx = 10
                self.moveunitsy = -3
                self.mframe += self.framespeed
                if self.mframe >= 4:
                    self.mframe = 0
                self.direction = 1
                
            if keys[K_DOWN]:
                self.y += 1
                self.moveunitsx = 15
                self.moveunitsy = 0
                self.mframe += self.framespeed
                if self.mframe >= 4:
                    self.mframe = 0
                self.direction = 2
                
            if keys[K_UP]:
                self.y -= 1
                self.moveunitsx = 15
                self.moveunitsy = -3
                self.mframe += self.framespeed
                if self.mframe >= 8:
                    self.mframe = 0
                self.direction = 3

##            while int(self.x%70) != 0:
##                self.x += 0.1
##                self.mframe += 0.1
##                if self.mframe >= 4:
##                    self.mframe = 0
##                self.direction = 0
             
        else:
            self.mframe = 0
            self.pressed = 0

        self.x,self.y = border(self.x,self.y)

    def attack(self):
        keys = key.get_pressed()
        if keys[K_RIGHT] == 0 and keys[K_DOWN] == 0 and keys[K_UP] == 0 and keys[K_LEFT] == 0:
            if keys[K_x]:
                self.attacking = 1
                self.aframe += 0.5
                if self.aframe >= 5:
                   self.aframe = 0
            else:
                self.attacking = 0
                self.aframe = 0
        else:
            self.attacking = 0
            self.aframe = 0
        

    def display(self, screen):
        if self.attacking == 0:
            screen.blit(self.mpics[self.direction][int(self.mframe)],(self.x*gridScale + self.moveunitsx,self.y*gridScale + self.moveunitsy))
        elif self.attacking == 1:
            screen.blit(self.apics[self.direction][int(self.aframe)],(self.x*gridScale + self.moveunitsx,self.y*gridScale + self.moveunitsy))

class Enemy:
    def __init__(self, x, y, health, attack):
        self.x = x
        self.y = y
        self.health = health
        self.attack = attack
        self.pics = []
        self.pics.append(makeList("batr","batr",0,4))
        self.pics.append(makeList("batl","batl",0,4))
        self.pics.append(makeList("batd","batd",0,4))
        self.pics.append(makeList("batu","batu",0,4))

        self.frame = 0
        self.framespeed = 0.33
        self.wait = 70
        self.direction = 0
        self.oldx = self.x
        self.oldy = self.y
        self.attacking = 10
        self.moving = 10

        self.moveunitsx = 0
        self.moveunitsy = 0
    def still(self):
        if self.moving == 0:
            self.frame += self.framespeed
            if self.frame >= 4:
                self.frame = 1
    def move(self):
        self.moving = 1
        ran = randint(0,8)
        randirect = randint(0,4)
        self.oldx = self.x
        self.oldy = self.y
        if ran == 0:
            if randirect == 0:
                self.x += 1
                self.direction = 0
                self.moveunitsx = 10
                self.moveunitsy = -10
            if randirect == 1:
                self.x -= 1
                self.direction = 1
                self.moveunitsx = 10
                self.moveunitsy = -10
            if randirect == 2:
                self.y += 1
                self.direction = 2
                self.moveunitsx = -10
                self.moveunitsy = 0
            if randirect == 3:
                self.y -= 1
                self.direction = 3
                self.moveunitsx = -10
                self.moveunitsy = 5
                self.frame += self.framespeed
                if self.frame >= 4:
                    self.frame = 0
        else:
            self.moving = 0
        self.x,self.y = border(self.x,self.y)
        
        
    def attack(self):
        if self.attacking == 1:
            None
            
    
    def display(self, screen):

        screen.blit(self.pics[self.direction][int(self.frame)],(self.x*gridScale + self.moveunitsx,self.y*gridScale + self.moveunitsy))

def game(screen):
    mx,my = 0,0
    myClock = time.Clock()
    board = []
    board2 = []
    for i in range(14):
        board.append([0]*18)
        board2.append([0]*16)
        
            
    
    
    boy = Boy(0,0)
    bat = Enemy(2,2,5,5)

    
    
    running = True
    while running:
        for e in event.get():
            if e.type == QUIT:
                running = False
        #------------------------------------------
        eblocklist = []
        blockx = 1
        blocky = 1

        eblocklist.append(blockx)
        eblocklist.append(blocky)
        eblocklist.append(bat.x)
        eblocklist.append(bat.y)

        pblocklist = []
        pblocklist.append(blockx)
        pblocklist.append(blocky)
        pblocklist.append(boy.x)
        pblocklist.append(boy.y)

        
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        
        

        #grid(board,screen)
        screen.blit(gamemap,(0,0))
        boy.move()
        boy.x,boy.y = checkcollide(boy.x,boy.y,eblocklist,boy.oldx,boy.oldy)
        boy.attack()
        boy.display(screen)

        bat.still()
        bat.move()
        bat.x,bat.y = checkcollide(bat.x,bat.y,pblocklist,bat.oldx,bat.oldy)
        bat.display(screen)
        #------------------------------------------
        myClock.tick(30)
        myClock.tick(30)
        display.flip()  
    quit()

game(screen)
