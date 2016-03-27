from bet import Bet
from dice import Dice

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
        self.shooters = 0
        self.rolls = 0
        self.history = []

    def simulate(self):
        dice = self.player.dice
        print '\nSTART BANK --> ', self.player.bankroll, "\n"
        while self.stop_condition():
            self.player.strategy(self)
            print self.shooters, '\t', self.rolls, '\tBANK --> ', self.player.bankroll,
            self.evaluate_roll(self, dice.roll())
        print '\n\tEND BANK --> ', self.player.bankroll, '\tMAX BANK --> ', self.player.max_bank, '\tMIN BANK --> ', self.player.min_bank
        print '\tShooters -->', self.shooters, '\tRolls --> ', self.rolls

    def evaluate_roll(self, table, dice):
        table.rolls += 1
        check = None

        if table.point is None:
            if dice.total in NATURALS:
                self.bet.assess_naturals(table)
                check = u'\u2714' * 4
            elif dice.total in CRAPS:
                self.bet.assess_craps(table)
                check = u'\u2718' * 4
            elif dice.total in BOXES:
                self.bet.assess_box(table, dice)
            else:
                raise Exception('Invalid Roll')
        else:
            if dice.total == SEVEN:
                self.bet.assess_seven_out(table)
                check = u'\u2718' * 4
            elif dice.total in CRAPS:
                pass
            elif dice.total in BOXES:
                self.bet.assess_box(table, dice)
                if table.point == dice.total:
                    check = u'\u2714' * 4

        print '\tDICE --->', dice.total, '\tPoint --> ', table.point if table.point is not None else '-', '\t', \
            check if check is not None else ' '

    def stop_condition(self):
        if self.shooters == 1000 or self.rolls == 10000 or self.player.bankroll <= 0:
            return False
        else:
            return True
