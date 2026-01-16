import random


class Dice:

    def __init__(self):
        self.MAX_DICE = 5
        self.dice = []

    def roll_dice(self, keep):
        for i in range(self.MAX_DICE - len(self.keep)):
            num = random.randint(1, 6)
            self.dice.append(num)
        return self.dice + keep


class Die:
    DEF_ROLL = 1

    def __init__(self):
        self.value = self.DEF_ROLL

    def roll(self):
        self.value = random.randint(1, 6)
        return self.value

    def get_value(self):
        return self.value
