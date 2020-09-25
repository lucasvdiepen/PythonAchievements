# Doel:
# Een "mannetje" dat links en rechts kan lopen

import os

isRunning = True
antwoord = ""

playerSprite = "@"

positieX = 0

print("Press enter to start the game")

while(isRunning):
    antwoord = input()

    if(antwoord.lower() == "quit" or antwoord.lower() == "exit"):
        isRunning = False
        break

    if(antwoord.lower() == "rechts"):
        positieX += 1
    elif(antwoord.lower() == "links"):
        positieX -= 1

    os.system("cls")

    for x in range(positieX):
        print(" ", end="")
    else:
        print(playerSprite)

    print("---------------------------------------")