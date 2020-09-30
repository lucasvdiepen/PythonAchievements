stringArray = []
integerArray = []
floatArray = []
booleanArray = []

stuff = ['c',5645,9393.77,"hello", True, False, "Good morning",88, -90, 777.777, 90,665.33,"F"]

for stuffItem in stuff:
    stuffType = type(stuffItem)
    if(stuffType == str):
        stringArray.append(stuffItem)
    elif(stuffType == int):
        integerArray.append(stuffItem)
    elif(stuffType == float):
        floatArray.append(stuffItem)
    elif(stuffType == bool):
        booleanArray.append(stuffItem)

print("String Array: " + str(stringArray))
print("Integer Array: " + str(integerArray))
print("Float Array: " + str(floatArray))
print("Boolean Array: " + str(booleanArray))