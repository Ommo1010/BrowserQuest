#PSEUDOCODE to check what weapon/armour we have
from random import *

class Item:
    def __init__(self, x ,y, itemname):
        self.x = x
        self.y = y
        #itemname = choice(list of items)
        self.itemname = itemname
        self.types = ""
        
def checkitem(itemx, itemy, boyx, boyy):
    if itemx == boyx and itemy == boyy:
        return True
    return False

enemy = "dead"
boyx = 0   #change to boy.x in real program
boyy = 0
itemonmap = False
#dropping items

if enemy == "dead":
    chance = randint(0,4)
    if chance == 0:
        item = Item(0,0,"armour")
        itemonmap = True
if itemonmap:
    if checkitem(item.x, item.y, boyx, boyy):
        boy.type = item.itemname

#achievement would be similar
#if player is on this spot, achievement get


def checkachievements(mapx,mapy,x,y,screenx,screeny,boyx,boyy):
    #screenx and screeny is current screen coords
    if mapx == screenx and mapy == screeny and x == boyx and y == boyy:
        return True
    return False

class Achievements:
    def __init__(self,mapx, mapy, x ,y, name):
        self.mapx = mapx
        self.mapy = mapy
        self.x = x
        self.y = y
        self.name = name

ach1 = Achievements(-1900,-9120,12,12,"cake")
achievementlist = []
achievementlist.append(achievement1)
for i in range achievmentlist:
    if checkachievements(ach1.mapx,ach1.mapy,ach1.x,ach1.y,screenx,screeny,boyx,boyy):
        print("Achievement",ach1.name,"get!")
        




    
