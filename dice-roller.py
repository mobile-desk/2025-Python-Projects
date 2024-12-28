import random

def roll_dice(num_dice, num_rolls):
    rolls = []
    for _ in range(num_rolls):
        roll = [random.randint(1, 6) for _ in range(num_dice)]
        rolls.append(roll)
    return rolls

num_dice = int(input("Enter the number of dice: "))
num_rolls = int(input("Enter the number of rolls: "))

print(roll_dice(num_dice, num_rolls))
