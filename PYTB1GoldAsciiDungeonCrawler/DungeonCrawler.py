import os
import sys
import time
try:
    from pynput.keyboard import Key, Listener
except ModuleNotFoundError:
    print("pynput module is missing. Please install the pynput library.")
    input("Press enter to continue")
    exit()

try:
    from playsound import playsound
except ModuleNotFoundError:
    print("playsound module is missing. Please install the playsound library.")
    input("Press enter to continue")
    exit()

import queue
import random
clear = lambda: os.system('cls')

currentPath = os.getcwd()

attackSoundEffect = currentPath + "\\SoundEffects\\soundeffect2.wav"
killSoundEffect = currentPath + "\\SoundEffects\\soundeffect1.mp3"

gameOverArt = """  ________                         ________
 /  _____/_____    _____   ____    \_____  \___  __ ___________
/   \  ___\__  \  /     \_/ __ \    /   |   \  \/ // __ \_  __ \\
\    \_\  \/ __ \|  Y Y  \  ___/   /    |    \   /\  ___/|  | \/
 \______  (____  /__|_|  /\___  >  \_______  /\_/  \___  >__|
        \/     \/      \/     \/           \/          \/"""

gameWonArt = """_____.___.                __      __              
\__  |   | ____  __ __   /  \    /  \____   ____  
 /   |   |/  _ \|  |  \  \   \/\/   /  _ \ /    \ 
 \____   (  <_> )  |  /   \        (  <_> )   |  \\
 / ______|\____/|____/     \__/\  / \____/|___|  /
 \/                             \/             \/ """

asciiArt = """                   (    )
                  ((((()))
                  |o\ /o)|
                  ( (  _')
                   (._.  /\__
                  ,\___,/ '  ')
    '.,_,,       (  .- .   .    )
     \   \\     ( '        )(    )
      \   \\    \.  _.__ ____( .  |
       \  /\\   .(   .'  /\  '.  )
        \(  \\.-' ( /    \/    \)
         '  ()) _'.-|/\/\/\/\/\|
             '\\ .( |\/\/\/\/\/|
               '((  \    /\    /
               ((((  '.__\/__.')
                ((,) /   ((()   )
                 "..-,  (()("   /
                  _//.   ((() ."
          _____ //,/" ___ ((( ', ___
                           ((  )
                            / /
                          _/,/'
                        /,/,"
"""

AttackDelay = 1000 # in milliseconds
EnemyAttackDelay = 2000 # in milliseconds

callback_queue = queue.Queue()

userInput = ""

MoveKeyDown = None

class bcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class HealthItem():
    def __init__(self, giveHealth, position):
        self.giveHealth = giveHealth
        self.position = position

class Player():
    health = 20
    position = Position(2, 5)
    canMove = True
    cantMoveStartTime = 0
    minDamage = 2
    maxDamage = 8

    def Damage(self, damage):
        self.health -= damage
        if(self.health <= 0):
            #You are dead. Game over
            game.Won = False
            game.Started = False

    def Move(self, x, y):
        newPosition = Position(self.position.x + x, self.position.y + y)
        charOnNewPosition = game.map.GetChar(newPosition)
        if(charOnNewPosition == "#" or charOnNewPosition == "*"):
            #cant move
            pass
        elif(charOnNewPosition == "x"):
            #enemy
            try:
                enemy = game.GetEnemy(newPosition)#crashes sometimes because enemy move away
                game.Attack(enemy)
            except Exception:
                pass
            
        elif(charOnNewPosition == "@"):
            #victory
            game.Won = True
            game.Started = False
        else:
            if(charOnNewPosition == "$"):
                #healthItem
                healthItem = game.GetHealthItem(newPosition)
                self.health += healthItem.giveHealth
                game.RemoveHealthItem(healthItem.position)

            game.map.ChangeChar(self.position, " ")
            game.map.ChangeChar(newPosition, "+")
            self.position = newPosition

class Enemy():
    health = 10
    position = Position(9, 5)
    path = [] #the position the enemy needs to walk
    pathCount = 0
    walkDelay = 500 # is in milliseconds
    lastPathChange = 0 #ms time
    canMove = True
    Dead = False
    minDamage = 2
    maxDamage = 8
    cantMoveStartTime = 0

    def __init__(self, health, position, walkDelay, minDamage, maxDamage, path):
        self.health = health
        self.position = position
        self.path = path
        self.walkDelay = walkDelay
        self.minDamage = minDamage
        self.maxDamage = maxDamage
    
    def MovePath(self):
        newPosition = Position(self.position.x + self.path[self.pathCount].x, self.position.y + self.path[self.pathCount].y)
        charOnNewPosition = game.map.GetChar(newPosition)
        if(charOnNewPosition == "#" or charOnNewPosition == "*" or charOnNewPosition == "$"):
            #cant move
            pass
        if(charOnNewPosition == "+"):
            #enemy on player
            game.Attack(self)            
        else:
            game.map.ChangeChar(self.position, " ")
            game.map.ChangeChar(newPosition, "x")
            self.position = newPosition
            self.pathCount += 1
            if(self.pathCount >= len(self.path)):
                self.pathCount = 0

    def Damage(self, damage):
        self.health -= damage
        if(self.health <= 0):
            #enemy dead
            #game.RemoveEnemy(self.position)
            self.Dead = True

class Map():
    xLength = 0
    yLength = 0
    map = []

    def Setup(self):
        self.xLength = 28
        self.yLength = 25
        self.map = [
        "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "@", " ", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", "#", "#", "#", "#", "#", " ", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", "#", "#", "#", " ", " ", "#", "#", "#", "#",
        " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ",
        " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ",
        " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ",
        " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ",
        " ", " ", " ", " ", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", "#", " ", " ", " ",
        "#", "#", "#", "#", "#", "#", " ", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", "#", "#", "#", " ", " ", "#", "#", "#", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", "#", "#", "#", " ", "#", " ", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", "#", "#", "#", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", " ", " ", " ", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"
    ]

    def __init__(self, player, enemies, healthItems):
        self.Setup()
        #Set position of player and enemies in map
        self.ChangeChar(player.position, "+")

        #add all enemies
        for enemy in enemies:
            self.ChangeChar(enemy.position, "x")

        for healthItem in healthItems:
            self.ChangeChar(healthItem.position, "$")

    def FindIndexByCoordinates(self, position):
        index = position.y * self.xLength
        index += position.x
        return index

    def GetChar(self, position):
        return self.map[self.FindIndexByCoordinates(position)]

    def ChangeChar(self, position, char):
        self.map[self.FindIndexByCoordinates(position)] = char

    def GetMap(self):
        return self.map

class Game():
    player = None
    enemies = []
    healthItems = []
    map = None
    Started = False
    Won = False

    def __init__(self):
        self.Setup()

    def Setup(self):
        self.player = Player()
        self.enemies.append(Enemy(10, Position(12, 3), 500, 2, 8, [Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0)]))
        self.enemies.append(Enemy(10, Position(18, 4), 500, 2, 8, [Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0)]))
        self.enemies.append(Enemy(10, Position(12, 5), 500, 2, 8, [Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0)]))
        self.enemies.append(Enemy(10, Position(18, 6), 500, 2, 8, [Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0), Position(1, 0)]))
        self.enemies.append(Enemy(10, Position(10, 17), 500, 5, 13, [Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, 1), Position(1, 0), Position(1, 0), Position(1, 0), Position(0, -1), Position(0, -1), Position(0, -1), Position(0, -1)]))
        self.enemies.append(Enemy(10, Position(23, 13), 500, 2, 8, [Position(0, -1), Position(0, -1), Position(0, -1), Position(0, -1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, 1)]))
        self.enemies.append(Enemy(10, Position(22, 9), 500, 2, 8, [Position(0, 1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, -1), Position(0, -1), Position(0, -1), Position(0, -1)]))
        self.enemies.append(Enemy(10, Position(6, 12), 500, 2, 8, []))
        self.enemies.append(Enemy(1, Position(4, 22), 500, 1, 1, []))
        self.healthItems.append(HealthItem(10, Position(4, 4)))
        self.healthItems.append(HealthItem(10, Position(1, 23)))
        self.map = Map(self.player, self.enemies, self.healthItems)

    def Reset(self):
        self.player = None
        self.enemies = []
        self.healthItems = []
        self.map = None
        self.Started = False
        self.Won = False
        self.Setup()

    def GetEnemy(self, position):
        for enemy in self.enemies:
            if(enemy.position.x == position.x and enemy.position.y == position.y):
                return enemy

    def Attack(self, enemy):
        try:
            playsound(attackSoundEffect, False)
        except Exception:
            pass
        game.player.Damage(random.randint(enemy.minDamage, enemy.maxDamage))
        enemy.Damage(random.randint(game.player.minDamage, game.player.maxDamage))
        enemy.canMove = False
        game.player.canMove = False
        timeNow = time.time() * 1000
        enemy.cantMoveStartTime = timeNow
        game.player.cantMoveStartTime = timeNow
        game.map.ChangeChar(enemy.position, "*")
        game.map.ChangeChar(game.player.position, "-")

    def GetHealthItem(self, position):
        for healthItem in self.healthItems:
            if(healthItem.position.x == position.x and healthItem.position.y == position.y):
                return healthItem

    def RemoveEnemy(self, position):
        for i in range(len(self.enemies)):
            if(self.enemies[i].position.x == position.x and self.enemies[i].position.y == position.y):
                self.map.ChangeChar(self.enemies[i].position, " ")
                self.enemies.pop(i)
                #kill sound effect
                try:
                    playsound(killSoundEffect, False)
                except Exception:
                    pass
                self.UpdateScreen()
                break

    def RemoveHealthItem(self, position):
        global UpdateScreen
        for i in range(len(self.healthItems)):
            if(self.healthItems[i].position.x == position.x and self.healthItems[i].position.y == position.y):
                self.map.ChangeChar(self.healthItems[i].position, " ")
                self.healthItems.pop(i)
                UpdateScreen = True
                break

    def UpdateScreen(self):
        if(game.Started):
            currentMap = self.map.GetMap()
            clear()
            lines = ""
            for i in range(len(currentMap)):
                
                if(i % self.map.xLength == 0):
                    #print("")
                    if(not i == 0):
                        lines += "\n"

                char = currentMap[i]
                if(char == "+" or char == "-"):
                    char = bcolors.GREEN + char + bcolors.ENDC
                elif(char == "x" or char == "*"):
                    char = bcolors.RED + char + bcolors.ENDC

                lines += char + " "
                
                """
                if(i % self.map.xLength == 0):
                    print("")
                
                char = currentMap[i]
                if(char == "+"):
                    char = bcolors.GREEN + char + bcolors.ENDC
                elif(char == "x" or char == "*"):
                    char = bcolors.RED + char + bcolors.ENDC
                sys.stdout.write(char + " ")
                sys.stdout.flush()
            """

            print(lines)

            print("\nHealth: " + str(game.player.health))

            print("\n" + str(userInput))

def MoveEnemies():
    global UpdateScreen
    timeNow = time.time() * 1000
    for i in range(len(game.enemies) - 1, -1, -1):
        enemy = game.enemies[i]
        if(enemy.canMove):
            if(len(enemy.path) > 0):
                if(timeNow > (enemy.lastPathChange + enemy.walkDelay)):
                    enemy.lastPathChange = timeNow
                    enemy.MovePath()
                    UpdateScreen = True
        else:
            if(timeNow > (enemy.cantMoveStartTime + EnemyAttackDelay)):
                enemy.canMove = True
                if(enemy.Dead):
                    game.map.ChangeChar(enemy.position, " ")
                    game.RemoveEnemy(enemy.position)
                else:
                    game.map.ChangeChar(enemy.position, "x")
                UpdateScreen = True

    if(not game.player.canMove):
        if(timeNow > (game.player.cantMoveStartTime + AttackDelay)):
            game.map.ChangeChar(game.player.position, "+")
            game.player.canMove = True
            UpdateScreen = True

def RunCommand(command):
    if(command.lower().strip() == "exit" or command.lower().strip() == "quit"):
        os._exit(0)
    elif(command.lower().strip() == "pos"):
        game.player.health = int(str(game.player.position.x) + "" + str(game.player.position.y))

def on_press(key):
    global UpdateScreen
    global MoveKeyDown
    global userInput
    global UpdateScreenEnd
    global UpdateScreenStart
    #print('{0} pressed'.format(key))

    if(key == Key.enter):
        RunCommand(userInput)
        userInput = ""
        UpdateScreen = True
        UpdateScreenEnd = True
        UpdateScreenStart = True
    elif(key == Key.backspace):
        userInput = userInput[:-1]
        UpdateScreen = True
        UpdateScreenEnd = True
        UpdateScreenStart = True
    elif(key == Key.space):
        if(game.Started):
            userInput += " "
        else:
            game.Reset()
            game.Started = True
            
        UpdateScreen = True
    try:
        userInput += str(key.char)
        UpdateScreen = True
        UpdateScreenEnd = True
        UpdateScreenStart = True
    except Exception:
        pass

    if(MoveKeyDown is None):
        if(game.player.canMove):
            if(key == Key.right):
                MoveKeyDown = key
                game.player.Move(1, 0)
                #callback_queue.put(lambda: game.player.Move(1, 0))
                UpdateScreen = True
            elif(key == Key.left):
                MoveKeyDown = key
                game.player.Move(-1, 0)
                #callback_queue.put(lambda: game.player.Move(-1, 0))
                UpdateScreen = True
            elif(key == Key.up):
                MoveKeyDown = key
                game.player.Move(0, -1)
                #callback_queue.put(lambda: game.player.Move(0, -1))
                UpdateScreen = True
            elif(key == Key.down):
                MoveKeyDown = key
                game.player.Move(0, 1)
                #callback_queue.put(lambda: game.player.Move(0, 1))
                UpdateScreen = True
            

def on_release(key):
    global UpdateScreen
    global MoveKeyDown
    if(key == MoveKeyDown):
        MoveKeyDown = None
        UpdateScreen = True

game = Game()

UpdateScreen = False
UpdateScreenEnd = False
UpdateScreenStart = False

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

updateDelay = 300 #in milliseconds
lastUpdate = -2000
onoff = False

while not game.Started: 
    timeNow = time.time() * 1000
    if(timeNow > (lastUpdate + updateDelay)):
        UpdateScreenStart = True
        onoff = not onoff
        lastUpdate = timeNow

    if(UpdateScreenStart):
        UpdateScreenStart = False
        clear()
        print (asciiArt)
        if(not onoff):
            print("Press SPACE to play")
        else:
            print("")

        print("\n" + userInput)
            

while True:
    if(game.Started):
        """
        try:
            callback = callback_queue.get(False)
            callback()
        except queue.Empty:
            pass
        """

        MoveEnemies()
        if(UpdateScreen):
            game.UpdateScreen()
            UpdateScreen = False
    else:
        #displayEndScreen
        timeNow = time.time() * 1000
        if(timeNow > (lastUpdate + updateDelay)):
            UpdateScreenEnd = True
            onoff = not onoff
            lastUpdate = timeNow

        if(UpdateScreenEnd):
            UpdateScreenEnd = False
            clear()
            if(game.Won):
                print(gameWonArt)
            else:
                print(gameOverArt)
            
            if(not onoff):
                print("\nPress SPACE to play again")
            else:
                print("\n")
            
            print("\n" + userInput)

input("Press enter to exit")