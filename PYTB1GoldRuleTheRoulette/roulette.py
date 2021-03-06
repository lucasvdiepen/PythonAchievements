import os
from enum import Enum
from pynput.keyboard import Key, Listener

clear = lambda: os.system('cls')

#os.system("color 27")

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Direction(Enum):
    UP = 0
    LEFT = 1
    RIGHT = 2
    DOWN = 3

#ANSI COLOR CODES
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLACK = '\u25A0'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BACKGROUNDRED = '\u001b[41;1m'
    BACKGROUNDBLUE = '\u001b[44m'
    BACKGROUNDBLACK = '\u001b[40m'
    BACKGROUNDGREEN = '\u001b[42m'

class PlaceColor(Enum):
    RED = 0
    BLACK = 1
    NONE = 2

class Place:
    text = ""
    color = PlaceColor.NONE
    money = 0
    multiplier = 0
    leftTop = 0
    rightCorner = 0
    def __init__(self, text, color, multiplier, leftTop, rightCorner):
        self.text = text
        self.color = color
        self.multiplier = multiplier
        self.leftTop = leftTop
        self.rightCorner = rightCorner

class Game:
    xLength = 60
    currentPosition = Position(5, 4)
    places = []

    table = [
        " ", " ", " ", " ", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", "|", "1st12", "", "", "", "", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", "2nd12", "", "", "", "", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", "3rd12", "", "", "", "", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ",
        "+", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "+",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "|", " ", " ", " ", "|", "3", " ", " ", "|", "6", " ", " ", "|", "9", " ", " ", "|", "12", "", " ", "|", "15", "", " ", "|", "18", "", " ", "|", "21", "", " ", "|", "24", "", " ", "|", "27", "", " ", "|", "30", "", " ", "|", "33", "", " ", "|", "36", "", " ", "|", "2to1", "", "", "", " ", " ", "|",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "|", " ", " ", " ", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "+",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "|", "0", " ", " ", "|", "2", " ", " ", "|", "5", " ", " ", "|", "8", " ", " ", "|", "11", "", " ", "|", "14", "", " ", "|", "17", "", " ", "|", "20", "", " ", "|", "23", "", " ", "|", "26", "", " ", "|", "29", "", " ", "|", "32", "", " ", "|", "35", "", " ", "|", "2to1 ", "", "", "", "", " ", "|",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "|", " ", " ", " ", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "+",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "|", " ", " ", " ", "|", "1", " ", " ", "|", "4", " ", " ", "|", "7", " ", " ", "|", "10", "", " ", "|", "13", "", " ", "|", "16", "", " ", "|", "19", "", " ", "|", "22", "", " ", "|", "25", "", " ", "|", "28", "", " ", "|", "31", "", " ", "|", "34", "", " ", "|", "2to1  ", "", "", "", "", "", "|",
        "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "|",
        "+", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "+",
        " ", " ", " ", " ", "|", "1to18", "", "", "", "", " ", " ", "|", "Even", "", "", "", " ", " ", " ", "|", "R", " ", " ", " ", " ", " ", " ", "|", "B", " ", " ", " ", " ", " ", " ", "|", "Odd", "", "", " ", " ", " ", " ", "|", "19to36", "", "", "", "", "", " ", "|", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", " ",
        " ", " ", " ", " ", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", "-", "-", "-", "-", "-", "-", "-", "+", " ", " ", " ", " ", " ", " ", " "

    ]

    def __init__(self):
        self.places.append(Place("3", PlaceColor.RED, 1, Position(5, 4), Position(7, 6)))
        self.places.append(Place("6", PlaceColor.BLACK, 1, Position(9, 4), Position(11, 6)))
        self.places.append(Place("9", PlaceColor.RED, 1, Position(13, 4), Position(15, 6)))
        self.places.append(Place("12", PlaceColor.RED, 1, Position(17, 4), Position(19, 6)))
        self.places.append(Place("15", PlaceColor.BLACK, 1, Position(21, 4), Position(23, 6)))
        self.places.append(Place("18", PlaceColor.RED, 1, Position(25, 4), Position(27, 6)))
        self.places.append(Place("21", PlaceColor.RED, 1, Position(29, 4), Position(31, 6)))
        self.places.append(Place("24", PlaceColor.BLACK, 1, Position(33, 4), Position(35, 6)))
        self.places.append(Place("27", PlaceColor.RED, 1, Position(37, 4), Position(39, 6)))
        self.places.append(Place("30", PlaceColor.RED, 1, Position(41, 4), Position(43, 6)))
        self.places.append(Place("33", PlaceColor.BLACK, 1, Position(45, 4), Position(47, 6)))
        self.places.append(Place("36", PlaceColor.RED, 1, Position(49, 4), Position(51, 6)))
        #
        self.places.append(Place("2", PlaceColor.BLACK, 1, Position(5, 8), Position(7, 10)))
        self.places.append(Place("5", PlaceColor.RED, 1, Position(9, 8), Position(11, 10)))
        self.places.append(Place("8", PlaceColor.BLACK, 1, Position(13, 8), Position(15, 10)))
        self.places.append(Place("11", PlaceColor.BLACK, 1, Position(17, 8), Position(19, 10)))
        self.places.append(Place("14", PlaceColor.RED, 1, Position(21, 8), Position(23, 10)))
        self.places.append(Place("17", PlaceColor.BLACK, 1, Position(25, 8), Position(27, 10)))
        self.places.append(Place("20", PlaceColor.BLACK, 1, Position(29, 8), Position(31, 10)))
        self.places.append(Place("23", PlaceColor.RED, 1, Position(33, 8), Position(35, 10)))
        self.places.append(Place("26", PlaceColor.BLACK, 1, Position(37, 8), Position(39, 10)))
        self.places.append(Place("29", PlaceColor.BLACK, 1, Position(41, 8), Position(43, 10)))
        self.places.append(Place("32", PlaceColor.RED, 1, Position(45, 8), Position(47, 10)))
        self.places.append(Place("35", PlaceColor.BLACK, 1, Position(49, 8), Position(51, 10)))
        #
        self.places.append(Place("1", PlaceColor.RED, 1, Position(5, 12), Position(7, 14)))
        self.places.append(Place("4", PlaceColor.BLACK, 1, Position(9, 12), Position(11, 14)))
        self.places.append(Place("7", PlaceColor.RED, 1, Position(13, 12), Position(15, 14)))
        self.places.append(Place("10", PlaceColor.BLACK, 1, Position(17, 12), Position(19, 14)))
        self.places.append(Place("13", PlaceColor.BLACK, 1, Position(21, 12), Position(23, 14)))
        self.places.append(Place("16", PlaceColor.RED, 1, Position(25, 12), Position(27, 14)))
        self.places.append(Place("19", PlaceColor.RED, 1, Position(29, 12), Position(31, 14)))
        self.places.append(Place("22", PlaceColor.BLACK, 1, Position(33, 12), Position(35, 14)))
        self.places.append(Place("25", PlaceColor.RED, 1, Position(37, 12), Position(39, 14)))
        self.places.append(Place("28", PlaceColor.BLACK, 1, Position(41, 12), Position(43, 14)))
        self.places.append(Place("31", PlaceColor.BLACK, 1, Position(45, 12), Position(47, 14)))
        self.places.append(Place("34", PlaceColor.RED, 1, Position(49, 12), Position(51, 14)))

    """    
    def FindCoordinatesByIndex(self, index):
        y = index / self.xLength
        x = index - y
        return Position(x, y)
    """

    def FindIndexByCoordinates(self, position):
        index = position.y * self.xLength
        index += position.x
        return index

    def GetChar(self, position):
        return self.table[self.FindIndexByCoordinates(position)]

    def ChangeChar(self, position, char):
        self.table[self.FindIndexByCoordinates(position)] = char

    def GetPlaceByPosition(self, position):
        for place in self.places:
            if(place.leftTop.x <= position.x and place.leftTop.y <= position.y):
                if(place.rightCorner.x >= position.x and place.rightCorner.y >= position.y):
                    return place

    def GetPlaceByText(self, text):
        for place in self.places:
            if(place.text == text):
                return place

    def Move(self, x, y):
        nextIsInBlock = False
        nextPosition = self.currentPosition
        while True:
            nextPosition = Position((nextPosition.x + x), (nextPosition.y + y))
            if(nextIsInBlock):
                newPlace = self.GetPlaceByPosition(nextPosition)
                if(newPlace is None):
                    #dead end
                    pass
                else:
                    #print(newPlace.text)
                    self.currentPosition = nextPosition
                    self.UpdateScreen()

                break
            
            if(self.GetChar(nextPosition) == "|" or self.GetChar(nextPosition) == "-"):
                #go to left top and right corner to get all coordinates between
                nextIsInBlock = True

    def UpdateScreen(self):
        lines = ""

        #set current selected position coordinates in a array
        place = game.GetPlaceByPosition(game.currentPosition)
        selectedIndexes = []
        nextX = place.leftTop.x
        nextY = place.leftTop.y
        while True:
            selectedIndexes.append(game.FindIndexByCoordinates(Position(nextX, nextY)))
            if(nextX == place.rightCorner.x and nextY == place.rightCorner.y):
                break
            nextX += 1
            if(nextX > place.rightCorner.x):
                nextX = place.leftTop.x
                nextY += 1

        for i in range(len(self.table)):
            if(i % self.xLength == 0):
                if(not i == 0):
                    lines += "\n"

            char = self.table[i]
            fullChar = ""
            endCount = 0
            if(i in selectedIndexes):
                if(char != "" and char != " " and char != "-" and char != "+" and char != "|"):
                    place = game.GetPlaceByText(char)
                    if(place.color == PlaceColor.RED):
                        char = bcolors.BACKGROUNDRED + char + bcolors.END
                    if(place.color == PlaceColor.BLACK):
                        char = bcolors.BACKGROUNDBLACK + char + bcolors.END
                        
                char = bcolors.BACKGROUNDBLUE + char + bcolors.END
                endCount += 1

            if(char != "" and char != " " and char != "-" and char != "+" and char != "|"):
                pass
            else:
                char = bcolors.BACKGROUNDGREEN + char + bcolors.END
            
            if(char.isdigit() and char != "0"):
                place = game.GetPlaceByText(char)
                if(place.color == PlaceColor.RED):
                    char = bcolors.BACKGROUNDRED + char + bcolors.END
                if(place.color == PlaceColor.BLACK):
                    char = bcolors.BACKGROUNDBLACK + char + bcolors.END

            
            """place = self.GetPlaceByText(char)
            if(not place is None):
                if(place.color == PlaceColor.RED):
                    char = bcolors.RED + char + bcolors.END

                elif(place.color == PlaceColor.BLACK):
                    char = bcolors.BLACK + char + bcolors.END
            """
            lines += char

        clear()
        print (lines)

game = Game()

game.UpdateScreen()

MoveKeyDown = None

def on_press(key):
    global MoveKeyDown
    if(MoveKeyDown is None):
        if(key == Key.right):
            MoveKeyDown = key
            game.Move(1, 0)
        elif(key == Key.left):
            MoveKeyDown = key
            game.Move(-1, 0)
        elif(key == Key.up):
            MoveKeyDown = key
            game.Move(0, -1)
        elif(key == Key.down):
            MoveKeyDown = key
            game.Move(0, 1)

def on_release(key):
    global MoveKeyDown
    if(key == MoveKeyDown):
        MoveKeyDown = None
        UpdateScreen = True

listener = Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

#print(bcolors.BACKGROUNDRED + "test" + bcolors.END)

#input()

while True:
    pass
