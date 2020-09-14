import datetime
import time
import sys
from enum import Enum
import random

dialogCharDelay = 0.07

class CorrectAnswer(Enum):
    A = 0
    B = 1
    C = 2

def ShowTextAnimation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(dialogCharDelay)
    print("")

def AskQuestion(question, options):
    print(question + "\n\n")

    rndChoices = [0, 1, 2]

    while True:
        rnd = random.choice(rndChoices)
    


while True:
    print("Hello You!, Ik ben Lucas")
    print("Wie ben jij?")
    name = input()
    #print("Hello " + name)
    ShowTextAnimation("Hello " + name)
    print("De datum en tijd is " + str(datetime.datetime.now()) + "\n\n")
    #TODO add 3 questions
    print

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