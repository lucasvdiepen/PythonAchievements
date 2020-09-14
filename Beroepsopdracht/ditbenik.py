import datetime
import time
import sys
import random

dialogCharDelay = 0.07
l = ["A", "B", "C"]

def ShowTextAnimation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(dialogCharDelay)
    print("")

def AskQuestion(question, options):
    print(question + "\n")

    rndChoices = [0, 1, 2]
    correctAnswerIndex = -1

    for j in range(3):
        rnd = random.choice(rndChoices)
        print(l[j] + ": " + options[rnd])
        if(rnd == 2):
            correctAnswerIndex = j
        
        rndChoices.remove(rnd)
    
    print("\n")
    while True:
        answer = input("Antwoord: ")
        if(answer.upper() == "A" or answer.upper() == "B" or answer.upper() == "C"):
            if answer.upper() == l[correctAnswerIndex]:
                print("Goed")
            else:
                print("Fout")

            break

        else:
            print("Kies tussen A, B of C \n\n")


while True:
    print("Hello You!, Ik ben Lucas")
    print("Wie ben jij?")
    name = input()
    #print("Hello " + name)
    ShowTextAnimation("Hello " + name)
    print("De datum en tijd is " + str(datetime.datetime.now()) + "\n\n")
    AskQuestion("test vraag???", ["antwoord1", "antwoord2", "antwoord3"])
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