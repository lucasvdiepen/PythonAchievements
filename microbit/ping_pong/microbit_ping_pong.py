# Add your Python code here. E.g.
import radio
from microbit import display, Image, button_a, button_b, accelerometer
import time
import random

class Ball:
    def __init__(self, x, y, directionX, directionY):
        self.x = x
        self.y = y
        self.directionX = directionX
        self.directionY = directionY
        
    def ApplyMovement(self):
        self.x += self.directionX
        self.y += self.directionY
        
    def Bounce(self, byPlayer = False):
        if(byPlayer):
            self.directionY = -1
            self.directionX = random.choice([-1, 1])
        else:
            self.directionX = self.directionX * -1
            
clocks = [Image.CLOCK1, Image.CLOCK2, Image.CLOCK3, Image.CLOCK4, Image.CLOCK5, Image.CLOCK6, Image.CLOCK7, Image.CLOCK8, Image.CLOCK9, Image.CLOCK10, Image.CLOCK11, Image.CLOCK12]
clockIndex = 0
ball = None
points = 0
pointsToWin = 3
ballMoveDelay = 500
pairDelay = 3000
buttonDelay = 300
clockUpdateDelay = 200
lookingForGame = False
prevBallMove = 0
prevPairTime = 0
prevButtonTime = 0
prevClockTime = 0
catchX = 0
prevCatchX = 0
gameStarted = False

def EndScreen(win):
    global gameStarted
    gameStarted = False
    if(win):
        display.scroll("You win")
    else:
        display.scroll("You lose")
    display.scroll('Press a button to start ', wait=False, loop=True)

def GetOppositeX(x):
    if(x == -1):
        return 4
    elif(x == 0):
        return 4
    elif(x == 1):
        return 3
    elif(x == 2):
        return 2
    elif (x == 3):
        return 1
    elif (x == 4):
        return 0
    elif (x == 5):
        return 0
        
def AddPoint():
    global points
    global pointsToWin
    for i in range(4):
        display.clear()
        time.sleep(0.5)
        display.show(points)
        time.sleep(0.5)
        if(i == 0):
            points += 1
    display.clear()
    if(points >= pointsToWin):
        radio.send("l")
        EndScreen(True)
        
def CheckBounce():
    global ball
    if(ball.y >= 0):
        if(ball.x >= 4 and ball.directionX == 1):
            ball.Bounce()
        
        if(ball.x <= 0 and ball.directionX == -1):
            ball.Bounce()
        
def StartCountdown():
    global lookingForGame
    global gameStarted
    global ball
    global points
    
    display.clear()
    for i in range(5, -1, -1):
        display.show(i)
        time.sleep(1)
    
    display.clear()
    lookingForGame = False
    points = 0
    gameStarted = True
    prevBallMove = time.ticks_ms()
    if(not ball is None):
        display.set_pixel(ball.x, ball.y, 9)
        CheckBounce()

def RadioReceived(text):
    global ball
    global prevBallMove
    global lookingForGame
    print("Received: " + text)
    if(not gameStarted and lookingForGame):
        if(text == "s"):
            ball = Ball(random.randint(0, 4), 0, random.choice([-1, 1]), 1)
            StartCountdown()
        elif(text == "q"):
            radio.send("s")
            ball = None
            StartCountdown()
    else:
        if(text == "w"):
            EndScreen(True)
        elif(text == "l"):
            EndScreen(False)
        elif(text == "p"):
            AddPoint()
            ball = Ball(random.randint(0, 4), 0, random.choice([-1, 1]), 1)
            display.set_pixel(ball.x, ball.y, 9)
            CheckBounce()
            prevBallMove = time.ticks_ms()
        else:
            args = text.split(",")
            if(len(args) == 2):
                ball = Ball(int(args[0]), 0, int(args[1]), 1)
                display.set_pixel(ball.x, ball.y, 9)
                CheckBounce()
                prevBallMove = time.ticks_ms()
    
radio.on()
display.scroll('Press a button to start ', wait=False, loop=True)
while True:
    try:
        incoming = radio.receive()
        if(not incoming is None):
            RadioReceived(incoming)
    except Exception:
        pass
    millis = time.ticks_ms()
    if(gameStarted):
        if button_b.is_pressed():
            if(millis > (prevButtonTime + buttonDelay)):
                prevButtonTime = millis
                RadioReceived("p")
        
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
        
        if(not ball is None):
            if(millis > (prevBallMove + ballMoveDelay)):
                prevBallMove = millis
                display.set_pixel(ball.x, ball.y, 0)
                ball.ApplyMovement()
                if(ball.x < 0 or ball.x > 4 or ball.y > 4 or ball.y < 0):
                    if(ball.y < 0 and ball.directionY == -1):
                        radio.send(str(GetOppositeX(ball.x)) + "," + str(ball.directionX * -1))
                        ball = None
                else:
                    display.set_pixel(ball.x, ball.y, 9)
                    bounced = False
                    if(ball.y >= 4):
                        if(ball.x == catchX):
                            ball.Bounce(True)
                            CheckBounce()
                            bounced = True
                        else:
                            display.set_pixel(ball.x, ball.y, 0)
                            ball = None
                            radio.send("p")
                            display.clear()
                            display.show(Image.SAD)
                            time.sleep(1.5)
                            display.clear()
                            
                    if(not ball is None):
                        if(not bounced):
                            if(ball.x >= 4 or ball.x <= 0):
                                if(ball.y >= 0):
                                    ball.Bounce()
                
    else:
        if(lookingForGame):
            if(millis > (prevPairTime + pairDelay)):
                prevPairTime = millis
                radio.send("q")
                
            if(millis > (prevClockTime + clockUpdateDelay)):
                prevClockTime = millis
                display.show(clocks[clockIndex])
                clockIndex += 1
                if(clockIndex > 11):
                    clockIndex = 0
        
        if button_a.is_pressed():
            if(millis > (prevButtonTime + buttonDelay)):
                prevButtonTime = millis
                lookingForGame = not lookingForGame
                
        if button_b.is_pressed():
            RadioReceived("s")
        
