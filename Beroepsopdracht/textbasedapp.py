class Item:
    def __init__(self, name, pickable, tags):
        self.name = name
        self.pickable = pickable
        self.tags = tags

class Room:
    def __init__(self, title, description, items, roomDirections):
        self.title = title
        self.description = description
        self.items = items
        self.roomDirections = roomDirections #make this a dictionary

class Command:
    def __init__(self, function, args, expectedArgs):
        self.function = function
        self.args = args
        self.expectedArgs = expectedArgs

rooms = []
commands = {
    "n,north": Command("GoDirection", "n", 0),
    "w,west": Command("GoDirection", "w", 0),
    "e,east": Command("GoDirection", "e", 0),
    "s,south": Command("GoDirection", "s", 0)
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

def RunCommand(command):
    #globals()[FindFunction(func)](FindArgs(func))
    globals()[command.function](command.args)


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
                    pass
                    #no limit for arguments, so send all arguments
                    RunCommand(Command(command.function, inputInList[1:len(inputInList)], command.expectedArgs))
            else:
                if(command.expectedArgs == argsCount):
                    RunCommand(Command(command.function, inputInList[1:len(inputInList)], command.expectedArgs))
                elif(argsCount < command.expectedArgs and argsCount >= 0):
                    print("Don't know what you mean yet. Follow up question should happen here")
                elif(argsCount > command.expectedArgs):
                    print("Don't know what you mean")
                
                    
    
        
        

#Setup process


#Command loop
while True:
    AskCommand()