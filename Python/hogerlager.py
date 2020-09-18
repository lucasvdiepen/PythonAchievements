# Doel:
# Hoger / lager spelletje moet als volgt werken.
# De speler wordt een random getal getoond van 1 t/m 10
# De speler moet daarna raden of het volgende random getal hoger of lager wordt
# Aan het einde moet de speler weten of/zij gewonnen heeft

import random

while True:
    willekeurig_getal = random.randrange(1, 11)
    print (willekeurig_getal)
    playerInput = input("Is het volgende getal hoger of lager? H/L > ")
    volgende_willekeurig_getal = random.randrange(1, 11)
    if(playerInput.upper() == "H"):
        if(willekeurig_getal > volgende_willekeurig_getal):
            print("Fout")
        elif(willekeurig_getal < volgende_willekeurig_getal):
            print("Goed")
        else:
            print("Het getal was gelijk")
    elif(playerInput.upper() == "L"):
        if(willekeurig_getal > volgende_willekeurig_getal):
            print("Goed")
        elif(willekeurig_getal < volgende_willekeurig_getal):
            print("Fout")
        else:
            print("Het getal was gelijk")
    print ("Het getal was " + str(volgende_willekeurig_getal))
    print("\n")