from enum import Enum
import os
try:
    from playsound import playsound
except ModuleNotFoundError:
    print("Playsound module not found")

class SearchIn(Enum):
    Room = 0
    Inventory = 1
    RoomAndInventory = 2

class Item:
    def __init__(self, name, description, pickable, tags):
        self.name = name
        self.description = description
        self.pickable = pickable
        self.tags = tags

class Room:
    def __init__(self, name, description, items, npc, roomDirections):
        self.name = name
        self.description = description
        self.items = items
        self.npc = npc
        self.roomDirections = roomDirections

class NPC:
    def __init__(self, name, description, tags, wantItems, text):
        self.name = name
        self.description = description
        self.tags = tags
        self.wantItems = wantItems
        self.text = text

class Command:
    def __init__(self, function, args, expectedArgs, followUp):
        self.function = function
        self.args = args
        self.expectedArgs = expectedArgs
        self.followUp = followUp

class CommandResponse:
    def __init__(self, command, baseCommand):
        self.command = command
        self.baseCommand = baseCommand

#Setup process

BOLD = '\033[1m'
END = '\033[0m'

itemListTestRoom = [Item("Magic wand", "This is a good looking wand.", True, ["wand"])]
npcListTestRoom = [NPC("Guard", "Looks like a normal guard", [], {"Passport": "GuardGotPassport"}, "You need to give me your passport")]


rooms = []
rooms.append(Room("Test Room", "This is a wonderfull test room", itemListTestRoom, npcListTestRoom, {"n": "Other Room"}))#test room
rooms.append(Room("Other Room", "This is the other room with magical stones", [Item("Stone", "This is a just normal stone. It might be usefull against enemies.", True, ["ROCK", "STONES"])], [],  {"s": "Test Room"}))#test room

currentRoom = "Test Room"
objective = "There is no objective yet"

commands = {
    "n,north": Command("GoDirection", "n", 1, None),
    "w,west": Command("GoDirection", "w", 1, None),
    "e,east": Command("GoDirection", "e", 1, None),
    "s,south": Command("GoDirection", "s", 1, None),
    "up": Command("GoDirection", "u", 1, None),
    "down": Command("GoDirection", "d", 1, None),
    "pick up,pick,pickup": Command("Pick", None, -1, "What do you want to pick up?"),
    "walk to,run to,go to,walk,run,go": Command("Walk", None, 1, "Which direction do you want to go?"),
    "x,examine": Command("Examine", None, -1, "What do you want to examine?"),
    "look around,l,look": Command("Look", None, 0, None),
    "i,inventory": Command("Inventory", None, 0, None),
    "use": Command("Use", None, -1, "What do you want to use"),
    "drop": Command("Drop", None, -1, "What do you want to drop?"),
    "exit,quit": Command("Exit", None, 0, None),
    "give": Command("Give", None, -1, "What do you want to give?"),
    "objective,obj": Command("Objective", None, 0, None)
}

inventory = []

# NPC Functions

def GuardGotPassport():
    print("Thank you. This passport looks normal. You can pass")

#Command Functions

def FollowUp(args, command):
    if(len(args) <= 0):
        AskFollowUp(command)
        return False
    
    return True

def Objective(args):
    print("Objective:")
    print(objective)

def Give(args):
    if(FollowUp(args, "give")):
        item = GetItem(args, SearchIn.Inventory)
        if(item is None):
            pass
        else:
            pass

def Use(args):
    if(FollowUp(args, "use")):
        print("This command does not work yet")

def Exit(args):
    print("Do you want to quit? Y/N")
    while True:
        playerInput = input("> ")
        if(playerInput.upper() == "Y" or playerInput.upper() == "YES"):
            exit()
        elif(playerInput.upper() == "N" or playerInput.upper() == "NO"):
            break
        else:
            print("Choose between Y or N \n")

def Drop(args):
    if(FollowUp(args, "drop")):
        item = GetItem(args, SearchIn.Inventory)
        if(item is None):
            pass
        else:
            DropItem(item.name)

def DropItem(name):
    for itemIndex in range(len(inventory)):
        if(inventory[itemIndex].name == name):
            for roomDetails in rooms:
                if(roomDetails.name == currentRoom):
                    roomDetails.items.append(inventory[itemIndex])
            print("You dropped: " + inventory[itemIndex].name)
            inventory.pop(itemIndex)

def Inventory(args):
    fullInventory = "You have: "
    if(len(inventory) > 2):
        inv = inventory[0:(len(inventory) - 2)]
        fullInventory += ", ".join([str(itemName.name) for itemName in inv])
        fullInventory += " and " + inventory[len(inventory) - 1].name
    else:
        fullInventory  += " and ".join([str(itemName.name) for itemName in inventory])

    print(fullInventory)


def Look(args):
    roomDetails = GetRoom(currentRoom)
    print(BOLD + roomDetails.name + END)
    print(roomDetails.description)

def Examine(args):
    if(FollowUp(args, "examine")):
        item = GetItem(args, SearchIn.RoomAndInventory)
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
            print(BOLD + newRoom.name + END)
            print(newRoom.description)

def Walk(args):
    if(FollowUp(args, "walk")):
        arg = args[0].upper()
        allowedList = ["N", "NORTH", "W", "WEST", "E", "EAST", "S", "SOUTH", "UP", "DOWN"]
        if(arg in allowedList):
            GoDirection([arg.lower()[0]])
        else:
            print("Don't know what you mean")


def Pick(args):
    if(FollowUp(args, "pick")):
        item = GetItem(args, SearchIn.Room)
        if (item is None):
            pass
        else:
            if(item.pickable):
                PickUpItem(item.name)
            else:
                print("You can't pick this item")

def GetItem(args, searchIn):
    itemList = []
    if(searchIn == SearchIn.Room or searchIn == SearchIn.RoomAndInventory):
        roomDetails = GetRoom(currentRoom)
        itemList.append(roomDetails.items)
    
    if(searchIn == SearchIn.Inventory or searchIn == searchIn.RoomAndInventory):
        itemList.append(inventory)
    
    for items in itemList:
        #Check full name
        fullArgs = " ".join([str(arg) for arg in args])
        for item in items:
            if(item.name.upper() == fullArgs.upper()):
                #found item in full name
                return item
        
        #Check tags
        for item in items:
            for arg in args:
                if(arg.lower() in item.tags):
                    #found item in tag
                    return item

    print("Couldn't find that item")

def GetNPC(args):
    roomDetails = GetRoom(currentRoom)

    fullArgs = " ".join([str(arg) for arg in args])
    for npc in roomDetails.npc:
        if(npc.name.upper() == fullArgs.upper()):
            return npc

    for npc in roomDetails.npc:
        for arg in args:
            if(arg.lower() in npc.tags):
                return npc

    print("Couldn't find that person")

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
            commandParts = command.split(" ")
            if(len(playerCommand) >= len(commandParts)):
                commandRecognized = True
                for i in range(len(commandParts)):
                    if(commandParts[i].upper() == playerCommand[i].upper()):
                        pass
                    else:
                        commandRecognized = False
                        break
                
                if(commandRecognized):
                    for j in range(len(commandParts)):
                        playerCommand.pop(0)
                    
                    fullCommand = commands[key]
                    argsToGive = []
                    if(fullCommand.args is None):
                        pass
                    else:
                        for arg in fullCommand.args:
                            argsToGive.append(arg)

                    for playerArg in playerCommand:
                        argsToGive.append(playerArg)

                    return CommandResponse(Command(fullCommand.function, argsToGive, fullCommand.expectedArgs, fullCommand.followUp), " ".join([str(part) for part in commandParts]))
            

def AskCommand():
    playerInput = input("> ")
    if(len(playerInput) <= 0):
        print("No input")
    else:
        inputInList = playerInput.split(" ")
        commandResponse = GetCommand(inputInList)
        if(commandResponse is None):
            print("Command not found")
        else:
            command = commandResponse.command
            argsCount = len(command.args)
            if(command.expectedArgs == 0):
                if(argsCount > 0):
                    print("Don't know what you mean")
                else:
                    RunCommand(command)
            elif(command.expectedArgs == -1):
                #no limit for arguments, so send all arguments
                RunCommand(command)
            else:
                if(command.expectedArgs == argsCount):
                    RunCommand(command)
                elif(argsCount < command.expectedArgs and argsCount >= 0):
                    AskFollowUp(commandResponse.baseCommand)
                elif(argsCount > command.expectedArgs):
                    print("Don't know what you mean")

def AskFollowUp(basecommand):
    baseCommandInList = basecommand.split(" ")
    commandDetails = GetCommand(baseCommandInList).command
    print(commandDetails.followUp)
    playerInput = input("> ")
    if(len(playerInput) <= 0):
        print("No input")
    else:
        inputInList = playerInput.split(" ")
        argsCount = len(inputInList)
        argsToGive = []
        if(commandDetails.args is None):
            pass
        else:
            for arg in commandDetails.args:
                argsToGive.append(arg)

        for playerArg in inputInList:
            argsToGive.append(playerArg)

        if(commandDetails.expectedArgs == -1):
            RunCommand(Command(commandDetails.function, argsToGive, commandDetails.expectedArgs, commandDetails.followUp))
        else:
            if(commandDetails.expectedArgs == argsCount):
                RunCommand(Command(commandDetails.function, argsToGive, commandDetails.expectedArgs, commandDetails.followUp))
            else:
                print("Don't know what you mean")

#Command loop
while True:
    AskCommand()