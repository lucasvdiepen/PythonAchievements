import random

def SchudWoord(woord):
    return ''.join(random.sample(woord, len(woord)))

print(SchudWoord("random"))
print(SchudWoord("woorden"))
print(SchudWoord("schudden"))