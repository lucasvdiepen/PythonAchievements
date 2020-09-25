import random

isRunning = True

while(isRunning):
    print("HERHAAL DIT!")

    num = random.randrange(5)
    if(num == 4):
        isRunning = False
else:
    print("Einde eerste while-loop")

lijstA = ["Tekst", 11, True, '#', 4.22, "Nog wat tekst"]
lijstB = ["Dit", "is", "een", "lijst", "van", "tekst"]

print(lijstA)
print(lijstB[1])
lijstA[1] = 23
print(lijstA)