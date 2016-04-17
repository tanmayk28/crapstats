from bet import Bet
from log import Log
from dice import Dice
from plotter import *

CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11


class Table(object):
    def __init__(self, minimum, player, input_rolls):
        self.bet = Bet()
        self.player = player
        self.dice = Dice()
        self.input_rolls = input_rolls

        self.point = None
        self.minimum = minimum

        # metadata
        self.shooters = 1
        self.rolls = 1
        self.longest_roll = 0
        self.points_won = 0
        self.points_lost = 0
        self.naturals_won = 0
        self.naturals_lost = 0
        self.come_out_naturals = 0
        self.craps_won = 0
        self.craps_lost = 0
        self.come_out_craps = 0
        self.roll_history = []
        self.delta = (0, 0)

    def simulate(self):
        while self.continue_betting():
            log = Log()
            self.player.strategy(self)
            log.pre_roll(self)
            self.shoot()
            self.delta = self.evaluate_roll()
            log.post_roll(self)
            self.player.catalogue(self, log)
        self.player.tabulate()
        self.log()

    def evaluate_roll(self):
        if self.point is None:
            if self.dice.total in NATURALS:
                delta = self.bet.assess_naturals(self)
                self.come_out_naturals += 1
            elif self.dice.total in CRAPS:
                delta = self.bet.assess_craps(self)
                self.come_out_craps += 1
            elif self.dice.total in BOXES:
                delta = self.bet.assess_box(self)
            else:
                raise Exception('Invalid Roll')
        else:
            if self.dice.total == SEVEN:
                delta = self.bet.assess_seven_out(self)
            elif self.dice.total == YOLEVEN:
                delta = self.bet.assess_yoleven(self)
            elif self.dice.total in CRAPS:
                delta = self.bet.assess_craps(self)
            elif self.dice.total in BOXES:
                delta = self.bet.assess_box(self)
            else:
                raise Exception('Invalid Roll')
        self.player.log_bankroll()
        return delta

    def log(self):
        print 'POINTS WON:', self.points_won, '\t\tSEVEN OUTS:', self.points_lost
        print 'NATURALS:', self.come_out_naturals, '\t\tCRAPS:', self.come_out_craps
        print 'LONGEST ROLL:', self.longest_roll, '\tAVG ROLL:', self.rolls / float(self.shooters)
        line_plot(self.player.bankroll_history)
        # pie_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values())
        # bar_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values(), 11)

    def shoot(self):
        if self.input_rolls is None:
            self.dice.roll()
        else:
            self.dice.add_roll(self.input_rolls[self.rolls - 1])

        self.rolls += 1
        return self.dice

    def continue_betting(self):
        if self.input_rolls is None:
            if self.player.bankroll <= 0:
                return False
            else:
                # wait for the current shooter to seven-out
                if self.rolls >= 20 and self.dice.total == 7:
                    return False
                else:
                    return True
        else:
            if self.player.bankroll <= 0 or self.rolls > len(self.input_rolls):
                return False
            else:
                return True

    def update_seven_out_stats(self):
        self.shooters += 1
        self.longest_roll = max(self.longest_roll, self.dice.current_roll)
        self.dice.current_roll = 0
