# Add your Python code here. E.g.
from microbit import *
import speech
import random

onderwerp = ["she", "Ed", "Rosmerta"]
werkwoord = ["walks", "learns", "drinks"]
rest = ["hard", "at school", "coffee"]

currentPitch = 100

def sayTheWords1(word):
    global currentPitch
    speech.say(word, speed=120, pitch=currentPitch, throat=100, mouth=100)
    sleep(500)
    currentPitch = display.read_light_level()
    
def sayTheWords2():
    global currentPitch
    willekeurigGetal = random.randint(0, len(onderwerp) -1)
    print(willekeurigGetal)
    display.show(willekeurigGetal)
    sayTheWords1(onderwerp[willekeurigGetal])
    sayTheWords1(werkwoord[willekeurigGetal])
    sayTheWords1(rest[willekeurigGetal])

while True:
    #readingX = accelerometer.get_x()
    
    #print(display.read_light_level())
    
    if(button_a.is_pressed()):
        display.show(Image.HAPPY)
        sayTheWords1("hallo i am happy")
    elif(button_b.is_pressed()):
        display.show(Image.SAD)
        sayTheWords1("why are you sad")
    elif(display.read_light_level() < 40):
        sayTheWords2()
    else:
        display.show(Image.SQUARE)
