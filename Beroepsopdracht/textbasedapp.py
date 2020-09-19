class Item:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

class Room:
    def __init__(self, title, description, items, roomDirections):
        self.title = title
        self.description = description
        self.items = items
        self.roomDirections = roomDirections #make this a dictionary

rooms = []
commands = {
    "n,north": "GoDirection(n)",
    "w,west": "GoDirection(w)",
    "e,east": "GoDirection(e)",
    "s,south": "GoDirection(s)"
}

def FindFunction(s):
    end = s.index("(")
    return s[0:end]

def FindArgs(s):
    start = s.index("(") + 1
    end = s.index(")")
    return s[start:end].split(",")

def GoDirection(args):
    print(args[0])

def RunCommand(func):
    globals()[FindFunction(func)](FindArgs(func))


#RunCommand("GoDirection(teststring,moreteststrings,plusthis)")

def GetCommand(playerCommand):
    for key in commands:
        commandList = key.split(",")
        for command in commandList:
            if(command.upper() == playerCommand.upper()):
                #command found
                return commands[key]

def AskCommand():
    playerInput = input("> ")
    inputInList = playerInput.split(" ")
    
    commandFunction = GetCommand(inputInList[0])
    if(commandFunction is None or commandFunction == ""):
        print("Command not found")
    else:
        RunCommand(commandFunction)

#Setup process


#Command loop
while True:
    AskCommand()