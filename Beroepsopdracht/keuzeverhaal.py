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

questions.append(Question("2", """Na een tijdje lopen besef je dat het te lang gaat duren. Je moet een andere manier vinden om in Beiroet te komen.
Je gaat met …
""", {"de bus": "3", "een auto": "3"}))

questions.append(Question("3", """Eenmaal aangekomen in Beiroet neem je gelijk de boot naar Mersin.
Je bent veilig aangekomen in Turkije. Je moet nu een weg naar Griekenland vinden.
""", {"betaalt een smokkelaar": "5", "Gaat zelf naar de grens toe": "4"}))

questions.append(Question("4", """Eenmaal aangekomen bij de grens van Griekenland probeer je het land in te komen. Helaas laat de grensbewaking je niet door.""", {"": "", "": ""}))

questions.append(Question("5", """De smokkelaar neem je mee op een boot. Na een lange tijd varen gaat de motor van de boot stuk. Mensen beginnen te huilen.
Wat doe je?
""", {"Je zegt dat ze moeten ophouden en dat het goed komt": "6", "Je doet niks": "6"}))

questions.append(Question("6", """De motor van de boot is nog steeds kapot.
Je ...
""", {"probeert de motor te rapareren": "7", 'schreeuwt: "HELP!"': "8"}))

questions.append(Question("7", """Je hebt niet de juiste gereedschap om de motor te maken. Je moet iets anders proberen.
Je ...
""", {'schreeuwt: "HELP!"': "8", "doet niks": "8"}))

questions.append(Question("8", """Gelukkig komt er een Griekse boot aanvaren die jullie brengt naar een Grieks eiland. Je reist meteen naar de grens van Griekenland. Daar moet je lang lopen en neem je de trein. Na weer een lange reis ben je in Hongarije. In de verte zie je soldaten staan.
Wat doe je?
""", {"Je gaat een andere kant op en vermijd de soldaten": "10", "Je loopt naar de soldaten toe": "9"}))

questions.append(Question("9", """De soldaten vinden je verdacht en ze nemen je mee.""", {"": "", "": ""}))

questions.append(Question("10", """Je komt een man tegen. Hij vraagt of je gebracht wil worden naar Boedapest met de auto.
Wat zeg je?
""", {"Ja heel graag": "13", "Nee bedankt": "11"}))

questions.append(Question("11", """Je loopt door. In de verte zie je soldaten.
Wat doe je?
""", {"Je gaat een andere kant op en vermijd de soldaten": "13", "Je gaat richting de soldaten": "12"}))

questions.append(Question("12", """Je probeert normaal te doen om niet op te vallen. De soldaten kijken je aan en lopen verder. Je bent uitgeput van al het lopen.
Je besluit …
""", {"Toch door te lopen": "13", "Een taxi te nemen": "13"}))

questions.append(Question("13", """Je bent aangekomen op het station in Boedapest.
Welke trein neem je?
""", {"De trein naar Düsseldorf": "14", "De trein naar Amsterdam": "16"}))

questions.append(Question("14", """Je bent na een lange trein reis in Düsseldorf aangekomen. Je moet een manier vinden om naar Nederland te gaan.
Je besluit om …
""", {"te lopen": "15", "te liften bij mensen": "16"}))

questions.append(Question("15", """Je merkt al snel dat lopen veel te zwaar is. Je zal dus toch misschien moeten liften.
Je besluit om …
""", {"toch te gaan liften": "16", "door te lopen": "16"}))

questions.append(Question("16", """Je bent eindelijk aangekomen in Nederland. Je zoekt het politiebureau. Eenmaal aangekomen bij het politiebureau zeggen ze je dat je de volgende dag naar de immigratiepolitie moet gaan.
Je besluit om ...
""", {"te gaan slapen": "17", "een plan te bedenken voor morgen": "17"}))

questions.append(Question("17", """De volgende dag ga je weer naar het politiebureau om je in te schrijven in Nederland. Je bent nu ingeschreven in Nederland. Je kreeg de opdracht om naar Ten Apel te gaan en je daar te registreren voor een opvang huisje. Je hebt ook asiel aangevraagd. Na een paar gesprekken is je asiel aanvraag goedgekeurd. Je zal nu een inburgeringsexamen moeten doen.

Ga je nu veel over Nederland leren voor de toets?
""", {"Ja": "20", "Nee": "18"}))

questions.append(Question("18", """Helaas. Je bent gezakt voor je inburgeringstoets. Je bedenkt dat het handig is voor de tweede goed te leren.
Je besluit voor de tweede poging …
""", {"goed te leren": "20", "niet te leren": "19"}))

questions.append(Question("19", """Helaas je bent voor de tweede keer gezakt voor je inburgeringstoets.""", {"": "", "": ""}))

questions.append(Question("20", """Je bent geslaagd voor je inburgeringstoets!
Het is handig om een opleiding te doen zodat je kan werken in Nederland.
Welke opleiding wil je doen?
""", {"Sustainable Energy Technology": "21", "Robotics": "21"}))

questions.append(Question("21", """Na een aantal jaar studeren ben je geslaagd. Je hebt werk gevonden en je hebt een huisje gekregen in Delft. Je bent gelukkig in Nederland en je hebt nu een nieuw leven.""", {"": "", "": ""}))

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

    print("Dit is het einde.")


def AskQuestion(question, options):
    if len(options) > len(chars):
        return

    nextQuestions = {"nothing": "nothing"}

    askInput = False

    for option in options:
        if(not option == ""):
            askInput = True
            break

    print(question + "\n")

    if(askInput):
        for j in range(len(options)):
            values = options.values()
            nextQuestions[chars[j]] = list(values)[j]
            keys = options.keys()
            print(chars[j] + ". " + list(keys)[j])
    
    print("")
    while askInput:
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