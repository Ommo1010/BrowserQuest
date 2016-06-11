#paint.py
from pygame import *
from random import *
from math import *
from tkinter import *
gridScale = 38

width = gridScale*25
height = gridScale*20
screen = display.set_mode((width,height))
display.set_caption("Game")
##init()                                  
##mixer.music.load("OMFG - Hello.mp3")      
##mixer.music.play(-1)
##font.init()
##root = Tk()                                 
##root.withdraw()

gamemapraw = image.load("gamemapnew.png")
gamemaph = gamemapraw.get_height()
gamemapw = gamemapraw.get_width()
gamemap = transform.smoothscale(gamemapraw,(int(gamemapw*1),int(gamemaph*1)))
maplist = []
for i in range(13):
    maplist.append([0]*3)

def makeList(name,name2,start,end):
    directions = []
    for i in range(start,end+1):
        directions.append(image.load(name+"/"+name2+str(i)+".png"))
    return directions
def grid(board,screen):
    for y in range(24):
        for x in range(32):
            board[y][x] = Rect(x*gridScale,y*gridScale,gridScale-1,gridScale-1)
            draw.rect(screen,(255,255,255),board[y][x],2)
def border(x,y,screenx,screeny):
    if screenx == 0:
        if x < 0:
            x = 0
    else:
        if x < 0:
            x = 24
            screenx += width
            
    if screenx == -1900:
        if x > 24:
            x = 24
    else:
        if x > 24:
            x = 0
            screenx-= width
            
    if screeny == 0:
        if y < 0:
            y = 0
    else:
        if y < 0:
            y = 19
            screeny += height
            
    if screeny == -9120:
        if y > 19:
            y = 19
    else:
        if y > 19:
            y = 0
            screeny -= height
            
    screenx,screeny = screenborder(screenx,screeny)
    return x,y,screenx,screeny

def screenborder(x,y):
    if x > 0:
        x = 0
    if x < -1900:
        x = -1900
    if y > 0:
        y = 0
    if y < -9120:
        y = -9120
    return x,y

def borderenemy(x,y):
    if x > 31:
        x = 31
    if x < 0:
        x = 0
    if y > 23:
        y = 23
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
        self.maximg = 0
        self.type = "clotharmour"
        self.armour = 0   #Start at zero and increase it by multiples of 4 (4 directions) for new armour.

        self.mpics = []
        self.apics = []
        self.mpics.append(makeList("firefoxr","firefoxr",0,3))
        self.mpics.append(makeList("firefoxl","firefoxl",0,3))
        self.mpics.append(makeList("firefoxd","firefoxd",0,3))
        self.mpics.append(makeList("firefoxu","firefoxu",0,7))
        #just do this for every armour, number at the end is 0, and then number of pics-1
##        self.mpics.append(makeList("clotharmourr","clotharmourr",0,3))
##        self.mpics.append(makeList("clotharmourl","clotharmourl",0,3))
##        self.mpics.append(makeList("clotharmourd","clotharmourd",0,3))
##        self.mpics.append(makeList("clotharmouru","clotharmouru",0,7))
        
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
        self.attackblock = (self.x,self.y)
        self.health = 10
        self.healthbar = Rect(self.x-10,self.y-20,20,10)
        
    def move(self):
        #Example of what armour we wearing
        #if self.type == "clotharmour":
            #self.armour = 4 -- if clotharmour was appended after firefox.
        if self.type == "firefox":
            self.armour = 0    #if firefox is appended first atm.
            self.maximg = [4,4,4,8]   #you can use list for moveunits like self.maximg if you want, just a bit of work
            self.moveunitsxr = -15
            self.moveunitsyr = -38
            self.moveunitsxl = 0
            self.moveunitsyl = -38
            self.moveunitsxd = 0
            self.moveunitsyd = -38
            self.moveunitsxu = -3
            self.moveunitsyu = -38

        
        keys = key.get_pressed()
        if keys[K_RIGHT] or keys[K_DOWN] or keys[K_UP] or keys[K_LEFT]:
            self.oldx = self.x
            self.oldy = self.y
            self.pressed = 1
            if keys[K_RIGHT]:
                self.x += 1
                self.mframe += self.framespeed
                if self.mframe >= self.maximg[0]:
                    self.mframe = 0
                self.direction = 0

            if keys[K_LEFT]:
                self.x -= 1
                self.mframe += self.framespeed
                if self.mframe >= self.maximg[1]:
                    self.mframe = 0
                self.direction = 1
                
            if keys[K_DOWN]:
                self.y += 1
                self.mframe += self.framespeed
                if self.mframe >= self.maximg[2]:
                    self.mframe = 0
                self.direction = 2
                
            if keys[K_UP]:
                self.y -= 1
                self.mframe += self.framespeed
                if self.mframe >= self.maximg[3]:
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

       

    def attack(self):
        keys = key.get_pressed()
        directions = [1,-1,1,-1]
        if keys[K_RIGHT] == 0 and keys[K_DOWN] == 0 and keys[K_UP] == 0 and keys[K_LEFT] == 0:
            if keys[K_x]:
                self.attacking = 1
                self.aframe += 0.5
                if self.aframe >= 5:
                   self.aframe = 0

                attackdirection = directions[self.direction]
                if self.direction in [1,2]:
                    self.attackblock = (self.x+attackdirection,self.y)
                    
            else:
                self.attacking = 0
                self.aframe = 0
        else:
            self.attacking = 0
            self.aframe = 0
        

    def display(self, screen):
        if self.direction == 0:
            screen.blit(self.pics[self.direction+self.armour][int(self.mframe)],(self.x*gridScale + self.moveunitsxr,self.y*gridScale + self.moveunitsyr))
        if self.direction == 1:
            screen.blit(self.pics[self.direction+self.armour][int(self.mframe)],(self.x*gridScale + self.moveunitsxl,self.y*gridScale + self.moveunitsyl))
        if self.direction == 2:
            screen.blit(self.pics[self.direction+self.armour][int(self.mframe)],(self.x*gridScale + self.moveunitsxd,self.y*gridScale + self.moveunitsyd))
        if self.direction == 3:
            screen.blit(self.pics[self.direction+self.armour][int(self.mframe)],(self.x*gridScale + self.moveunitsxu,self.y*gridScale + self.moveunitsyu))

        elif self.attacking == 1:
            screen.blit(self.apics[self.direction+self.armour][int(self.aframe)],(self.x*gridScale + self.moveunitsx,self.y*gridScale + self.moveunitsy))
        draw.rect(screen,(0,255,0),self.healthbar)
class Enemy:
    def __init__(self, species, x, y, health, attack):
        self.x = x
        self.y = y
        self.type = species
        self.health = health
        self.attack = attack
        self.pics = []
        self.maximg = 0
        if self.type == "bat":
            self.pics.append(makeList("batr","batr",0,4))
            self.pics.append(makeList("batl","batl",0,4))
            self.pics.append(makeList("batd","batd",0,4))
            self.pics.append(makeList("batu","batu",0,4))
            self.maximg = 4
            self.moveunitsxr = 0
            self.moveunitsyr = -35
            self.moveunitsxl = 0
            self.moveunitsyl = -35
            self.moveunitsxd = -25
            self.moveunitsyd = -15
            self.moveunitsxu = -25
            self.moveunitsyu = -15
        elif self.type == "snake":
            self.pics.append(makeList("snaker","snaker",0,3))
            self.pics.append(makeList("snakel","snakel",0,3))
            self.pics.append(makeList("snaked","snaked",0,3))
            self.pics.append(makeList("snakeu","snakeu",0,3))
            self.maximg = 3
            self.moveunitsxr = 0
            self.moveunitsyr = -50
            self.moveunitsxl = 0
            self.moveunitsyl = -50
            self.moveunitsxd = -0
            self.moveunitsyd = -50
            self.moveunitsxu = -0
            self.moveunitsyu = -10
        self.frame = 0
        self.framespeed = 0.33
        self.wait = 70
        self.direction = 0
        self.oldx = self.x
        self.oldy = self.y
        self.attacking = 10
        self.moving = 10
        
        

    def still(self):
        if self.moving == 0:
            self.frame += self.framespeed
            if self.frame >= self.maximg:
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
                
                
            if randirect == 1:
                self.x -= 1
                self.direction = 1
                
            if randirect == 2:
                self.y += 1
                self.direction = 2
                
            if randirect == 3:
                self.y -= 1
                self.direction = 3

        else:
            self.moving = 0
        self.x,self.y = borderenemy(self.x,self.y)
        
        
    def attack(self):
        if self.attacking == 1:
            None
            
    
    def display(self, screen):
        if self.direction == 0:
            screen.blit(self.pics[self.direction][int(self.frame)],(self.x*gridScale + self.moveunitsxr,self.y*gridScale + self.moveunitsyr))
        if self.direction == 1:
            screen.blit(self.pics[self.direction][int(self.frame)],(self.x*gridScale + self.moveunitsxl,self.y*gridScale + self.moveunitsyl))
        if self.direction == 2:
            screen.blit(self.pics[self.direction][int(self.frame)],(self.x*gridScale + self.moveunitsxd,self.y*gridScale + self.moveunitsyd))
        if self.direction == 3:
            screen.blit(self.pics[self.direction][int(self.frame)],(self.x*gridScale + self.moveunitsxu,self.y*gridScale + self.moveunitsyu))

def menu():
    mx,my = 0,0
    vals = ["game"]
    running = True
    page = "menu"
    background = image.load("background.png")
    screen.blit(background,(0,0))
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        

##        buttons = [Rect(200,y*60+200,100,40) for y in range(4)]
##        draw.rect(screen,(255,255,255),buttons[0])
##
##        if buttons[0].collidepoint(mx,my):
##            mode = "game"
        while page != "exit":
            if page == "game":
                game()
            if page == "menu":
                menu()
def game():
    mx,my = 0,0
    screenposx = 0
    screenposy = -180*gridScale
    
    myClock = time.Clock()
    board = []
    for i in range(24):
        board.append([0]*(32))
        
            
    
    
    boy = Boy(0,0)
    bat1 = Enemy("bat",2,2,5,5)
    bat2 = Enemy("bat",9,9,5,5)
    snake2 = Enemy("snake",9,9,5,5)
    enmylist = []
    enmylist.append(bat1)
    enmylist.append(bat2)
    enmylist.append(snake2)
    
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
        for enmy in enmylist:
            eblocklist.append(enmy.x)
            eblocklist.append(enmy.y)

        pblocklist = []
        pblocklist.append(blockx)
        pblocklist.append(blocky)
        pblocklist.append(boy.x)
        pblocklist.append(boy.y)

        
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()
        
        
        ##maplist[screenposy/height][screenposx/width]
        

        screen.blit(gamemap,(screenposx,screenposy))
        boy.move()
        boy.x,boy.y,screenposx,screenposy = border(boy.x,boy.y,screenposx,screenposy)
        boy.x,boy.y = checkcollide(boy.x,boy.y,eblocklist,boy.oldx,boy.oldy)
        #boy.x,boy.y = checkcollide(boy.x,boy.y,mapblock,boy.oldx,boy.oldy)
        boy.attack()
        boy.display(screen)

        grid(board,screen)     #DRAWS THE GRID. IMPORTANT FOR MOVEUNITS
        
        if boy.attacking == 1:
            if boy.attackblock == (bat.x,bat.y):
                bat.health -= 1
        #if bat.health == 0:
            #bat = None
        for enmy in enmylist:
            enmy.still()
            enmy.move()
            enmy.x,enmy.y = checkcollide(enmy.x,enmy.y,pblocklist,enmy.oldx,enmy.oldy)
            enmy.display(screen)
        #------------------------------------------
        myClock.tick(30)
        myClock.tick(30)
        display.flip()  
    quit()

game()
