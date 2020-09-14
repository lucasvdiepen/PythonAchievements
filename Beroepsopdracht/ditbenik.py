import datetime
import time
import sys
import random

testval = chr(2)

dialogCharDelay = 0.07
chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

print(chars.index("C"))

def ShowTextAnimation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(dialogCharDelay)
    print("")

def AskQuestion(question, options):
    if len(options) > len(chars):
         return
    rndChoices = list(range(0, len(options)))
    correctAnswerIndex = -1

    print(question + "\n")

    for j in range(len(rndChoices)):
        rnd = random.choice(rndChoices)
        print(chars[j] + ". " + options[rnd])
        if(rnd == (len(options) - 1)):
            correctAnswerIndex = j
        
        rndChoices.remove(rnd)
    
    print("")
    while True:
        answer = input("Antwoord: ")
        if(len(answer) == 1 and answer.isalpha()):
            if(len(options) >= (chars.index(answer.upper()) + 1)):
                if answer.upper() == chars[correctAnswerIndex]:
                    print("Goed")
                else:
                    print("Fout")

                break

            else: print("Kies de letter van een van de antwoorden \n\n")
        else: print("Kies de letter van een van de antwoorden \n\n")


while True:
    print("Hello You!, Ik ben Lucas")
    print("Wie ben jij?")
    name = input()
    #print("Hello " + name)
    ShowTextAnimation("Hello " + name)
    print("De datum en tijd is " + str(datetime.datetime.now()) + "\n\n")
    #Het laatste antwoord moet altijd het goede antwoord zijn
    AskQuestion("test vraag?", ["antwoord1", "antwoord2", "antwoord3"])
    while True:
        againInput = input(name + " wil jij dit programma nog een keer doen? Type Y/N: ")
        if againInput.upper() == "Y":
            for i in range(3):
                print("")
            break
        elif againInput.upper() == "N":
            print("Oke. Dankjewel")
            time.sleep(1)
            exit()
        else:
            print("\nKies tussen Y of N")