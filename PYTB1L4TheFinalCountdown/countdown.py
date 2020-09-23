import time

soundCantPlay = False

try:
    from playsound import playsound
except ModuleNotFoundError:
    soundCantPlay = True

for i in range(1000, -1, -1):
    print(i)
    time.sleep(0.01)

if(soundCantPlay):
    print("BOEM")
else:
    playsound("C:\\Users\\Lucas\\Desktop\\School\\PythonAchievements\\PYTB1L4TheFinalCountdown\\boom.mp3")