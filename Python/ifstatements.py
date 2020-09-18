varA = 5
varB = 10

if (varA == 5):
    print("varA staat gelijk aan 5")

else:
    print("varA staat niet gelijk aan 5")

if(varA == varB):
    print("varA staat gelijk aan varB")
elif (varA < varB):
    print("varA is kleiner dan varB")
elif (varA == 50):
    pass #Doe niks
else:
    print("varA is toch groter dan varB")

if(False):
    print("Doe dit")

varW = False
varX = True
varY = True
varZ = True

if(varW and varX or varY and varZ):
    print("Print dit")
    
if(varW and (varX or varY) and varZ):
    print("Print mij ook")


print("Einde programma")