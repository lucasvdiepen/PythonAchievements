import time
import random

chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class Question():
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options

questions = []

#questions.append(Question("", """ """, {"": "", "": ""}))
questions.append(Question("START", """Je moet zo snel mogelijk vluchten. 

Neem je nog afscheid van je familie en vrienden?""", {"Ja": "1", "Nee": "1"}))

questions.append(Question("1", """Je zit nu in Damascus je moet naar Beiroet. 

Hoe ga je daarnaartoe?""", {"Lopend": "2", "Met de bus": "3"}))

def GetQuestion(questionName):
    for question in questions:
        if(question.name == questionName):
            return question

def AskQuestions():
    nextQuestion = "START"
    while True:
        currentQuestion = GetQuestion(nextQuestion)
        nextQuestion = AskQuestion(currentQuestion.question, currentQuestion.options)
        if(nextQuestion == "" or nextQuestion is None):
            break

    print("Dit waren de vragen.")


def AskQuestion(question, options):
    if len(options) > len(chars):
        return

    nextQuestions = {"nothing": "nothing"}

    print(question + "\n")

    for j in range(len(options)):
        values = options.values()
        nextQuestions[chars[j]] = list(values)[j]
        keys = options.keys()
        print(chars[j] + ". " + list(keys)[j])
    
    print("")
    while True:
        answer = input("> ")
        if(len(answer) == 1 and answer.isalpha()):
            if(len(options) >= (chars.index(answer.upper()) + 1)):
                time.sleep(0.5)

                print("\n")
                return nextQuestions[answer.upper()]

            else: print("Kies de letter van een van de antwoorden \n\n")
        else: print("Kies de letter van een van de antwoorden \n\n")

while True:
    AskQuestions()

    while True:
        againInput = input("wil jij dit programma nog een keer doen? Type Y/N: ")
        if againInput.upper() == "Y":
            print("\n\n")
            break
        elif againInput.upper() == "N":
            print("Oke. Dankjewel")
            time.sleep(1)
            exit()
        else:
            print("\nKies tussen Y of N")