import datetime
import time
import sys

dialogCharDelay = 0.07

def ShowTextAnimation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(dialogCharDelay)
    print("")

while True:
    print("Hello You!, Ik ben Lucas")
    print("Wie ben jij?")
    name = input()
    #print("Hello " + name)
    ShowTextAnimation("Hello " + name)
    print("De datum en tijd is " + str(datetime.datetime.now()))
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