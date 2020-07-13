import pgzrun
import random
import types
import os
SEPERATOR = '\\' if os.name == 'nt' else '/'
#======================Initialize======================
#COMMON VARIABLES
WIDTH,HEIGHT = 768,432
OUT = (-100,0) #Pos out of screen
TIME = 0
spdx = 3 #Vx of character and blocks
runlset,runrset,idlelset,idlerset,mobswalkr,mobswalkl = [],[],[],[],[],[] #Animations frame
bg,bg1,bg2 = [],[],[] #Background 
floor,door = [],[Actor('door')] #Floor,door
stage,substage = 0, 1 
deathCount = 0
songFlag = True #True: Time to change song
GAME_STATE = "MENU"

#UI Buttons
playButton = Actor("ui"+SEPERATOR+"play")
pauseButton = Actor("ui"+SEPERATOR+"pause")
stopButton = Actor("ui"+SEPERATOR+"stop")
okButton = Actor("ui"+SEPERATOR+"ok")
restartButton = Actor("ui"+SEPERATOR+"restart")
startButton = Actor("ui"+SEPERATOR+"start")
questionButton = Actor("ui"+SEPERATOR+"question")
ui = [playButton,pauseButton,stopButton,okButton,restartButton,startButton,questionButton]

#Stage 1
board,begin_pos,end_pos = [],[],[] #begin_pos是board初始时的左侧位置，end_pos是board终止时的左侧位置
star,starCount = [],[]

#Stage 2 & Stage 3
ground,block,layer1 = [],[],[] #Blocks
trap,killTrap,fallTrap,knife = [],[],[],[] #Traps
mobs,mobs1,mobs2 = [],[],[] #Mobs

#Stage 4
letters = []
HP_BAR = []
words = []
flag = False #Buttons
spd,fq = 5,30 #Speed of blocks and frequency

#======================Merge Lists======================
floor = ground + block + layer1 #Floor to be stepped
trap = killTrap + fallTrap #Traps
tiles = trap + floor + door #Tiles to be moved with screen
bg = bg1 + bg2 #Background
mobs = mobs1 + mobs2 #Mobs
blocks = tiles + mobs #Every blocks

#======================IMPORT DEFAULT IMAGES======================
#Character
for i in range(8):
    runrset.append("player"+SEPERATOR+"run"+SEPERATOR+"runr"+SEPERATOR+"right"+str(i))
    runlset.append("player"+SEPERATOR+"run"+SEPERATOR+"runl"+SEPERATOR+"left"+str(i))
for i in range(12):
    idlerset.append("player"+SEPERATOR+"idle"+SEPERATOR+"idler"+SEPERATOR+"idler"+str(i))
    idlelset.append("player"+SEPERATOR+"idle"+SEPERATOR+"idlel"+SEPERATOR+"idlel"+str(i))

##Stage 1
#Stars
for i in range(3):
    star.append(Actor('star'))

##Stage 3
#Mobs
for i in range(6):
    mobswalkl.append("mobs"+SEPERATOR+"walkl"+SEPERATOR+"walkl"+ str(i))
    mobswalkr.append("mobs"+SEPERATOR+"walkr"+SEPERATOR+"walkr" + str(i))

##Stage 4
#HP Bar
for i in range(21):
    HP_BAR.append("hp_bar"+SEPERATOR+str(i))
#Attack Effect
bossAttackEffect = Actor("transparent")
playerAttackEffect = Actor("transparent")

#======================SETUP CHARACTER======================
#PLAYER
PLAYER = Actor("player"+SEPERATOR+"idle"+SEPERATOR+"idler"+SEPERATOR+"idler0")
PLAYER.frame = 0
PLAYER.state = 'IDLE'
PLAYER.direction = 'RIGHT'
PLAYER.hp = 20
PLAYER.hpBar = Actor(HP_BAR[20])
#BOSS (for Stage 4)
BOSS = Actor("boss"+SEPERATOR+"idle")
BOSS.hp = 20
BOSS.hpBar = Actor(HP_BAR[20])
BOSS.hpdeduct = 0.5

#======================CAMERA(For stage 2 and 3)======================
rightLimit,leftLimit = 50*81-WIDTH/2,WIDTH/2 
rightBorder,leftBorder = 50*81-PLAYER.width,PLAYER.width
camCenter = leftBorder

#======================DEFINE CLASS======================
#Floor to be stepped by players, floor.collision handles player's collision with floor
class Floor(list):
    def collideFloor(self):
        for i in self:
            if (PLAYER.colliderect( \
                    i) and i.top - 4 * spdx <= PLAYER.bottom <= i.top + 4 * spdx and PLAYER.left >= i.left - 8 * spdx and PLAYER.right <= i.right + 8 * spdx):
                return True
        return False

    def collideLeft(self):
        for i in self:
            if (PLAYER.colliderect( \
                    i) and i.bottom - 4 * spdx <= PLAYER.bottom <= i.bottom + 4 * spdx and i.right - 4 * spdx <= PLAYER.left <= i.right + 4 * spdx):
                return True
        return False

    def collideRight(self):
        for i in self:
            if (PLAYER.colliderect( \
                    i) and i.bottom - 4 * spdx <= PLAYER.bottom <= i.bottom + 4 * spdx and i.left - 4 * spdx <= PLAYER.right <= i.left + 4 * spdx):
                return True
        return False
    
#======================INITIALIZE VARIABLES======================
def initializeVariable1():
    global PLAYER,starSum,starCount,star,floor,board,bg,all_elements,door
    #Background
    bg = []
    for i in range(5):
        bg.append(Actor("background"+SEPERATOR+"plx-" + str(i+1)))
    #Character
    PLAYER.jumph = 0
    PLAYER.frame = 0
    PLAYER.state = 'IDLE'
    PLAYER.direction = 'RIGHT'
    #Variables in common of 3 stages
    starSum = 0
    starCount,star = [],[]
    door = [Actor('door')]
    for i in range(3):
        star.append(Actor('star'))
    floor,board = Floor(),Floor()
    for i in range(3):
        starCount.append(Actor('greystar'))
    #Reset according to stages
    if(substage == 1):
        for i in range(2):
            floor.append(Actor("tileset"+SEPERATOR+"ground"))
    elif(substage == 2):
        for i in range(10):
            floor.append(Actor("tileset"+SEPERATOR+"block"))
    elif(substage == 3):
        for i in range(4):
            floor.append(Actor("tileset"+SEPERATOR+"block"))
        for i in range(2):
            board.append(Actor("tileset"+SEPERATOR+"board"))

def initializeVariable2():
    global PLAYER,bg1,bg2,floor,door,killTrap,knife
    #Empty lists to prevents bugs from append
    bg1,bg2 = [],[]
    floor,door = [],[]
    killTrap,knife = [],[]
    #Background
    for i in range(5):
        bg1.append(Actor("background"+SEPERATOR+"plx-" + str(i+1)))
        bg2.append(Actor("background"+SEPERATOR+"plx-" + str(i+1)))
    for i in range(25):
        floor.append(Actor("tileset"+SEPERATOR+"ground"))
    door.append(Actor("door"))
    door.append(Actor("door"))
    #Player
    PLAYER.jumph = 0
    PLAYER.frame = 0
    PLAYER.state = 'FALL'
    #Killing Traps
    for i in range(3):
        killTrap.append(Actor("mobs"+SEPERATOR+"walkl"+SEPERATOR+"walkl0"))
    for i in range(2):
        knife.append(Actor("knife"))

def initializeVariable3():
    global PLAYER,MaxJumpHeight,bg1,bg2,ground,block,layer1,door,killTrap,fallTrap,mobs1,mobs2,rightlimit,leftLimit,rightBorder,leftBorder,camCenter
    bg1,bg2,ground,block,layer1,door,killTrap,fallTrap,mobs1,mobs2 = [],[],[],[],[],[],[],[],[],[]
    #Background
    for i in range(5):
        bg1.append(Actor("background"+SEPERATOR+"plx-" + str(i+1)))
        bg2.append(Actor("background"+SEPERATOR+"plx-" + str(i+1)))
    #Floor
    for i in range(50):
        ground.append(Actor("tileset"+SEPERATOR+"ground"))
    for i in range(9):
        block.append(Actor("tileset"+SEPERATOR+"block"))
    for i in range(10):
        layer1.append(Actor("tileset"+SEPERATOR+"ground"))
    for i in range(1):
        door.append(Actor('door'))
    ##Trap
    #Kill Trap
    for i in range(6):
        tmp = Actor('spike')
        tmp.effect = 'DEAD'
        killTrap.append(tmp)
    #Fall Trap
    for i in range(2):
        fallTrap.append(Actor("tileset"+SEPERATOR+"ground"))  
        fallTrap[i].fall = False
    #Mobs
    for i in range(1):
        mobs1.append(Actor("mobs"+SEPERATOR+"walkr"+SEPERATOR+"walkr0"))
        mobs1[i].range = ground[0].width-mobs1[i].width/2
        mobs1[i].state = 'WALK'
        mobs1[i].direction = 'RIGHT'
        mobs1[i].frame = 0
        mobs1[i].jumph = 0
        mobs1[i].camCenter = 0
    for i in range(1):
        mobs2.append(Actor("mobs"+SEPERATOR+"walkr"+SEPERATOR+"walkr0"))
        mobs2[i].range = ground[0].width-mobs2[i].width/2
        mobs2[i].state = 'WALK'
        mobs2[i].direction = 'RIGHT'
        mobs2[i].frame = 0
        mobs2[i].jumph = 0
        mobs2[i].camCenter = 0
    #Player
    PLAYER.jumph = 0
    PLAYER.frame = 0
    PLAYER.state = 'FALL'
    PLAYER.direction = 'RIGHT'
    #Camera
    rightLimit,leftLimit = 50*81-WIDTH/2,WIDTH/2 
    rightBorder,leftBorder = 50*81-PLAYER.width,PLAYER.width
    camCenter = leftBorder
    MaxJumpHeight = PLAYER.height + 2*ground[0].height

def initializeVariable4():
    global TIME,PLAYER,BOSS,spd,fq,words,flag,letters,ground
    #Empty list to prevent append bugs
    ground,words,letters = [],[],[]
    flag = False #Key pressed, False: no key pressed
    #Floor
    for i in range(50):
        ground.append(Actor("tileset"+SEPERATOR+"ground"))
    #Player
    PLAYER.frame = 0
    PLAYER.state = 'IDLE'
    PLAYER.direction = 'RIGHT'
    PLAYER.image = "player"+SEPERATOR+"idle"+SEPERATOR+"idler"+SEPERATOR+"idler0"
    PLAYER.hp = 20
    PLAYER.hpBar = Actor(HP_BAR[20])
    #Boss
    BOSS.image = "boss"+SEPERATOR+"idle"
    BOSS.hp = 20
    BOSS.hpBar = Actor(HP_BAR[20])
    #Initialize base on substages
    if(substage == 1):
        for i in range(10):
            letters.append(str(i))
            BOSS.hpdeduct = 0.5
            spd,fq = 5,30
    elif(substage == 2):
        for i in range(26):
            letters.append(chr(97+i))
        BOSS.hpdeduct = 0.25
        spd,fq = 5,20

def initializeVariable():
    if(stage == 1):
        initializeVariable1()
    elif(stage == 2):
        initializeVariable2()
    elif(stage == 3):
        initializeVariable3()
    elif(stage == 4):
        initializeVariable4()

#======================MERGE LIST======================
def mergeList():
    global floor,trap,tiles,bg,blocks,mobs,killTrap
    if(stage == 2):
        bg = bg1 + bg2
        floor = floor+door+killTrap+knife
    elif(stage == 3):
        floor = ground + block + layer1
        trap = killTrap + fallTrap
        tiles = trap + floor + door
        bg = bg1 + bg2
        mobs = mobs1 + mobs2
        blocks = tiles + mobs

#======================SETUP MAP======================
#Substage map for stage 1
def Stage1Map1():
    global PLAYER,floor,door,star
    #Floor
    floor[0].bottomright = WIDTH * 0.5, HEIGHT - PLAYER.height - floor[0].height + 2
    floor[1].bottomleft = WIDTH * 0.5, HEIGHT - PLAYER.height - floor[0].height + 2
    #Door
    door[0].bottomright = floor[1].right, floor[1].top + 5
    #Player
    PLAYER.bottomleft = floor[0].topleft
    PLAYER.bottom -= 2
    #Star
    for i in range(3):
        star[i].bottomleft = floor[0].left + PLAYER.width + (i + 1) * 60, floor[0].top - 10

def Stage1Map2():
    global PLAYER,floor,door,star
    #Floor
    floor[0].midbottom = WIDTH * 0.5 - 26, HEIGHT - 30
    floor[1].midbottom = WIDTH * 0.5 + 26, HEIGHT - 30
    floor[2].bottomright = floor[0].topleft
    floor[3].bottomleft = floor[1].topright
    floor[4].bottomleft = floor[3].bottomright
    floor[5].bottomright = floor[2].topleft
    floor[6].bottomright = floor[3].topright
    floor[7].bottomright = floor[5].topright
    floor[8].bottomleft = floor[2].right, floor[7].bottom
    floor[9].bottomright = floor[6].topleft
    #Door
    door[0].bottomright = floor[4].topright
    #Player
    PLAYER.bottomleft = floor[0].topleft
    PLAYER.bottom -= 2
    #Star
    star[0].midbottom = floor[1].midtop
    star[1].midbottom = floor[2].midtop
    star[2].midbottom = floor[9].midtop

def Stage1Map3():
    global PLAYER, floor, board, door, star, begin_pos, end_pos
    #Floor
    floor[0].center = WIDTH * 0.5 - 3 * 52, HEIGHT * 0.5 + 3 * 52
    floor[1].center = WIDTH * 0.5 - 52, HEIGHT * 0.5 + 2 * 52
    floor[2].center = WIDTH * 0.5 + 52, HEIGHT * 0.5 + 2 * 52
    floor[3].center = WIDTH * 0.5 - 52, HEIGHT * 0.5 - 52
    #MovingBoard
    for i in range(2):
        board[i].midtop = WIDTH * 0.5 + (6 * i - 3) * 52, HEIGHT * 0.5 + (3.5 - 3 * i ) * 52
        begin_pos.append(board[i].left)
    end_pos = [WIDTH * 0.5 + 2.5 * 52, WIDTH * 0.5 - 4.5 * 52 ]
    #Door
    door[0].bottomleft = floor[0].left,floor[3].bottom
    #PLAYER
    PLAYER.bottomleft = floor[0].topleft
    PLAYER.bottom -= 2
    #Star
    star[0].center = WIDTH * 0.5 + 52, HEIGHT * 0.5 + 3*52
    star[1].center = WIDTH * 0.5 + 52, HEIGHT * 0.5 - 52
    star[2].center = WIDTH * 0.5 - 52, HEIGHT * 0.5 - 2 * 52

def initializeMap1():
    global bg,starCount
    #Background
    for i in range(5):
        bg[i].topleft = 0, 0
    #Countstar
    for i in range(3):
        starCount[i].midtop = WIDTH * 0.5 + (i - 1) * 50, 30
    #Initialize map based on substage
    if(substage == 1):
        Stage1Map1()
    elif(substage == 2):
        Stage1Map2()
    elif(substage == 3):
        Stage1Map3()

def initializeMap2():
    mergeList()
    #Player
    PLAYER.bottomleft = WIDTH/2,HEIGHT - floor[0].height
    #Background
    for i in range(5):
        bg1[i].topright = WIDTH*0.5,0
        bg2[i].topleft = WIDTH*0.5,0
    #Floor
    for i in range(25):
        floor[i].bottomleft = i*(floor[i].width - 2),HEIGHT
    for i in range(4,25,3):
        floor[i].bottomleft = OUT
    #Door
    door[0].bottomright = 25*(floor[0].width -2),HEIGHT-floor[0].height
    door[1].bottomright = PLAYER.bottomleft
    #Mobs
    killTrap[0].bottomleft = 6*(floor[0].width-2),HEIGHT - floor[0].height
    killTrap[1].bottomleft = 12*(floor[0].width-2),HEIGHT - floor[0].height
    killTrap[2].bottomleft = 18*(floor[0].width-2),HEIGHT - floor[0].height
    #Knife
    knife[0].topleft = 2*8*(floor[0].width-2),HEIGHT-floor[0].height-PLAYER.height/2
    knife[1].topleft = 2*14*(floor[0].width-2),HEIGHT-floor[0].height-PLAYER.height/2

def initializeMap3():
    mergeList()
    gap = ground[0].width - 2 #Gap between ground tiles
    layer1H = HEIGHT - PLAYER.height - ground[0].height + 2 #Layer 1 Height
    #Player
    PLAYER.topleft = 0,0
    #Background
    for i in range(5):
        bg1[i].topright = WIDTH*0.5,0
        bg2[i].topleft = WIDTH*0.5,0
    ##Trap
    #KillTrap
    killTrap[0].bottomleft = 0,HEIGHT-2
    killTrap[1].bottomleft = gap,HEIGHT-2
    killTrap[2].bottomright = 3*gap,HEIGHT-2
    killTrap[3].bottomleft = 12*gap,layer1H
    killTrap[4].bottomleft = 12*gap+killTrap[0].width,layer1H-2
    killTrap[5].bottomleft = 24*gap,layer1H-2
    #FallTrap
    fallTrap[0].bottomleft = 9*gap,HEIGHT
    fallTrap[1].bottomleft = 9*gap,layer1H
    #Floor
    for i in range(50):
        ground[i].bottomleft = i*(gap),HEIGHT
    for i in range(3,50,3):
        if(i == 12 or i == 15 or i == 18 or i == 21 or i == 24):
            continue
        ground[i].bottomleft = OUT
    #Block
    block[0].bottomleft = 15*gap,HEIGHT-ground[0].height
    block[1].bottomleft = block[0].bottomright
    block[2].bottomleft = block[1].bottomright
    block[3].bottomleft = 18*gap,HEIGHT-ground[0].height
    block[4].bottomleft = block[3].bottomright
    block[5].bottomleft = block[4].bottomright
    block[6].bottomleft = 21*gap,HEIGHT-ground[0].height
    block[7].bottomleft = block[6].bottomright
    block[8].bottomleft = block[7].bottomright
    #Layer1
    for i in range(10):
        layer1[i].bottomleft = 3*(i+1)*(gap),layer1H
    layer1[2].bottomleft = OUT
    layer1[4].bottomleft = OUT
    layer1[5].bottomleft = OUT
    layer1[6].bottomleft = OUT
    #Mobs
    mobs[0].bottomleft = 17*gap-mobs[0].width/2,HEIGHT - ground[0].height
    mobs[1].bottomleft = 20*gap-mobs[0].width/2,HEIGHT - ground[0].height
    #Door
    door[0].bottomright = layer1[7].topright

def initializeMap4():
    global PLAYER,BOSS
    #Player, Boss and thier hp bar,attack effects
    PLAYER.bottomleft = PLAYER.width*3,HEIGHT-ground[0].height
    BOSS.bottomright = WIDTH,HEIGHT
    PLAYER.hpBar.center = (100,320)
    BOSS.hpBar.center = (590,130)
    bossAttackEffect.center=(-310,650)
    playerAttackEffect.center=(420,130)
    #Floor
    for i in range(50):
        ground[i].topright = (i+1)*(ground[i].width-5),HEIGHT - ground[i].height + 2

def initializeMap():
    if(stage == 1):
        initializeMap1()
    elif(stage == 2):
        initializeMap2()
    elif(stage == 3):
        initializeMap3()
    elif(stage == 4):
        initializeMap4()

#======================RESTART STAGE======================
def restartStage():
    global songFlag
    #Moves ui buttons out of screen
    for i in ui:
        i.pos = OUT
    #Bgm choices
    if(songFlag):
        if(GAME_STATE == 'MENU'):
            sounds.victory.stop()
            sounds.running.stop()
            sounds.forest.stop()
            sounds.escape.stop()
            sounds.boss.stop()
            sounds.forest.play(-1)
            songFlag = False
        if(stage == 2):
            sounds.forest.stop()
            sounds.running.play(-1)
            songFlag = False
        elif(stage == 3):
            sounds.running.stop()
            sounds.escape.play(-1)
            songFlag = False
        elif(stage == 4):
            sounds.escape.stop()
            sounds.boss.play(-1)
            songFlag = False
    #Initialize!
    initializeVariable()
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

#======================SET ATTRIBUTE======================
PLAYER.__setattr__('moveRight',types.MethodType(moveRight,PLAYER))
PLAYER.__setattr__('moveLeft',types.MethodType(moveLeft,PLAYER))

#======================MOVE IN GROUP======================
#Background
def bgLeft():
    for i in bg:
        moveLeft(i)
def bgRight():
    for i in bg:
        moveRight(i)
#Floor
def blocksLeft():
    for i in blocks:
        i.left -= spdx
def blocksRight():
    for i in blocks:
        i.left += spdx

#Screen
def screenLeft():
    global camCenter
    if(stage == 2):
        for i in bg:
            moveLeft(i)
        for i in floor:
            i.left -= spdx
    else:
        camCenter += spdx
        if(camCenter > rightBorder):
            camCenter = rightBorder
        if(rightLimit <= camCenter):
            PLAYER.moveRight(1)
        elif(camCenter <= leftLimit):
            PLAYER.moveRight(1)
        else:
            bgLeft()
            blocksLeft()
def screenRight():
    global camCenter
    if(stage == 2):
        for i in bg:
            moveRight(i)
        for i in floor:
            i.left += spdx
    else:
        camCenter -= spdx
        if(camCenter < leftBorder):
            camCenter = leftBorder
        if(camCenter <= leftLimit):
            PLAYER.moveLeft(1)
        elif(rightLimit <= camCenter):
            PLAYER.moveLeft(1)
        else:
            bgRight()
            blocksRight()
#Mobs:
def mobsMove(act):
    act.frame += 0.25
    if(act.direction == 'RIGHT'):
        act.left += spdx/2
        act.camCenter += spdx/2
        act.image = mobswalkr[int(act.frame%6)]
    else:
        act.camCenter -= spdx/2
        act.left -= spdx/2
        act.image = mobswalkl[int(act.frame%6)]
def mobsJump(act):
    if(act.jumph <= MaxJumpHeight):
        act.top -= 1.5*spdx
        act.jumph += 1.5*spdx
    else:
        act.state = 'FALL'
def mobsFall(act):
    act.top += 1.5*spdx
    act.jumph -= 1.5*spdx

#======================INTERACTIONS======================
#Set GAME_STATE
def resumeGame():
    global GAME_STATE
    GAME_STATE = 'PLAY'
    restartStage()

def setGameClear():
    global GAME_STATE
    GAME_STATE = 'GAMECLEAR'
    
def setGameOver():
    global GAME_STATE
    GAME_STATE = 'GAMEOVER'

def setStageClear():
    global GAME_STATE
    GAME_STATE = 'STAGECLEAR'

#Mouse click(for ui buttons)
def on_mouse_down(pos):
    global GAME_STATE,stage,substage,songFlag,deathCount
    global stage,startButton,restartButton
    if restartButton.collidepoint(pos):
        restartButton.pos = OUT
        clock.schedule_unique(resumeGame,0.2)
    elif startButton.collidepoint(pos):
        stage = 1
        startButton.pos = OUT
        restartStage()
        GAME_STATE = 'PLAY'
    elif pauseButton.collidepoint(pos):
        pauseButton.pos = OUT
        GAME_STATE = 'PAUSE'
    elif playButton.collidepoint(pos):
        stopButton.pos = OUT
        playButton.pos = OUT
        GAME_STATE = 'PLAY'
    elif stopButton.collidepoint(pos):
        deathCount = 0
        stopButton.pos = OUT
        playButton.pos = OUT
        stage = 0
        substage = 1
        if(GAME_STATE != 'QUESTION'):
            songFlag = True
        GAME_STATE = 'MENU'
        restartStage()
    elif okButton.collidepoint(pos):
        okButton.pos = OUT
        clock.schedule_unique(resumeGame,0.2)
    elif questionButton.collidepoint(pos):
        questionButton.pos = OUT
        startButton.pos = OUT
        GAME_STATE = "QUESTION"

#======================FUNCTIONS FOR DIFFERENT STAGES======================
#STAGE1
def back(act, begin_pos):
    act.left = begin_pos

def moving_left(act):
    act.left -= 0.7 * spdx

def moving_right(act):
    act.left += 0.7 * spdx

def towards_left(begin_pos, end_pos):
    if end_pos < begin_pos:
        return True
    else:
        return False

#STAGE 2 & 3
#COLLISION
def collideFloor(act=PLAYER):
    for i in floor:
        if(act.colliderect(i) and i.top-4*spdx<= act.bottom <= i.top+4*spdx and act.left >= i.left-8*spdx and act.right <= i.right + 8*spdx):
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

#Stage 4
#Keyboard press(substage1:number, substage 2:letters)
def on_key_down(key):
    global flag
    flag=key.name.lower()

##Set player state (Pack in as functions for clock.schedule)
#Player
def PLAYER_idle():
    PLAYER.frame += 0.25
    PLAYER.image = idlerset[int(PLAYER.frame)%12]

def PLAYER_injured():
    global PLAYER
    PLAYER.image="player"+SEPERATOR+"injured"
    PLAYER.hp -= 5
    if(PLAYER.hp < 0):
        PLAYER.hp = 0
        PLAYER.image = "boss"+SEPERATOR+"injured"
    PLAYER.hpBar.image = HP_BAR[int(PLAYER.hp)]
    clock.schedule_unique(PLAYER_idle,1.0)
    sounds.lightning.set_volume(0.9)
    sounds.lightning.play()

#Boss
def BOSS_idle():
    BOSS.image="boss"+SEPERATOR+"idle"

def BOSS_injured():
    global BOSS
    BOSS.image="boss"+SEPERATOR+"injured"
    BOSS.hp -= BOSS.hpdeduct
    if(BOSS.hp < 0):
        BOSS.hp = 0
    BOSS.hpBar.image = HP_BAR[int(BOSS.hp)]
    clock.schedule(BOSS_idle,1.0)
    sounds.attack.play()
    sounds.attack.set_volume(0.4)

#Attack effects
def bossAttack():
    bossAttackEffect.image=("boss"+SEPERATOR+"attack")
    clock.schedule_unique(bossAttackNormal,0.3)
def bossAttackNormal():
    bossAttackEffect.image=("transparent")

def playerAttack():
    playerAttackEffect.image=("player"+SEPERATOR+"attack")
    clock.schedule_unique(playerAttackNormal,0.3)
def playerAttackNormal():
    playerAttackEffect.image=("transparent")

#================================VICTORY OR DEFEAT================================
#Stage 1
def playerLose1():
    global PLAYER, starSum
    if starSum < 3 and PLAYER.collidepoint(door[0].center):
        return True
    elif PLAYER.top >= HEIGHT:
        return True
    return False

def playerWin1():
    global PLAYER, starSum
    if starSum == 3 and PLAYER.collidepoint(door[0].center):
        sounds.bell.play()
        return True
    else:
        return False

#Stage 2
def playerLose2():
    global PLAYER
    PLAYER.status = 'DEAD'
    for i in killTrap:
        if(PLAYER.colliderect(i)):
            return True
    for i in knife:
        if(PLAYER.colliderect(i)):
            sounds.spiketrap.play()
            return True
    if(PLAYER.top >= HEIGHT):
        return True
    return False

def playerWin2():
    for i in door:
        if(PLAYER.colliderect(i)):
            sounds.bell.play()
            return True
    return False

#Stage 3
def playerLose3():
    global PLAYER
    PLAYER.status = 'DEAD'
    for i in killTrap:
        if(PLAYER.colliderect(i) and i.effect == 'DEAD'):
            sounds.spiketrap.play()
            i.top -= 30
            return True
    for i in mobs:
        if(PLAYER.colliderect(i)):
            return True
    if(PLAYER.top >= HEIGHT):
        return True
    return False

def playerWin3():
    for i in door:
        if(PLAYER.colliderect(i)):
            sounds.bell.play()
            return True
    return False

#Stage 4
def playerLose4():
    if(PLAYER.hp <= 0):
        return True
    return False

def playerWin4():
    if(BOSS.hp <= 0):
        return True
    return False

#======================DRAW STAGE======================
def drawStage1():
    for i in bg:
        i.draw()
    for i in starCount:
        i.draw()
    for i in star:
        i.draw()
    for i in floor:
        i.draw()
    for i in door:
        i.draw()
    if substage == 3:
        for i in board:
            i.draw()
    PLAYER.draw()

def drawStage2():
    for i in bg:
        i.draw()
    for i in floor:
        i.draw()
    for i in door:
        i.draw()
    PLAYER.draw()

def drawStage3():
    for i in bg:
        i.draw()
    for i in trap:
        i.draw()    
    for i in tiles:
        i.draw()
    for i in mobs:
        i.draw()
    PLAYER.draw()

def drawStage4():
    for i in range(4):
        screen.blit(("background"+SEPERATOR+"plx-"+str(i+1)),(0,0))
    for i in ground:
        i.draw()
    PLAYER.draw()
    BOSS.draw()
    bossAttackEffect.draw()
    playerAttackEffect.draw()
    PLAYER.hpBar.draw()
    BOSS.hpBar.draw()
    for i in words:
        i.draw()

def draw():
    #GAME_STATE -> UI
    if(GAME_STATE == 'QUESTION'):
        for i in range(5):
            screen.blit(("background"+SEPERATOR+"plx-" + str(i+1)),(0,0))
        screen.blit("ui"+SEPERATOR+"move",(160,40))
        screen.blit("ui"+SEPERATOR+"arrowright",(450,35))
        screen.blit("ui"+SEPERATOR+"arrowleft",(330,30))
        screen.blit("ui"+SEPERATOR+"arrowup",(335,150))
        screen.blit("ui"+SEPERATOR+"jump",(150,160))
        stopButton.center=(360,310)
        stopButton.draw()
        return
    elif(GAME_STATE == 'MENU'):
        for i in range(5):
            screen.blit(("background"+SEPERATOR+"plx-" + str(i+1)),(0,0))
        screen.blit("ui"+SEPERATOR+"title",(70,0))
        #screen.blit('titlezh',(220,80))
        startButton.center = (360,280)
        startButton.draw()
        questionButton.topright = (WIDTH,0)
        questionButton.draw()
        return    
    if(GAME_STATE == 'STAGECLEAR'):
        screen.blit("ui"+SEPERATOR+"stageclear",(220,80))
        okButton.center=(360,310)
        okButton.draw()
        return
    elif(GAME_STATE =='GAMEOVER'):
        for i in range(5):
            screen.blit(("background"+SEPERATOR+"plx-" + str(i+1)),(0,0))
        screen.blit("ui"+SEPERATOR+"gameover",(240,70))
        screen.draw.text("DEATHS:%d " % deathCount, (315, 380))
        restartButton.center=(360,310)
        restartButton.draw()
        return
    elif(GAME_STATE == 'PAUSE'):
        for i in range(5):
            screen.blit(("background"+SEPERATOR+"plx-" + str(i+1)),(0,0))
        playButton.center=(280,310)
        stopButton.center=(420,310)
        playButton.draw()
        stopButton.draw()
        return
    elif(GAME_STATE == 'GAMECLEAR'):
        for i in range(5):
            screen.blit(("background"+SEPERATOR+"plx-" + str(i+1)),(0,0))
        screen.blit("ui"+SEPERATOR+"gameclear",(220,80))
        stopButton.center=(360,310)
        stopButton.draw()
        return
    screen.clear()
    if(stage == 1):
        drawStage1()
    elif(stage == 2):
        drawStage2()
    elif(stage == 3):
        drawStage3()
    elif(stage == 4):
        drawStage4()
    pauseButton.topright = WIDTH,0
    pauseButton.draw()

def update1():
    global PLAYER, starSum, substage, begin_pos, end_pos,stage,songFlag,deathCount
    if(PLAYER.state == 'DEAD' or PLAYER.state == 'WIN'):
        return
    #True if Player is on floor
    PLAYER.floor = (floor.collideFloor() or board.collideFloor())
    ##Win or Lose
    if playerLose1():
        deathCount+= 1
        PLAYER.state = 'DEAD'
        clock.schedule(setGameOver,0.5)
        return
    if playerWin1():
        substage += 1
        if(substage == 4):
            substage = 1
            stage += 1
        PLAYER.state = 'WIN'
        songFlag = True
        setStageClear()
    ##Pick Star
    for i in star:
        if PLAYER.colliderect(i):
            star.remove(i)
            sounds.star.play()
            starCount[starSum].image = 'brightstar'
            starSum += 1
    ##MovingBoard
    if board != []:
        for i in range(len(board)):
            if towards_left(begin_pos[i], end_pos[i]):
                moving_left(board[i])
                if board[i].left <= end_pos[i]:
                    # PLAYER.state = 'FALL'
                    back(board[i], begin_pos[i])
            else:
                moving_right(board[i])
                if board[i].left >= end_pos[i]:
                    back(board[i], begin_pos[i])
    ##JUMP
    if(keyboard.up and PLAYER.state != 'FALL' and PLAYER.state != 'JUMP'):
        PLAYER.jumph = 0
        PLAYER.state = 'JUMP'
        sounds.jump.play()
    if(PLAYER.state == 'JUMP'):
        if(PLAYER.direction == 'RIGHT'):
            PLAYER.image = "player"+SEPERATOR+"jump"+SEPERATOR+"jumpr"
        elif (PLAYER.direction == 'LEFT'):
            PLAYER.image = "player"+SEPERATOR+"jump"+SEPERATOR+"jumpl"
        PLAYER.top -= spdx*1.5
        PLAYER.jumph += spdx*1.5
        if(keyboard.right):
            PLAYER.direction = 'RIGHT'
        elif(keyboard.left):
            PLAYER.direction = 'LEFT'
        if(PLAYER.jumph >= PLAYER.height + 2*floor[0].height):
            PLAYER.state = 'FALL'
        return
    if not PLAYER.floor:
        PLAYER.state = 'FALL'
    if(PLAYER.state == 'FALL'):
        if(PLAYER.direction == 'RIGHT'):
            PLAYER.image = "player"+SEPERATOR+"landing"+SEPERATOR+"landingr"
        elif (PLAYER.direction == 'LEFT'):
            PLAYER.image = "player"+SEPERATOR+"landing"+SEPERATOR+"landingl"
        PLAYER.top += spdx*1.5
        PLAYER.jumph -= spdx*1.5
        if(keyboard.right):
            PLAYER.direction = 'RIGHT'
        elif(keyboard.left):
            PLAYER.direction = 'LEFT'
        if PLAYER.floor:
            PLAYER.state = 'IDLE'
        return
    ##MOVE RIGHT
    if(keyboard.right and not floor.collideRight()):
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','RIGHT'
        PLAYER.frame += 0.25
        PLAYER.image = runrset[int(PLAYER.frame)%8]
        PLAYER.moveRight(1)
        return
    ##MOVE LEFT
    elif(keyboard.left and not floor.collideLeft()):
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','LEFT'
        PLAYER.frame += 0.25
        PLAYER.image = runlset[int(PLAYER.frame)%8]
        PLAYER.moveLeft(1)
        return
    if(PLAYER.state != 'IDLE'):
        PLAYER.frame = 0
    PLAYER.state = 'IDLE'
    ##IDLE
    if(PLAYER.state == 'IDLE' and PLAYER.direction == 'LEFT'):
        PLAYER.frame += 0.25
        PLAYER.image = idlelset[int(PLAYER.frame)%12]
    elif(PLAYER.state == 'IDLE' and PLAYER.direction == 'RIGHT'):
        PLAYER.frame += 0.25
        PLAYER.image = idlerset[int(PLAYER.frame)%12]

def update2():
    global PLAYER,stage,songFlag,deathCount
    if(PLAYER.state == 'DEAD' or PLAYER.state == 'WIN'):
        return
    ##Win or Lose
    if(playerLose2()):
        deathCount += 1
        PLAYER.state = 'DEAD'
        clock.schedule(setGameOver,0.5)
        return
    if(playerWin2()):
        PLAYER.state = 'WIN'
        stage += 1
        songFlag = True
        setStageClear()
    for i in knife:
        i.left -= spdx
    #True if Player is on floor
    PLAYER.floor = collideFloor()
    ##JUMP
    if(keyboard.up and PLAYER.state != 'FALL' and PLAYER.state != 'JUMP'):
        PLAYER.jumph = 0
        sounds.jump.play()
        PLAYER.state = 'JUMP'
    if(PLAYER.state == 'JUMP'):
        PLAYER.image = "player"+SEPERATOR+"jump"+SEPERATOR+"jumpr"
        PLAYER.top -= spdx*1.5
        PLAYER.jumph += spdx*1.5
        if(not collideRight()):
            PLAYER.direction = 'RIGHT'
            screenLeft()
        if(PLAYER.jumph >= PLAYER.height + 2*floor[0].height):
            PLAYER.state = 'FALL'
        return
    #FALL
    if not PLAYER.floor:
        PLAYER.state = 'FALL'
    if(PLAYER.state == 'FALL'):
        PLAYER.image = "player"+SEPERATOR+"landing"+SEPERATOR+"landingr"
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

def update3():
    global PLAYER,mobs,stage,songFlag,deathCount
    if(PLAYER.state == 'DEAD' or PLAYER.state == 'WIN'):
        return
    ##Win or Lose
    if(playerLose3()):
        deathCount += 1
        PLAYER.state = 'DEAD'
        clock.schedule(setGameOver,0.5)
        return
    if(playerWin3()):
        PLAYER.state = 'WIN'
        stage += 1
        songFlag = True
        setStageClear()
    #MobsMove
    for i in mobs:
        if(i.camCenter <= -i.range):
            i.direction = 'RIGHT'
        elif(i.camCenter >= i.range):
            i.direction = 'LEFT'
        if(i.state == 'FALL' and collideFloor()):
            i.state = 'WALK'
        if(i.state == 'JUMP'):
            mobsJump(i)
        if(i.state != 'JUMP' and not collideFloor(i)):
            i.state = 'FALL'
            mobsFall(i)
        mobsMove(i)
    #fallTrap
    for i in fallTrap:
        if(i.fall):
            i.top += 5
        if(PLAYER.colliderect(i) and i.top-4*spdx<= PLAYER.bottom <= i.top+4*spdx):
            sounds.falltrap.play()
            i.top += 5
            i.fall = True
    #On Floor
    PLAYER.floor = collideFloor()
    ##JUMP
    if(keyboard.up and PLAYER.state != 'FALL' and PLAYER.state != 'JUMP'):
        PLAYER.jumph = 0
        PLAYER.state = 'JUMP'
        sounds.jump.play()
    if(PLAYER.state == 'JUMP'):
        if(PLAYER.direction == 'RIGHT'):
            PLAYER.image = "player"+SEPERATOR+"jump"+SEPERATOR+"jumpr"
        elif (PLAYER.direction == 'LEFT'):
            PLAYER.image = "player"+SEPERATOR+"jump"+SEPERATOR+"jumpl"
        PLAYER.top -= spdx*1.5
        if(mobs[1].state != 'FALL'):
            mobs[1].state = 'JUMP'
        PLAYER.jumph += spdx*1.5
        if(keyboard.right and not collideRight()):
            PLAYER.direction = 'RIGHT'
            screenLeft()
        elif(keyboard.left and not collideLeft()):
            PLAYER.direction = 'LEFT'
            screenRight()
        if(PLAYER.jumph >= PLAYER.height + 2*ground[0].height):
            PLAYER.state = 'FALL'
        return
    if not PLAYER.floor:
        PLAYER.state = 'FALL'
    #FALL
    if(PLAYER.state == 'FALL'):
        if(PLAYER.direction == 'RIGHT'):
            PLAYER.image = "player"+SEPERATOR+"landing"+SEPERATOR+"landingr"
        elif (PLAYER.direction == 'LEFT'):
            PLAYER.image = "player"+SEPERATOR+"landing"+SEPERATOR+"landingl"
        PLAYER.top += spdx*1.5
        PLAYER.jumph -= spdx*1.5
        if(keyboard.right and not collideRight()):
            PLAYER.direction = 'RIGHT'
            screenLeft()
        elif(keyboard.left and not collideLeft()):
            PLAYER.direction = 'LEFT'
            screenRight()
        if collideFloor():
            PLAYER.state = 'IDLE'
        return
    ##MOVE RIGHT    
    if(keyboard.right and not collideRight()):
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','RIGHT'
        PLAYER.frame += 0.25
        PLAYER.image = runrset[int(PLAYER.frame)%8]
        screenLeft()
        return
    ##MOVE LEFT
    elif(keyboard.left and not collideLeft()): 
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','LEFT'
        PLAYER.frame += 0.25
        PLAYER.image = runlset[int(PLAYER.frame)%8]
        screenRight()
        return
    if(PLAYER.state != 'IDLE'):
        PLAYER.frame = 0
    PLAYER.state = 'IDLE'
    ##IDLE
    if(PLAYER.state == 'IDLE' and PLAYER.direction == 'LEFT'): 
        PLAYER.frame += 0.25
        PLAYER.image = idlelset[int(PLAYER.frame)%12]
    elif(PLAYER.state == 'IDLE' and PLAYER.direction == 'RIGHT'):
        PLAYER.frame += 0.25
        PLAYER.image = idlerset[int(PLAYER.frame)%12]

def update4():
    global PLAYER,flag,key_pressed,TIME,spd,substage,songFlag,stage,deathCount
    TIME += 1
    if(PLAYER.state == 'DEAD' or PLAYER.state == 'WIN'):
        return
    ##Win or Lose
    if(playerWin4()):
        substage+=1
        PLAYER.state ='WIN'
        if(substage == 2):
            setStageClear()
        elif(substage == 3):
            sounds.boss.stop()
            setGameClear()
            sounds.victory.play()
        return
    if(playerLose4()):
        deathCount += 1
        PLAYER.state = 'DEAD'
        clock.schedule(setGameOver,0.5)
        return
    ##Generate letter blocks
    if (TIME % fq) == 0:
        x=random.choice(letters)
        y=str.upper(x)
        t=Actor("alphabets"+SEPERATOR+x)
        if(substage == 1):
            t.name = "k_"+x
        else:
            t.name = x
        t.topright = 0,0
        words.append(t)
    ##Check whether letter blocks is out of map, remove if so
    for i in words:
        i.left += spd
        if i.left>=WIDTH:
           words.remove(i)
           PLAYER_injured()
           bossAttack()
    ##Check where key pressed match the block at the right,attacks if so,hurt otherwise
    if(words != [] and words[0].name == flag):
        words.remove(words[0])
        BOSS_injured()
        playerAttack()
        flag = False
    else:
        if flag:
            PLAYER_injured()
            bossAttack()
            flag= False

def update():
    if(GAME_STATE == 'PAUSE' or GAME_STATE == 'STAGECLEAR' or GAME_STATE == 'GAMECLEAR'):
        return
    if(stage == 1):
        update1()
    elif(stage == 2):
        update2()
    elif(stage == 3):
        update3()
    elif(stage == 4):
        update4()

restartStage()
pgzrun.go()