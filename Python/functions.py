def NieuweFunctie(text, doPrint = True):
    if(doPrint):
        print(text)
        return "Dit geef ik terug"

returnValue = NieuweFunctie("Dit is een nieuwe functie")
print(returnValue)