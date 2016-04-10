#30x14(plus 1 for utilities)
#------------------------------------
from pygame import *
from math import *
from random import *
#------------------------------------
flags=DOUBLEBUF|HWSURFACE#|FULLSCREEN
screen = display.set_mode((900,450),flags,32)
#------------------------------------
init()                                  
mixer.music.load("Sound\Music.mp3")      
#mixer.music.play(-1)#plays the song indefinitely

font.init()
#------------------------------------
greentile=transform.smoothscale(image.load("Map\grass.png"),(30,30)).convert()
#------------------------------------
spawnmap=[[0 for x in range(30)] for x in range(15)]
spawnmap[5][6]=1
#------------------------------------
running=True
spawn=True
curpos=0,0
move=False
movecounter=0
#------------------------------------
def pathfinder(new,old):
    if new==old:
        return curpos
    if old[0]!=new[0]:
        if new[0]>old[0]:
            return(new[0]-30,new[1])
        if new[0]<old[0]:
            return(new[0]+30,new[1])
    if old[1]!=new[1]:
        if new[1]>old[1]:
            return(new[0],new[1]-30)
        if new[1]<old[1]:
            return(new[0],new[1]+30)
#------------------------------------
while running:
    for e in  event.get():
        if e.type==QUIT:
            running=False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    if spawn==True:
        for l in range(0,30):
            for w in range(0,15):
                if spawnmap[w][l]==0:
                    screen.blit(greentile,(l*30,w*30))
    mappos=mx//30*30,my//30*30
    if mb[0]==1 and spawnmap[mappos[1]//30][mappos[0]//30]==0:
        draw.rect(screen,(255,0,0),(mappos[0],mappos[1],30,30),1)
        move=True
        omappos=mappos
    elif mb[0]==0:
        draw.rect(screen,(0,255,0),(mappos[0],mappos[1],30,30),1)
    draw.rect(screen,(0,0,255),(curpos[0],curpos[1],30,30),0)
    movecounter+=1
    if move==True and movecounter%5==0:
        movecounter=0
        if curpos==mappos:
            move=False
        curpos=pathfinder(curpos,omappos)
    display.flip()
quit()
