import time
import random

chars = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

class Question():
    def __init__(self, name, question, options):
        self.name = name
        self.question = question
        self.options = options

questions = []

#questions.append(Question("", "", {"": "", "": "", "": ""}))

def GetQuestion(questionName):
    for question in questions:
        if(question.name == questionName):
            return question

def AskQuestions():
    nextQuestion = "Start"
    while True:
        currentQuestion = GetQuestion(nextQuestion)
        nextQuestion = AskQuestion(currentQuestion.question, currentQuestion.options)
        if(nextQuestion == "" or nextQuestion is None):
            break

    print("Dit waren de vragen.")


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
                time.sleep(1)

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