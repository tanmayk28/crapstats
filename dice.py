from random import randint

CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11


class Dice(object):
    def __init__(self):
        self.total = None
        self.die1 = None
        self.die2 = None
        self.hardway = None

    def roll(self):
        self.die1 = randint(1, 6)
        self.die2 = randint(1, 6)
        self.total = self.die1 + self.die2

        if self.die1 == self.die2 and self.total in BOXES:
            self.hardway = True
        else:
            self.hardway = False

        self.add_to_history()

        return self

    def add_to_history(self):
        pass
