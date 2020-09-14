# Add your Python code here. E.g.
from microbit import *
import time
import random

highscore = 0

startingHearts = 5
startingDownTime = 1000

""""img = Image("05050:"
             "05050:"
             "05050:"
             "99999:"
             "09990")

prevX = 0
prevY = 0

x = 0
y = 0

while True:
    display.set_pixel(prevX, prevY, 0)
    display.set_pixel(x, y, 9)
    prevX = x
    prevY = y
    if(x == 4 and y == 4):
        time.sleep(0.2)
        break
    if(x == 4):
        y += 1
        x = -1
    x += 1
    time.sleep(0.2)
    
display.clear()"""

#display.scroll("HELLO YOU!")

def Missed(currentHearts):
    print("Missed")
    for i in range(3):
        display.show(Image.HEART)
        time.sleep(0.3)
        display.clear()
        time.sleep(0.3)
    
    display.show(currentHearts)
    time.sleep(2)
    display.clear()

def Game(gameHearts, gameDownTime, currentHighscore):
    points = 0
    ballY = 0
    prevx = 0
    prevy = 0
    catchX = 0
    prevCatchX = 0
    rndLine = 0
    dropDownTime = 0
    millis = 0
    hearts = gameHearts
    downTime = gameDownTime
    
    while True:
        #move pixel to left and right
        readingX = accelerometer.get_x()
        if readingX < -300 and readingX > -550:
            catchX = 1
        
        if readingX < -600:
            catchX = 0
                
        if readingX > 300 and readingX < 550:
            catchX = 3
        
        if readingX > 600:
            catchX = 4
                
        if readingX > -250 and readingX < 250:
            catchX = 2
        
        if not catchX == prevCatchX:
            display.set_pixel(prevCatchX, 4, 0)
        
        display.set_pixel(catchX, 4, 9)
        prevCatchX = catchX
        
        #drop down pixels
        millis = time.ticks_ms()
        if(millis - dropDownTime) > downTime:
            display.set_pixel(prevx, prevy, 0)
            display.set_pixel(rndLine, ballY, 9);
            prevx = rndLine
            prevy = ballY
            ballY += 1
            if ballY == 5:
                if rndLine == catchX:
                    print("Catched")
                    points += 1
                    if not downTime <= 200:
                        downTime -= 50
                else:
                    #missed
                    hearts -= 1
                    Missed(hearts)
                    if hearts <= 0:
                        #game over
                        
                        #check if this score is higher than highscore
                        if(points > currentHighscore):
                            #new highscore
                            with open("highscore", "w") as highscoreFile:
                                scoreToSave = str(points)
                                highscoreFile.write(scoreToSave)
                                
                        scoreText = 'Score: ' + str(points)
                        display.scroll(scoreText)
                        display.clear()
                        break
                
                ballY = 0
                rndLine = random.randint(0, 4)
                
            dropDownTime = millis


arrowEnabled = False
menuMillis = 0
menuTime = 0

#Getting highscore
try:
    with open("highscore.txt", "r") as file:
        highscore = file.read()
except OSError:
    print("OSERROR")
    highscore = 0

#Menu
while True:
    menuMillis = time.ticks_ms()
    if(menuMillis - menuTime) > 600:
        #toggle arrow to left
        menuTime = menuMillis
        if arrowEnabled:
            display.clear()
            arrowEnabled = False
        else:
            display.show(Image.ARROW_W)
            arrowEnabled = True
            
    if button_a.is_pressed():
        display.clear()
        Game(startingHearts, startingDownTime, highscore)
        
    if button_b.is_pressed():
        display.clear()
        highscoretxt = "Highscore: " + str(highscore)
        display.scroll(highscoretxt)
