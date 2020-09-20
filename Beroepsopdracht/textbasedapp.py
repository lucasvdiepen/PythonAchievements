class Item:
    def __init__(self, name, description, pickable, tags):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.tags = tags

class Room:
    def __init__(self, name, description, items, roomDirections):
        self.name = name
        self.description = description
        self.items = items
        self.roomDirections = roomDirections #make this a dictionary

class Command:
    def __init__(self, function, args, expectedArgs, followUp):
        self.function = function
        self.args = args
        self.expectedArgs = expectedArgs
        self.followUp = followUp

#Setup process

rooms = []
rooms.append(Room("Test Room", "This is a wonderfull test room", [Item("Magic wand", "This is a good looking wand.", True, ["WAND"])], {"n": "Other Room"}))#test room
rooms.append(Room("Other Room", "This is the other room with magical stones", [Item("Stone", "This is a just normal stone. It might be usefull against enemies.", True, ["ROCK", "STONES"])], {"s": "Test Room"}))#test room

currentRoom = "Test Room"

commands = {
    "n,north": Command("GoDirection", "n", 0, None),
    "w,west": Command("GoDirection", "w", 0, None),
    "e,east": Command("GoDirection", "e", 0, None),
    "s,south": Command("GoDirection", "s", 0, None),
    "pick,pickup": Command("Pick", None, -1, "What do you want to pick up?"),
    "walk,run": Command("Walk", None, 1, "Which direction do you want to go?"),
    "x,examine": Command("Examine", None, -1, "What do you want to examine?")
}

inventory = []

#Command Functions

def FollowUp(args, command):
    if(len(args) <= 0):
        AskFollowUp(command)
        return False
    
    return True

def Examine(args):
    if(len(args) <= 0):
        AskFollowUp("examine")
    else:
        item = GetItem(args)
        if(item is None):
            pass
        else:
            print(item.description)

def GoDirection(args):
    global currentRoom
    roomDetails = GetRoom(currentRoom)
    roomToGo = ""
    if(args[0] in roomDetails.roomDirections):
        roomToGo = roomDetails.roomDirections[args[0]]
    if(roomToGo is None or roomToGo == ""):
        print("You can't go there")
    else:
        #go to new room
        newRoom = GetRoom(roomToGo)
        if(newRoom is None):
            print("[Error: Room doesn't exists]")
        else:
            currentRoom = newRoom.name
            print(newRoom.name)
            print(newRoom.description)

def Walk(args):
    if(len(args) <= 0):
        AskFollowUp("walk")
    else:
        arg = args[0].upper()
        allowedList = ["N", "NORTH", "W", "WEST", "E", "EAST", "S", "SOUTH"]
        if(arg in allowedList):
            GoDirection([arg.lower()[0]])
        else:
            print("Don't know what you mean")


def Pick(args):
    if(len(args) <= 0):
        #Follow up question should happen here
        AskFollowUp("pick")
    else:
        item = GetItem(args)
        if (item is None):
            pass
        else:
            if(item.pickable):
                PickUpItem(item.name)
            else:
                print("You can't pick this item")

def GetItem(args):
    roomDetails = GetRoom(currentRoom)
    #Check full name
    fullArgs = " ".join([str(arg) for arg in args])
    for item in roomDetails.items:
        if(item.name.upper() == fullArgs.upper()):
            #found item in full name
            return item
    
    #Check tags
    for item in roomDetails.items:
        for arg in args:
            if(arg.upper() in item.tags):
                #found item in tag
                return item

    print("Couldn't find that item")

def PickUpItem(name):
    for roomDetails in rooms:
        if(roomDetails.name == currentRoom):
            for itemIndex in range(len(roomDetails.items)):
                if(roomDetails.items[itemIndex].name == name):
                    inventory.append(roomDetails.items[itemIndex])
                    print("You picked up: " + roomDetails.items[itemIndex].name)
                    roomDetails.items.pop(itemIndex)

def GetRoom(name):
    for room in rooms:
        if(name == room.name):
            return room

def RunCommand(command):
    globals()[command.function](command.args)

def GetCommand(playerCommand):
    for key in commands:
        commandList = key.split(",")
        for command in commandList:
            if(command.upper() == playerCommand.upper()):
                #command found
                return commands[key]

def AskCommand():
    playerInput = input("> ")
    if(len(playerInput) <= 0):
        print("No input")
    else:
        inputInList = playerInput.split(" ")
        command = GetCommand(inputInList[0])
        if(command is None):
            print("Command not found")
        else:
            argsCount = len(inputInList) - 1
            if(command.expectedArgs == 0):
                if(argsCount > 0):
                    print("Don't know what you mean")
                else:
                    RunCommand(command)
            elif(command.expectedArgs == -1):
                    #no limit for arguments, so send all arguments
                    RunCommand(Command(command.function, inputInList[1:len(inputInList)], command.expectedArgs, command.followUp))
            else:
                if(command.expectedArgs == argsCount):
                    RunCommand(Command(command.function, inputInList[1:len(inputInList)], command.expectedArgs, command.followUp))
                elif(argsCount < command.expectedArgs and argsCount >= 0):
                    AskFollowUp(inputInList[0])
                elif(argsCount > command.expectedArgs):
                    print("Don't know what you mean")

def AskFollowUp(basecommand):
    commandDetails = GetCommand(basecommand)
    print(commandDetails.followUp)
    playerInput = input("> ")
    inputInList = playerInput.split(" ")
    argsCount = len(inputInList)
    if(commandDetails.expectedArgs == -1):
        RunCommand(Command(commandDetails.function, inputInList, commandDetails.expectedArgs, commandDetails.followUp))
    else:
        if(commandDetails.expectedArgs == argsCount):
            RunCommand(Command(commandDetails.function, inputInList, commandDetails.expectedArgs, commandDetails.followUp))
        else:
            print("Don't know what you mean")

#Command loop
while True:
    AskCommand()