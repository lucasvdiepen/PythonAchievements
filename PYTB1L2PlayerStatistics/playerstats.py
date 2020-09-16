from enum import Enum

class Gun(Enum):
    def __str__(self):
        return str(self.value)
    
    Pistol = "Pistol"
    SMG = "Sub Machine Gun"
    AR = "Assult Rifle"
    Sniper = "Sniper"

def newPlayer(name, age, strength, gun, ammo, alive, level, kills, lives, money):
    Player = {
        "Name": name,
        "Age": age,
        "Strength": strength,
        "Gun": gun,
        "Ammo": ammo,
        "Alive": alive,
        "Level": level,
        "Kills": kills,
        "Lives": lives,
        "Money": money
    }
    return Player

player = newPlayer("Lucas", 16, 100, Gun.Sniper, 40, True, 99, 18, 3, 66.55)

for key in player:
    value = player[key]
    print(key + ": " + str(value))
