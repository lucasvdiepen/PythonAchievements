import os
import sys
import time
from pynput.keyboard import Key, Listener
import queue
import random
clear = lambda: os.system('cls')

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
            pils  _//.   ((() ."
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
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
            print("Dead. Game over should happen here")

    def Move(self, x, y):
        newPosition = Position(self.position.x + x, self.position.y + y)
        charOnNewPosition = game.map.GetChar(newPosition)
        if(charOnNewPosition == "#" or charOnNewPosition == "*"):
            #cant move
            pass
        elif(charOnNewPosition == "x"):
            #enemy
            enemy = game.GetEnemy(newPosition)#crashes sometimes because enemy move away
            enemy.canMove = False
            self.canMove = False
            self.Damage(random.randint(enemy.minDamage, enemy.maxDamage))
            enemy.Damage(random.randint(self.minDamage, self.maxDamage))
            game.map.ChangeChar(enemy.position, "*")
            timeNow = time.time() * 1000
            enemy.cantMoveStartTime = timeNow
            game.player.cantMoveStartTime = timeNow
        else:
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

    def __init__(self, health, position, path, walkDelay, minDamage, maxDamage):
        self.health = health
        self.position = position
        self.path = path
        self.walkDelay = walkDelay
        self.minDamage = minDamage
        self.maxDamage = maxDamage
    
    def MovePath(self):
        newPosition = Position(self.position.x + self.path[self.pathCount].x, self.position.y + self.path[self.pathCount].y)
        charOnNewPosition = game.map.GetChar(newPosition)
        if(charOnNewPosition == "#" or charOnNewPosition == "*"):
            #cant move
            pass
        if(charOnNewPosition == "+"):
            #enemy on player
            game.player.Damage(random.randint(self.minDamage, self.maxDamage))
            self.Damage(random.randint(game.player.minDamage, game.player.maxDamage))
            self.canMove = False
            game.player.canMove = False
            timeNow = time.time() * 1000
            self.cantMoveStartTime = timeNow
            game.player.cantMoveStartTime = timeNow
            game.map.ChangeChar(self.position, "*")
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
    xLength = 17
    yLength = 10

    map = [
        "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#",
        "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"
    ]

    def __init__(self, player, enemies):
        #Set position of player and enemies in map
        self.ChangeChar(player.position, "+")

        #add all enemies
        for enemy in enemies:
            self.ChangeChar(enemy.position, "x")

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
    player = Player()
    enemies = []
    map = Map(player, enemies)
    Started = False

    def __init__(self):
        self.enemies.append(Enemy(10, Position(9, 5), [Position(0, -1), Position(0, -1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, -1), Position(0, -1)], 500, 2, 8))
        self.enemies.append(Enemy(10, Position(15, 2), [Position(-1, 0), Position(-1, 0), Position(-1, 0), Position(1, 0), Position(1, 0), Position(1, 0)], 500, 2, 8))

    def GetEnemy(self, position):
        for enemy in self.enemies:
            if(enemy.position.x == position.x and enemy.position.y == position.y):
                return enemy

    def RemoveEnemy(self, position):
        for i in range(len(self.enemies)):
            if(self.enemies[i].position.x == position.x and self.enemies[i].position.y == position.y):
                self.map.ChangeChar(self.enemies[i].position, " ")
                self.enemies.pop(i)
                self.UpdateScreen()
                break


    def UpdateScreen(self):
        self.currentMap = self.map.GetMap()
        clear()
        for i in range(len(self.currentMap)):
            if(i % self.map.xLength == 0):
                print("")
            
            char = self.currentMap[i]
            if(char == "+"):
                char = bcolors.OKGREEN + char + bcolors.ENDC
            elif(char == "x" or char == "*"):
                char = bcolors.FAIL + char + bcolors.ENDC
            sys.stdout.write(char + " ")
            sys.stdout.flush()

        print("\n\nHealth: " + str(game.player.health))

        print("\n" + str(userInput))

        print("")

def MoveEnemies():
    global UpdateScreen
    timeNow = time.time() * 1000
    for i in range(len(game.enemies) - 1, -1, -1):
        enemy = game.enemies[i]
        if(enemy.canMove):
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
            game.player.canMove = True

def RunCommand(command):
    if(command.lower().strip() == "exit" or command.lower().strip() == "quit"):
        os._exit(0)

def on_press(key):
    global UpdateScreen
    global MoveKeyDown
    global userInput
    #print('{0} pressed'.format(key))

    if(game.Started):
        if(key == Key.enter):
            RunCommand(userInput)
            userInput = ""
            UpdateScreen = True
        elif(key == Key.backspace):
            userInput = userInput[:-1]
            UpdateScreen = True
        elif(key == Key.space):
            userInput += " "
            UpdateScreen = True
        try:
            userInput += str(key.char)
            UpdateScreen = True
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
    else:
        if(key == Key.space):
            game.Started = True

def on_release(key):
    global UpdateScreen
    global MoveKeyDown
    if(key == MoveKeyDown):
        MoveKeyDown = None
        UpdateScreen = True

game = Game()

UpdateScreen = False

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
        clear()
        print (asciiArt)
        lastUpdate = timeNow
        if(onoff):
            onoff = False
        else: 
            onoff = True
            print("Press SPACE to play")

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

input("Press enter to exit")