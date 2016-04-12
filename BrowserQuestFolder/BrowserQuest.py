#------------------------------------
from pygame import *
from math import *
from random import *
from pprint import *
#------------------------------------
flags=DOUBLEBUF|HWSURFACE#|FULLSCREEN
screen = display.set_mode((900,500),flags,32)
#------------------------------------
init()                                  
mixer.music.load("Sound\Music.mp3")      
mixer.music.play(-1)#plays the song indefinitely

font.init()
#-----------------------------------
bandit=[
(transform.scale(image.load("Entities\Bandit/1.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/2.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/3.gif"),(30,30)).convert()),
(transform.scale(image.load("Entities\Bandit/4.gif"),(30,30)).convert())]

hero=[]
for i in range(1,17):
    hero.append(transform.scale(image.load("Hero/"+str(i)+".gif"),(90,75)).convert())

sandtile=transform.smoothscale(image.load("Map\Sand.png"),(30,30)).convert()
greentile=transform.smoothscale(image.load("Map\grass.png"),(30,30)).convert()
#------------------------------------
spawnmap=[[0 for x in range(30)] for x in range(15)]
sandmap=[[0 for x in range(30)] for x in range(15)]
villagemap=[[0 for x in range(30)] for x in range(15)]
#------------------------------------
land=[[0 for x in range(5)] for x in range(5)]
land[2][1]=villagemap
land[2][2]=spawnmap
currentland=2,2
land[2][3]=sandmap
#------------------------------------
curpos1=150,150
running=True
currentarea=spawnmap
curpos=300,300
move=False
movecounter=0
test=False
first=True
erase=True
sand=False
entitycounter=10
herocounter=0
hcounter=0
health=100
healthcounter=0
fight=False
stage="enter"
bcounter=0
banditcounter=0
player2=False
healthcounter1=0
health1=100
#------------------------------------
def pathfinder(new,old,mapp):
    if new==old:
        return new
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
    return new
#----------------------------
def search(x, y, grid):
    if grid[x][y] == 1:
        print("found",x,y)
        return(x*30,y*30)

    elif grid[x][y] == 2:
        print("wall",x,y)
        return False
    elif grid[x][y] == 3:
        print("visited",x,y)
        return False
    print("visiting",x,y)
    # mark as visited
    grid[x][y] = 3
    # explore neighbors clockwise starting by the one on the right
    if ((x < len(grid)-1 and search(x+1, y, grid))
        or (y > 0 and search(x, y-1, grid))
        or (x > 0 and search(x-1, y, grid))
        or (y < len(grid)-1 and search(x, y+1, grid))):
        return True
    return False
#------------------------------------
def entity(mapp,number,clas):
    for i in range(number):
        place=randint(0,451)
        column=place//15-1
        row=place%15-1
        if clas=="bandit" and mapp[row][column]==0:
            mapp[row][column]=2
        elif clas=="orc" and mapp[row][column]==0:
            mapp[row][column]=3
        elif clas=="villager" and mapp[row][column]==0:
            mapp[row][column]=1
    return mapp
#-----------------------------------
def drawmap(land,stage,clas):
    if stage=="enter":
        land=entity(land,5,clas)
    if land==spawnmap or land==villagemap:
        tile=greentile
    elif land==sandmap:
        tile=sandtile
    for l in range(0,30):
        for w in range(0,15):
            if land[w][l]>=0:#empty
                screen.blit(tile,(l*30,w*30))
            if land[w][l]==2:#bandit
                #------------------
                screen.blit(bandit[banditcounter],(l*30,w*30))#violates black box
                #-------------------
            if land[w][l]==1:#villager
                draw.rect(screen,(200,200,200),(l*30,w*30,30,30),0)
            if land[w][l]==3:#orc
                draw.rect(screen,(0,255,0),(l*30,w*30,30,30),0)
    land[curpos[1]//30][curpos[0]//30]=5
    #CHEESUS CRUST
    #print(land[curpos[1]//30][curpos[0]//30])
    land[curpos1[1]//30][curpos1[0]//30]=6
def transition(currentland,nextland,gridoflands):
    try:
        t=gridoflands[currentland[0]+nextland[0]]
    except IndexError:
        return currentland
    try:
        t=gridoflands[currentland[1]+nextland[1]]
    except IndexError:
        return currentland
    arriveat=gridoflands[currentland[0]+nextland[0]][currentland[1]+nextland[1]]
    arriveat=[[0 for x in range(30)] for x in range(15)]
    return arriveat
#------------------------------------
while running and health>0:
    for e in  event.get():
        if e.type==QUIT:
            running=False
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                running = False
        if e.type == KEYDOWN:
            player2=True
            omappos1=mappos
            if e.key == K_a:
                curpos1=curpos1[0]-30,curpos1[1]
            if e.key == K_w:
                curpos1=curpos1[0],curpos1[1]-30
            if e.key == K_d:
                curpos1=curpos1[0]+30,curpos1[1]
            if e.key == K_s:
                curpos1=curpos1[0],curpos1[1]+30
        else:
            player2=False
    mb = mouse.get_pressed()
    mx,my = mouse.get_pos()
    if curpos[0]//30==29:
        #currentarea=transition(currentland,(0,1),land)
        sandmap=[[0 for x in range(30)] for x in range(15)]
        curpos=300,300
        currentarea=sandmap
        stage="enter"
    elif curpos[0]//30==0:
        #currentarea=transition(currentland,(0,-1),land)
        spawnmap=[[0 for x in range(30)] for x in range(15)]
        curpos=300,300
        currentarea=spawnmap
        stage="enter"
    #---------------------------------
    if curpos[0]//30<29 and curpos[1]//30<14 and currentarea[curpos[1]//30+1][curpos[0]//30]>1:
        #print(currentarea[curpos[1]//30+1][curpos[0]//30])
        test=True
        healthcounter+=1
        if healthcounter%50==0:
            currentarea[curpos[1]//30+1][curpos[0]//30]=0
            fight=True
            healthcounter=0
            health-=10
            entitycounter+=1
    if test==True and entitycounter%5==0:
        entitycounter=0



    if curpos1[0]//30<29 and curpos1[1]//30<14 and currentarea[curpos1[1]//30+1][curpos1[0]//30]>1:
        print(health1)
        test=True
        healthcounter1+=1
        if healthcounter1%50==0:
            currentarea[curpos1[1]//30+1][curpos1[0]//30]=0
            fight=True
            healthcounter1=0
            health1-=10
            entitycounter+=1
    if test==True and entitycounter%5==0:
        entitycounter=0
        """
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
        """
    #--------------------------------
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30-1][curpos[0]//30]==2:
        pass
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30][curpos[0]//30+1]==2:
        pass
    if curpos[0]//30<29 and curpos[1]//30<14 and spawnmap[curpos[1]//30][curpos[0]//30-1]==2:
        pass
    #-------------------------------
    if currentarea==spawnmap:
        drawmap(spawnmap,stage,"bandit")
        if bcounter%200==0:
            banditcounter+=1
        bcounter+=1
        if bcounter==80:
            bcounter=0
        if banditcounter==4:
            banditcounter=0
        stage="explore"
    elif currentarea==sandmap:
        drawmap(sandmap,stage,"orc")
        stage="explore"
    #--------------------------------------
    draw.rect(screen,(0),(0,450,900,50),0)
    draw.rect(screen,(0,255,0),(0,450,max((900-(100-health)*9),0),50),0)
    #-------------------------------
    mappos=min(max(mx//30*30,0),870),min(max(my//30*30,0),420)
    if mb[0]==1 and currentarea[mappos[1]//30][mappos[0]//30]==0:
        draw.rect(screen,(255,0,0),(mappos[0],mappos[1],30,30),1)
        move=True
        omappos=mappos
    elif mb[0]==0:
        draw.rect(screen,(0,255,0),(mappos[0],mappos[1],30,30),1)
    #------------------
    if fight==True:
        hcounter+=1
    if hcounter%20==0 and hcounter>0:
        herocounter+=1
        hcounter=0
    if herocounter==16:
        herocounter=0
    #----------------
    screen.blit(hero[herocounter],(curpos[0]-30,curpos[1]-35))
    screen.blit(hero[herocounter],(curpos1[0]-30,curpos1[1]-35))
    movecounter+=1
    if move==True and movecounter%7==0:
        movecounter=0
        if curpos==mappos:
            move=False
        curpos=pathfinder(curpos,omappos,currentarea)
    
    #if player2==True and movecounter%7==0:
        #curpos1=pathfinder(curpos1,omappos1,currentarea)
        #curpos1=pathfinder(curpos1,omappos1,currentarea)
        """
        grid=spawnmap
        grid[omappos[1]//30][omappos[0]//30]=1
        curpos=search(curpos[0]//30,curpos[1]//30,grid)
        """
    #print(currentarea[curpos[1]//30+1][curpos[0]//30])
    display.flip()
quit()
