import pgzrun
import random
##Initialize
WIDTH,HEIGHT = 768,432
OUT = (-100,0)
TIME = 0
runrset,idlerset = [],[] #List of actions' frames
bg1,bg2= [],[] #Background
killTrap = []
floor = []
door = []
spdx = 3 #Speed of moves

#Merge Lists
bg = bg1 + bg2

#======================IMPORT IMAGE======================
#Character
for i in range(8):
    runrset.append('player\\run\\runr\\right'+str(i))
for i in range(12):
    idlerset.append('player\\idle\\idler\\idler'+str(i))

#======================SETUP CHARACTER======================
PLAYER = Actor('player\\idle\idler\idler0')

#======================INITIALIZE VARIABLES======================
def initializeVariable():
    global PLAYER,bg1,bg2,floor,door
    bg1,bg2 = [],[]
    floor,door = [],[]
    #Background
    for i in range(5):
        bg1.append(Actor("background\\plx-" + str(i+1)))
        bg2.append(Actor("background\\plx-" + str(i+1)))
    for i in range(25):
        floor.append(Actor("tileset\\ground"))
    door.append(Actor("door"))
    #Player
    PLAYER.jumph = 0
    PLAYER.frame = 0
    PLAYER.state = 'FALL'

def mergeList():
    global bg,floor
    bg = bg1 + bg2
    floor = floor+door

#======================SETUP MAP======================
def initializeMap():
    #Player
    PLAYER.bottomleft = WIDTH/2,HEIGHT - floor[0].height
    #Background
    for i in range(5):
        bg1[i].topright = WIDTH*0.5,0
        bg2[i].topleft = WIDTH*0.5,0
    for i in range(25):
        floor[i].bottomleft = i*(floor[i].width - 2),HEIGHT
    for i in range(4,25,3):
        floor[i].bottomleft = OUT
    door[0].bottomright = 25*(floor[0].width -2),HEIGHT-floor[0].height

#======================RESTART STAGE======================
def restartStage():
    initializeVariable()
    mergeList()
    initializeMap()

#======================ACTOR MOVEMENT======================
#Infinite Moves
def moveLeft(act,mode=0): ##Mode 0: Infinite Move; Mode 1: Bordered Move
    if(mode == 1 and act.left <= 0):
        return
    act.left -= spdx
    if(mode == 0 and act.right < 0):
        act.left = WIDTH-spdx

def moveRight(act,mode=0):
    if(mode == 1 and act.right >= WIDTH):
        return
    act.left += spdx
    if(mode == 0 and act.left > WIDTH):
        act.right = spdx

#======================MOVE IN GROUP======================
#Screen
def screenLeft():
    for i in bg:
        moveLeft(i)
    for i in floor:
        i.left -= spdx

def screenRight():
    for i in bg:
        moveRight(i)
    for i in floor:
        i.left += spdx

#======================Interaction======================
#COLLISION
def collideFloor(act=PLAYER):
    for i in floor:
        if(act.colliderect(i) and i.top-4*spdx<= act.bottom <= i.top+4*spdx and PLAYER.left >= i.left-8*spdx and PLAYER.right <= i.right + 8*spdx):
            return True
    return False

def collideLeft():
    for i in floor:
        if(PLAYER.colliderect(i) and i.bottom-4*spdx <= PLAYER.bottom <= i.bottom+4*spdx and i.right-4*spdx <= PLAYER.left <= i.right+4*spdx):
            return True
    return False

def collideRight():
    for i in floor:
        if(PLAYER.colliderect(i) and i.bottom-4*spdx <= PLAYER.bottom <= i.bottom+4*spdx and i.left-4*spdx <= PLAYER.right <= i.left+4*spdx):
            return True
    return False

#======================VICTORY AND DEFEAT======================
def playerLose():
    global PLAYER
    PLAYER.status = 'DEAD'
    for i in killTrap:
        if(PLAYER.colliderect(i) and i.effect == 'DEAD'):
            i.top -= 30
            return True
    if(PLAYER.top >= HEIGHT):
        return True
    return False

def playerWin():
    for i in door:
        if(PLAYER.colliderect(i)):
            return True
    return False

#======================DRAW STAGE======================
def drawStage4():
    for i in bg:
        i.draw()
    for i in floor:
        i.draw()
    for i in door:
        i.draw()
#======================DRAW & UPDATE======================
def draw():
    drawStage4()
    PLAYER.draw()

def update():
    global PLAYER
    if(PLAYER.state == 'DEAD' or PLAYER.state == 'WIN'):
        return
    ##Interactions
    if(playerLose()):
        PLAYER.state = 'DEAD'
        clock.schedule(restartStage,0.25)
        return
    if(playerWin()):
        PLAYER.state = 'WIN'
        clock.schedule(restartStage,0.25)
        return
    #On Floor
    PLAYER.floor = collideFloor()
    ##JUMP
    if(keyboard.up and PLAYER.state != 'FALL' and PLAYER.state != 'JUMP'):
        PLAYER.jumph = 0
        PLAYER.state = 'JUMP'
    if(PLAYER.state == 'JUMP'):
        PLAYER.image = 'player\\jump\\jumpr'
        PLAYER.top -= spdx*1.5
        PLAYER.jumph += spdx*1.5
        if(not collideRight()):
            PLAYER.direction = 'RIGHT'
            screenLeft()
        if(PLAYER.jumph >= PLAYER.height + 2*floor[0].height):
            PLAYER.state = 'FALL'
        return
    if not PLAYER.floor:
        PLAYER.state = 'FALL'
    if(PLAYER.state == 'FALL'):
        PLAYER.image = 'player\\landing\\landingr'
        PLAYER.top += spdx*1.5
        PLAYER.jumph -= spdx*1.5
        if(not collideRight()):
            PLAYER.direction = 'RIGHT'
            screenLeft()
        if collideFloor():
            PLAYER.state = 'IDLE'
        return
    ##MOVE RIGHT    
    if(not collideRight()):
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','RIGHT'
        PLAYER.frame += 0.25
        PLAYER.image = runrset[int(PLAYER.frame)%8]
        screenLeft()
        return
    ##IDLE
    if(PLAYER.state != 'IDLE'):
        PLAYER.frame = 0
    PLAYER.state = 'IDLE'
    ##IDLE
    if(PLAYER.state == 'IDLE'): 
        PLAYER.frame += 0.25
        PLAYER.image = idlerset[int(PLAYER.frame)%12]

restartStage()
pgzrun.go()
