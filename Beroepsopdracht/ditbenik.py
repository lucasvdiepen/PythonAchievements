import datetime
import time
import sys
import random

testval = chr(2)

dialogCharDelay = 0.07
chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

correctResponses = ["Goed!", "Klopt!", "Correct!", "Goed gegokt"]
incorrectResponses = ["Fout", "Helaas", "Verkeerd gegokt"]

class Question():
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options

questions = []

#questions.append(Question("", "", {"": "", "": "", "": ""}))
questions.append(Question("Woon", "Waar woon ik?", {"Alkmaar": "Leeftijd", "Amsterdam": "Leeftijd", "Heerhugowaard": "Leeftijd"}))
questions.append(Question("Leeftijd", "Hoe oud ben ik?", {"17": "Niveau", "15": "Niveau", "16": "Niveau"}))
questions.append(Question("Niveau", "Welk niveau heb ik vorig jaar gedaan", {"havo": "Snack", "vwo": "Snack", "vmbo-t": "Snack"}))
questions.append(Question("Snack", "Wat is mijn lievelings snack?", {"Frikandel": "", "Kaassouflé": "", "Kroket": "Groente"}))
questions.append(Question("Groente", "Oke dat klopt. \n\nWat is dan mijn lievelings groente?", {"Broccoli": "", "Wortels": "", "Bloemkool": ""}))

def ShowTextAnimation(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(dialogCharDelay)
    print("")

def GetQuestion(questionName):
    for question in questions:
        if(question.name == questionName):
            return question

def AskQuestions():
    nextQuestion = "Woon"
    while True:
        currentQuestion = GetQuestion(nextQuestion)
        nextQuestion = AskQuestion(currentQuestion.question, currentQuestion.options)
        if(nextQuestion == "" or nextQuestion is None):
            break

    print("Klaar.")


def AskQuestion(question, options):
    if len(options) > len(chars):
        return
    rndChoices = list(range(0, len(options)))
    correctAnswerIndex = -1

    nextQuestions = {"nothing": "nothing"}

    print(question + "\n")

    for j in range(len(rndChoices)):
        rnd = random.choice(rndChoices)
        values = options.values()
        nextQuestions[chars[j]] = list(values)[rnd]
        keys = options.keys()
        print(chars[j] + ". " + list(keys)[rnd])
        if(rnd == (len(options) - 1)):
            correctAnswerIndex = j
        
        rndChoices.remove(rnd)
    
    print("")
    while True:
        answer = input("> ")
        if(len(answer) == 1 and answer.isalpha()):
            if(len(options) >= (chars.index(answer.upper()) + 1)):
                if answer.upper() == chars[correctAnswerIndex]:
                    print(random.choice(correctResponses))
                else:
                    print(random.choice(incorrectResponses))
                
                time.sleep(1)

                print("\n")
                return nextQuestions[answer.upper()]

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
    #AskQuestion("Waar woon ik?", ["Alkmaar", "Amsterdam", "Heerhugowaard"])
    #AskQuestion("Welk niveau heb ik vorig jaar gedaan", ["havo", "vwo", "vmbo-t"])
    #AskQuestion("Hoe oud ben ik?", ["17", "15", "16"])
    AskQuestions()
    while True:
        againInput = input(name + " wil jij dit programma nog een keer doen? Type Y/N: ")
        if againInput.upper() == "Y":
            print("\n\n")
            break
        elif againInput.upper() == "N":
            print("Oke. Dankjewel")
            time.sleep(1)
            exit()
        else:
            print("\nKies tussen Y of N")