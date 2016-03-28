import operator
from bet import Bet
from log import Log

CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11


class Table(object):
    def __init__(self, minimum, player):
        self.bet = Bet()
        self.point = None
        self.minimum = minimum
        self.player = player
        self.shooters = 1
        self.rolls = 1
        self.roll_history = []
        self.delta = (0, 0)

    def simulate(self):
        dice = self.player.dice
        while self.stop_condition():
            log = Log()
            log.pre_roll(self)
            self.player.strategy(self)
            self.delta = self.evaluate_roll(self, dice.roll())
            log.post_roll(self)
            self.player.catalogue(self, log)
        self.player.tabulate()

    def evaluate_roll(self, table, dice):
        table.rolls += 1
        delta = (0, 0)
        check = None

        if table.point is None:
            if dice.total in NATURALS:
                delta = self.bet.assess_naturals(table)
                check = u'\u2714' * 4
            elif dice.total in CRAPS:
                delta = self.bet.assess_craps(table)
                check = u'\u2718' * 4
            elif dice.total in BOXES:
                delta = self.bet.assess_box(table, dice)
            else:
                raise Exception('Invalid Roll')
        else:
            if dice.total == SEVEN:
                check = u'\u2718' * 4
                delta = self.bet.assess_seven_out(table)
            elif dice.total == YOLEVEN:
                pass
            elif dice.total in CRAPS:
                pass
            elif dice.total in BOXES:
                if table.point == dice.total:
                    check = u'\u2714' * 4
                delta = self.bet.assess_box(table, dice)
            else:
                raise Exception('Invalid Roll')
        return delta

    def stop_condition(self):
        if self.shooters == 1000 or self.rolls == 10000 or self.player.bankroll <= 0:
            return False
        else:
            return True
