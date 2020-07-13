![图片](https://uploader.shimo.im/f/EiRdGqZJrNFyHaHx.png!thumbnail)

顾景佳，黄彬，柯旭洺，尤俊浩（排名按音序）


---
## 摘要

本次项目是利用pygame zero制作的闯关游戏。游戏实现了连续动画效果，设有多道关卡和多种元素，玩法丰富；同时兼顾游戏的艺术性，像素画风与背景音乐相互融合极大增强游戏的体验。

### **第一关**：初入森林——搜集小星星

![图片](https://uploader.shimo.im/f/rbuxOuGSSzxydQcK.png!thumbnail)

### **第二关**：跑酷——越过所有的障碍

![图片](https://uploader.shimo.im/f/ha9pIOueSOOrD36w.png!thumbnail)

### **第三关**：危机四伏——躲过伪装的陷阱

![图片](https://uploader.shimo.im/f/qnypEYS8xiOn5kND.png!thumbnail)

![图片](https://uploader.shimo.im/f/L9EQt1UgCfPXJcHv.png!thumbnail)

### ** ****第四关**：恐惧——有限时间内，在键盘上按下对应字符的键，击杀Boss

![图片](https://uploader.shimo.im/f/odqaRxDPbqmTjigm.png!thumbnail)

 


---
## 一、选题及创意

         经过组员讨论，我们一致选择软件项目，开发小游戏。由于组内四位成员代码能力各不相同，我们决定采用闯关模式，每个组员根据自己的创意和能力设计出一个小游戏，然后串联成完整的故事线，最后整合成一个有四个关卡的游戏。

       游戏名为Out of The Woods，中文名穿越丛林。寓意有双重意思，即有穿越丛林的意思，也有脱离困境之意。背景设立在莽莽的丛林中，游戏由四大关组成，难度递进。随着丛林探索的深入，游戏节奏由慢到快，由舒缓到刺激，在通过层层任务、经历种种阻碍后，玩家终于与Boss对抗，接受终极挑战。

       为了增加游戏游戏的可玩性和趣味性，我们只对操作方法进行了基本的介绍，玩法和障碍则让玩家自己探索。游戏中设置了移动板、陷阱、运动障碍物等元素，需要玩家摸索他们的规律，同时依靠敏捷的操作与反应才能通关，这对玩家的思考能力以及技术水平都是一种挑战。


---
## 二、设计方案

       整体框架由游戏素材以及四个游戏关卡的代码块组成。而每个小游戏的具体又可细分为几个小关卡，主要是由以下几个主要模块构成：

1. 导入需要用到的游戏素材

游戏开始前的设置：包括背景、人物、音效、障碍物等

1. 初始化变量

游戏开始前的设置：包括关卡所要用到的所有变量的值与Actors的初始位置

1. 游戏显示相关

draw()函数——绘制屏幕、update()函数——更新变量

1. 游戏主体逻辑处理

游戏规则相关如操作方式、人物的移动、障碍物的设置，游戏通过和结束的规则

1. 游戏用户交互界面的设置

暂停、帮助等图标选项、以及通关成功、失败等提示，使得游戏完整性更强

![图片](https://uploader.shimo.im/f/1GInduZ2luoyFCc5.png!thumbnail)

![图片](https://uploader.shimo.im/f/CZ1fjQKQ5QsAzCF0.png!thumbnail)

![图片](https://uploader.shimo.im/f/YysEVA4499QbZI04.png!thumbnail)

![图片](https://uploader.shimo.im/f/skf8jtCDYIIYjwQT.png!thumbnail)


---
## 三、实现方案及代码分析


---
### 第一步：初始化

1. 变量的声明

先定义后续需要用到的所有全局变量

```python
WIDTH,HEIGHT = 768,432
OUT = (-100,0)
TIME = 0
spdx = 3
...
```
1. 列表的合一

把同类型的列表化成一个，方便后续的处理（如循环等）

```python
floor = ground + block + layer1
trap = killTrap + fallTrap
tiles = trap + floor + door
...
```
1. 游戏素材的导入

注1:由于Mac系统和Windows系统的路径处理方式不同，故采用SEPERATOR作为分隔词

```python
SEPERATOR = '\\' if os.name == 'nt' else '/'
for i in range(8):
    runrset.append("player"+SEPERATOR+"run"+SEPERATOR+"runr"+SEPERATOR+"right"+str(i))
...
```
1. 类的定义

为了方便处理，我们定义了Floor()类，以处理场景地板与人物的碰撞


---
### 第二步：程序逻辑的统一

在确保每个关卡都能正常运行的前提下，把代码的基本逻辑统一化，方便后续的整合。

整体来看，控制游戏进程处理的有下列几个模块：

1. 模块（一）——变量的初始化，initializeVariables()
1. 模块（二）——地图的初始化,initializeMap()
1. 模块（三）——屏幕绘制 ，draw() 
1. 模块（四）——状态更新，update() 

 

主要模块的操控因子为stage和GAME_STATE。stage表明的是现在到了第几关，而GAME_STATE则表明了当前的游戏状态，如、暂停、帮助、通关等界面。通过两个变量就可以控制游戏的进程，极大提升了游戏的可拓展性，只要把地图设置好，继续拓展也只是复制贴上的功夫，模块化处理的思想对于处理大规模的程序效果显著的。

进一步通过一个函数操控游戏的画面与活动：

注2：部分重复性质（实现原理相同）的代码采用省略号...忽略，详情请参见源代码

```python
def restartStage():
    global songFlag #是否切换音乐
    for i in ui:
        i.pos = OUTse    initializeVariable()
...
    initializeMap()
```

---
### 第三步：一般性的函数

1. 处理交互事件的函数

包括用户交互界面各个按钮事件的处理

```python
def on_mouse_down(pos):
...
    if restartButton.collidepoint(pos):
        restartButton.pos = OUT
        clock.schedule_unique(resumeGame,0.2)
...
```
1. 改变游戏状态的函数

在游戏进程时，强制改变游戏界面的函数，比如死亡界面、暂停页面

```python
def resumeGame():
    global GAME_STATE
    GAME_STATE = 'PLAY'
    restartStage()
def setGameClear():
    global GAME_STATE
    GAME_STATE = 'GAMECLEAR'  
...
```

---
### 第四步：关卡的具体化与特殊化处理

这里主要介绍各个关卡特殊的函数定义以及掌控游戏逻辑的核心，模块（四）——update()函数

移动模式由第三关特化而成，所有方块的移动可总结成下列两个函数，根据需要采用两种模式，模式(0)：移动到左边界会从右边界出来；模式(1)：正常移动

注3：整合后用数字代表各个关卡的函数，比如关卡一的update函数就是update1()、

```python
##Mode 0: Infinite Move; Mode 1: Bordered Move
def moveLeft(act,mode=0): 
    if(mode == 1 and act.left <= 0):
        return
    act.left -= spdx
    if(mode == 0 and act.right < 0):
        act.left = WIDTH-spdx
...
```
人物与地板的碰撞判定：
```python
def collideFloor(act=PLAYER):
    for i in floor:
        if(act.colliderect(i) and i.top-4*spdx<= act.bottom <= i.top+4*spdx and act.left >= i.left-8*spdx and act.right <= i.right + 8*spdx):
            return True
    return False
def collideLeft():
    for i in floor:
        if(PLAYER.colliderect(i) and i.bottom-4*spdx <= PLAYER.bottom <= i.bottom+4*spdx and i.right-4*spdx <= PLAYER.left <= i.right+4*spdx):
            return True
    return False
...
```
collideFloor()判断人物是否站立在地板上，进而判断人物是否跌落；而collideLeft()判断人物是否碰到墙壁，限制x轴位移。其中由于pygamezero 帧上限，碰撞边界可能会超过，所以不能直接用 == 判定 ，故采用4*spdx
#### 关卡一：收集小星星

```python
def update1():
...
    ##Pick Star
    for i in star:
        if PLAYER.colliderect(i):
            star.remove(i)
            sounds.star.play()
            starCount[starSum].image = 'brightstar'
            starSum += 1
    ##Moving Board
    if board != []:
        for i in range(len(board)):
            if towards_left(begin_pos[i], end_pos[i]):
                moving_left(board[i])
                if board[i].left <= end_pos[i]:
                    # PLAYER.state = 'FALL'
                    back(board[i], begin_pos[i])
...
   ##MOVE RIGHT
    if(keyboard.right and not floor.collideRight()):
        if(PLAYER.state != 'RUN'):
            PLAYER.frame = 0
        PLAYER.state,PLAYER.direction = 'RUN','RIGHT'
        PLAYER.frame += 0.25
        PLAYER.image = runrset[int(PLAYER.frame)%8]
        PLAYER.moveRight(1)
        return
...
```
update()函数里主要的接口有判断输赢的函数playerWin()、playerLose()；实现人物移动的函数moveLeft()、moveRight();
除此之外，各种游戏的判断也在update()函数里面执行，比如小星星收集的计数、关卡3-3的板子的循环移动，另外，关卡一限制了一边跑一边跳的行动模式。

```python
def playerLose1():
    global PLAYER, starSum
    if starSum < 3 and PLAYER.collidepoint(door[0].center):
        return True
    elif PLAYER.top >= HEIGHT:
        return True
    return False
def playerWin1():
    global PLAYER, starSum
    if starSum == 3 and PLAYER.collidepoint(door[0].center):
        sounds.bell.play()
        return True
    else:
        return False
```
胜利条件是收集到三颗星星并且触碰到通关门，要是没到三个星星就动到门或者是掉落地图外，就算失败。
#### 关卡二：跑酷

只保留跳跃的操作。update()函数主干与第一关大致相同，唯一不同的是人物的移动是采用了相对运动来造成视觉效果。人物只是维持向右边跑的动作，移动的反而是背景。具体代码将在关卡三给出。

```python
def playerLose2():
    global PLAYER
    PLAYER.status = 'DEAD'
    for i in knife:
        if(PLAYER.colliderect(i)):
            sounds.spiketrap.play()
            return True
    if(PLAYER.top >= HEIGHT):
        return True
    return False
def playerWin2():
    for i in door:
        if(PLAYER.colliderect(i)):
            sounds.bell.play()
            return True
    return False
```
输的条件新增怪物致死，只要加个碰撞判定就行，而飞刀由于要塑造出迎面而来的感觉，所以在所有方块都左移的前提下，它还要与其他方块再多一个相对速度，只要在update()函数里让他左移多一次就行。
#### 关卡三：危机四伏

这关的行动模式是上述两关模板，左右移动只需根据键盘按键作出响应，除非碰到墙壁，不然都能成功移动；而跳跃和坠落的判定则更加复杂，我们给人物增添了当前跳跃高度PLAYER.jumph这个属性，记录其当前跳跃高度，当超过了最高跳跃高度，则人物开始坠落，只有当人物与地板的碰撞时，才能恢复到初始状态"IDLE"。

```python
#跳跃
if(keyboard.up and PLAYER.state != 'FALL' and PLAYER.state != 'JUMP'):
        PLAYER.jumph = 0
        PLAYER.state = 'JUMP'
        sounds.jump.play()
```
```python
if(PLAYER.state == 'FALL'):
...
        if collideFloor():
            PLAYER.state = 'IDLE'
        return
```
这关的特点是多重的陷阱：
1. 尖刺，先画陷阱，再画地板就可以隐藏陷阱，只要设定让玩家碰撞到陷阱时，陷阱再往上位移就完成了。
2. 掉落陷阱，外形采用普通地板，但是经过触碰后却会直接掉落，不要加入floor列表里，并且设定碰撞后就会掉落即可。
3. 怪物跟随跳跃，把怪物同样赋予PLAYER的跳跃属性，而"跟随"只需要在人物跳跃时追加一个判断即可

另，关卡里的怪物是会在固定范围内左右移动的，与关卡一Moving Board回到原点的方式不同，怪物的移动方式是有固定轨迹的，实现方法如下：

```python
def mobsMove(act):
    act.frame += 0.25
    if(act.direction == 'RIGHT'):
        act.left += spdx/2
        act.camCenter += spdx/2
        act.image = mobswalkr[int(act.frame%6)]
    else:
        act.camCenter -= spdx/2
        act.left -= spdx/2
        act.image = mobswalkl[int(act.frame%6)]
```
通过赋予怪物一个camCenter属性，就能有效的控制其活动范围。
最后补充关卡二的镜头移动实现方法：

```python
def screenLeft():
    global camCenter
    if(stage == 2):
        for i in bg:
            moveLeft(i)
        for i in floor:
            i.left -= spdx
    else: #Stage 3
        camCenter += spdx
        if(camCenter > rightBorder):
            camCenter = rightBorder
        if(rightLimit <= camCenter):
            PLAYER.moveRight(1)
        elif(camCenter <= leftLimit):
            PLAYER.moveRight(1)
        else:
            bgLeft()
            blocksLeft()
```
要实现玩家右移的视觉效果，可以采用屏幕、方块的左移来实现。然而在关卡三还要考量人物到了左右边界时，人物就不再停留在中心了。此时画面是不动的，动的则应该是人物本身。所以可以采用camCenter这一变量判断。关卡二则是去除了这一条件的弱化版。
注4:背景的地图移动采用模式0，这样只需要两张图片即可实现无限轮回

失败条件和胜利条件除了新增尖刺陷阱致死外，与关卡二大同小异。

#### 关卡四：恐惧——Boss战

这个关卡由接宝物创新，引入频率和速度的关系。交互方式选择了键盘打字的方式，所以首先要定义一个flag记录当前的按键状态（flag == FALSE 代表当前无按键交互）。

而方块组的记录采用list，这是因为用dict的话一个按键就会把重复字母的方块清空。

```python
#生成方块组
if (TIME % fq) == 0:
        x=random.choice(letters)
        y=str.upper(x)
        t=Actor("alphabets"+SEPERATOR+x)
        if(substage == 1):
            t.name = "k_"+x
        else:
            t.name = x
        t.topright = 0,0
        words.append(t)
```
```python
#方块超出屏幕，人物就掉血
for i in words:
        i.left += spd
        if i.left>=WIDTH:
           words.remove(i)
           PLAYER_injured()
           bossAttack()
```
```python
#按对字母就攻击，按错了就被攻击（必须从最右边的字母方格按起）
if(words != [] and words[0].name == flag):
        words.remove(words[0])
        BOSS_injured()
        playerAttack()
        flag = False
    else:
        if flag:
            PLAYER_injured()
            bossAttack()
            flag= False
```

---
### 第五步：交互界面——UI的处理

交互界面在游戏的任何进程里优先级都是最高的，所以不采用stage进行判断，而新增一个变量GAME_STATE。在update()里判断如果当前游戏状态处于UI界面时，就直接返回，不更新任何状态，即可暂时保留当前游戏内容。

而GAME_STATE则直接由鼠标与按键的交互更新。

```python
def on_mouse_down(pos):
    global GAME_STATE,stage,substage,songFlag,deathCount
    global stage,startButton,restartButton
    if restartButton.collidepoint(pos):
        restartButton.pos = OUT
        clock.schedule_unique(resumeGame,0.2)
    elif startButton.collidepoint(pos):
        stage += 1
        startButton.pos = OUT
        restartStage()
...
```
在交互完以后必须把按键挪到屏幕外，以免出现按键虽然没显示，实际却仍在那个位置的bug。

---
### 第六步：游戏的美化加工

由于pygame zero没有内置对gif图片的直接处理，所以我们把Actor的移动动画以帧为单位来导入列表，方便后续使用，下面以怪物的左移动画为示范：

```python
##先导入图片
#Mobs 
for i in range(6):
    mobswalkl.append("mobs"+SEPERATOR+"walkl"+SEPERATOR+"walkl"+ str(i))
...
##再赋予mobs当前该调用的帧数作为属性
#In initializeVariable2()
for i in range(1):
        ...
        mobs2[i].frame = 0
        ...
##在调用移动函数里同步增加当前帧数
def mobsMove(act):
    act.frame += 0.25
    if(act.direction == 'RIGHT'):
        act.left += spdx/2
        act.camCenter += spdx/2
##最后直接把对应的帧数直接赋值给mobs.image即可
        act.image = mobswalkr[int(act.frame%6)] #模6：完整动作由6帧构成
...
```
关卡四的攻击特效处理是先把攻击设成透明，在判断玩家/Boss受伤时同步调用显示攻击效果，并利用clock.schedule在固定时间后调整回透明。
音效处理可直接与事件进行绑定处理，bgm的更新则由songFlag控制(True代表bgm该更换了），并且在restartStage()中进行处理。

```python
def restartStage():
    global songFlag
...
    if(stage == 0 and songFlag):
        sounds.victory.stop()
        sounds.running.stop()
        sounds.forest.stop()
        sounds.escape.stop()
        sounds.boss.stop()
        sounds.forest.play(-1)
        songFlag = False
 ...
```

---
## 四、后续工作展望

该项目具备发展成一定规模项目的基础。我们根据组员和一部分玩家的游戏体验，认为该项目进一步开发的空间较大，基本设想如下：

1. 游戏关卡相比于市面上的闯关类游戏较少。因此项目完善的重要标准即是**关卡****与****地图****的****多样化实现。**
2. 游戏中，玩家操作仅限于“上，左，右”三个方向键，操作模式较为单一。可以加入“投掷、下滑”等操作，给玩家更丰富的游戏体验。
3. 游戏还可以采用**双人同时操作设置**。玩家1使用“WASD”四个按键作为方向键控制自己的人物移动，玩家2使用四个方向键使得自己的人物移动。双人协同合作通关。
4. 游戏在玩家主动退出时应能够提供**存档****功能**，待玩家再次挑战时可以读档继续上次的挑战。
5. 该游戏可以进一步开发为**剧情导向**，在闯关的同时逐步带入游戏剧情。
6. 游戏可以**设置不同难度**，让游戏小白和重度玩家都能有良好体验。

---
### 五、小组分工合作：

| 尤俊浩   | 关卡二、关卡三、游戏界面、游戏美化加工、游戏素材嵌入、代码整合、报告撰写   | 
|:----|:----|
| 黄彬   | 关卡二、海报制作、报告修改   | 
| 顾景佳   | 关卡一、海报制作、报告撰写、视频制作、素材收集   | 
| 柯旭洺   | 关卡四，游戏界面，游戏美化加工，素材收集，报告修改   | 

### 讨论截图：

![图片](https://uploader.shimo.im/f/u6bODKIHzsMYUipR.jpg!thumbnail)
![图片](https://uploader.shimo.im/f/INULpuwLyJfJQQ5h.jpg!thumbnail)
![图片](https://uploader.shimo.im/f/eCjp9A3vspb0e9sZ.jpg!thumbnail)
![图片](https://uploader.shimo.im/f/KvLvyx0ZZl67Ne9W.jpg!thumbnail)


