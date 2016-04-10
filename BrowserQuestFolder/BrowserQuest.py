#------------------------------------
from pygame import *
from math import *
from random import *
from pprint import *
#------------------------------------
flags=DOUBLEBUF|HWSURFACE#|FULLSCREEN
screen = display.set_mode((900,450),flags,32)
#------------------------------------
init()                                  
mixer.music.load("Sound\Music.mp3")      
#mixer.music.play(-1)#plays the song indefinitely

font.init()
#-----------------------------------
bandit=[
(transform.scale(image.load("Entities\Bandit/1.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/2.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/3.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/4.gif"),(30,30)).convert())]
    
sandtile=transform.smoothscale(image.load("Map\Sand.png"),(30,30)).convert()
greentile=transform.smoothscale(image.load("Map\grass.png"),(30,30)).convert()
#------------------------------------
spawnmap=[[0 for x in range(30)] for x in range(15)]
ospawnmap=spawnmap
sandmap=[[0 for x in range(30)] for x in range(15)]
osandmap=sandmap
#spawnmap[5][6]=1
#------------------------------------
running=True
spawn=True
curpos=300,300
move=False
movecounter=0
enter=True
breath=3
test=False
first=True
erase=True
sand=False
entitycounter=10
banditcounter=0
bcounter=0
#------------------------------------
def pathfinder(new,old,mapp):
    if new==old:
        return new
    #-----------------------------
    """
    curx,cury=old[1]//30,old[0]//30
    if 0>curx or curx>29 or cury<0 or cury>14:
        subtract=0
    else:
        subtract=1
    """
    #-----------------------------
    if old[0]!=new[0]:
        if new[0]>old[0]:# and mapp[curx-subtract][cury]==0:
            return(new[0]-30,new[1])
        if new[0]<old[0]:# and mapp[curx+subtract][cury]==0:
            return(new[0]+30,new[1])
    if old[1]!=new[1]:
        if new[1]>old[1]:# and mapp[curx][cury-subtract]==0:
            return(new[0],new[1]-30)
        if new[1]<old[1]:# and mapp[curx][cury+subtract]==0:
            return(new[0],new[1]+30)
    return new
#------------------------------------
def entity(mapp,number,clas):
    for i in range(number):
        place=randint(0,451)
        column=place//15-1
        row=place%15-1
        if clas=="bandit":
            mapp[row][column]=2
        elif clas=="goblin":
            mapp[row][column]=3
    return mapp
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
    if enter==True:
        spawnmap=entity(spawnmap,5,"bandit")
        enter=False
    if curpos[0]//30==29:
        sandmap=osandmap
        curpos=300,300
        enter=True
        spawn=False
        sand=True
    elif curpos[0]//30==0:
        spawnmap=ospawnmap
        curpos=300,300
        enter=True
        spawn=True
        sand=False
    #---------------------------------
    """
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30+1][curpos[0]//30]==2:
        test=True
    entitycounter+=1
    if test==True and entitycounter%10==0:
        entitycounter=0
        if first==True:
            entitypos=pathfinder(curpos,(curpos[0]+1,curpos[1]),spawnmap)
            first=False
        else:
            entitypos=pathfinder(curpos,entitypos,spawnmap)
        if erase==True:
            erase=False
            oldpos=curpos[1]//30+1,curpos[0]//30
        elif erase==False:
            erase=True
        spawnmap[oldpos[0]][oldpos[1]]=0
        spawnmap[entitypos[1]//30][entitypos[0]//30]=2
    #--------------------------------
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30-1][curpos[0]//30]==2:
        pass
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30][curpos[0]//30+1]==2:
        pass
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30][curpos[0]//30-1]==2:
        pass
    #-------------------------------
    """
    for l in range(0,30):
        for w in range(0,15):
            if sand==True:
                if spawnmap[w][l]==0:
                    screen.blit(sandtile,(l*30,w*30))
                if spawnmap[w][l]==2:
                    draw.rect(screen,(255,0,0),(l*30,w*30,30,30),0)
            if spawn==True:
                if spawnmap[w][l]==0 or spawnmap[w][l]==2:
                    screen.blit(greentile,(l*30,w*30))
                if spawnmap[w][l]==2:
                    """
                    #################
                    if breath==3:
                        breath=0
                    elif breath==0:
                        breath=3
                    ################
                    """
                    #draw.rect(screen,(255,0,0),(l*30,w*30,30,30),0)
                    if bcounter%200==0:
                        banditcounter+=1
                    bcounter+=1
                    if bcounter==800:
                        bcounter=0
                    if banditcounter==4:
                        banditcounter=0
                    screen.blit(bandit[banditcounter],(l*30,w*30))

    mappos=mx//30*30,my//30*30
    if mb[0]==1 and spawnmap[mappos[1]//30][mappos[0]//30]==0:
        draw.rect(screen,(255,0,0),(mappos[0],mappos[1],30,30),1)
        move=True
        omappos=mappos
    elif mb[0]==0:
        draw.rect(screen,(0,255,0),(mappos[0],mappos[1],30,30),1)
    draw.rect(screen,(0,0,255),(curpos[0],curpos[1],30,30),0)
    movecounter+=1
    if move==True and movecounter%7==0:
        movecounter=0
        if curpos==mappos:
            move=False
        curpos=pathfinder(curpos,omappos,spawnmap)
    
    display.flip()
quit()
