import os

os.system("color 27")

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BACKGROUNDRED = '\u001b[41;1m'

print(bcolors.BACKGROUNDRED + "test" + bcolors.ENDC)

input()