import datetime

while True:
    print("Hello You!, Ik ben Lucas")
    print("Wie ben jij?")
    name = input()
    print("Hello " + name)
    print("De datum en tijd is " + str(datetime.datetime.now()))
    while True:
        againInput = input(name + " wil jij dit programma nog een keer doen? Type Y/N: ")
        if againInput.upper() == "Y":
            break
        elif againInput.upper() == "N":
            print("Oke. Dankjewel")
            exit()
        else:
            print("\nKies tussen Y of N")