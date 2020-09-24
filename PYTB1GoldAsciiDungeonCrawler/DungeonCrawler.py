import os
import sys
import time
from pynput.keyboard import Key, Listener
import queue
clear = lambda: os.system('cls')

AttackDelay = 1500 # in milliseconds
EnemyAttackDelay = 2500

callback_queue = queue.Queue()

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
    health = 5
    position = Position(2, 5)
    canMove = True

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
            enemy = game.GetEnemy(newPosition)
            enemy.canMove = False
            self.canMove = False
            enemy.Damage(2)
            game.map.ChangeChar(enemy.position, "*")
            game.cantMoveStartTime = time.time() * 1000
        else:
            game.map.ChangeChar(self.position, " ")
            game.map.ChangeChar(newPosition, "+")
            self.position = newPosition

class Enemy():
    health = 5
    position = Position(9, 5)
    path = [Position(0, -1), Position(0, -1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, 1), Position(0, -1), Position(0, -1)] #the position the enemy needs to walk
    pathCount = 0
    walkDelay = 500 # is in miliseconds
    lastPathChange = 0 #ms time
    canMove = True
    
    def MovePath(self):
        newPosition = Position(self.position.x + self.path[self.pathCount].x, self.position.y + self.path[self.pathCount].y)
        charOnNewPosition = game.map.GetChar(newPosition)
        if(charOnNewPosition == "#" or charOnNewPosition == "*"):
            #cant move
            pass
        if(charOnNewPosition == "+"):
            #enemy on player
            game.player.Damage(2)
            self.canMove = False
            game.player.canMove = False
            game.cantMoveStartTime = time.time() * 1000
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
            game.RemoveEnemy(self.position)

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
    enemies = [Enemy()]
    map = Map(player, enemies)

    cantMoveStartTime = 0

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


    def UpdateScreen(self):
        self.currentMap = self.map.GetMap()
        clear()
        for i in range(len(self.currentMap)):
            if(i % self.map.xLength == 0):
                print("")
            
            char = self.currentMap[i]
            if(char == "+"):
                char = bcolors.OKGREEN + char + bcolors.ENDC
            elif(char == "x"):
                char = bcolors.FAIL + char + bcolors.ENDC
            sys.stdout.write(char + " ")
            sys.stdout.flush()

        print("\n")


game = Game()
game.UpdateScreen()

UpdateScreen = False

def MoveEnemies():
    global UpdateScreen
    timeNow = time.time() * 1000
    for enemy in game.enemies:
        if(enemy.canMove):
            if(timeNow > (enemy.lastPathChange + enemy.walkDelay)):
                enemy.lastPathChange = timeNow
                enemy.MovePath()
                UpdateScreen = True
    
    if(timeNow > (game.cantMoveStartTime + EnemyAttackDelay)):
        for enemy in game.enemies:
            if(not enemy.canMove):
                game.map.ChangeChar(enemy.position, "x")
                enemy.canMove = True
                UpdateScreen = True

    if(timeNow > (game.cantMoveStartTime + AttackDelay)):
        game.player.canMove = True

def on_press(key):
    global UpdateScreen
    #print('{0} pressed'.format(key))
    if(game.player.canMove):
        if(key == Key.right):
            game.player.Move(1, 0)
            #callback_queue.put(lambda: game.player.Move(1, 0))
            UpdateScreen = True
        elif(key == Key.left):
            game.player.Move(-1, 0)
            #callback_queue.put(lambda: game.player.Move(-1, 0))
            UpdateScreen = True
        elif(key == Key.up):
            game.player.Move(0, -1)
            #callback_queue.put(lambda: game.player.Move(0, -1))
            UpdateScreen = True
        elif(key == Key.down):
            game.player.Move(0, 1)
            #callback_queue.put(lambda: game.player.Move(0, 1))
            UpdateScreen = True

def on_release(key):
    pass

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
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

input("Press enter to continue")