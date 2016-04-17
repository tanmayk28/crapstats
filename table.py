from log import Log
from dice import Dice
from plotter import *

CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11


class Table(object):
    def __init__(self, minimum, players, input_rolls):
        self.players = players
        self.dice = Dice()
        self.input_rolls = input_rolls

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
        while self.continue_playing():
            self.shoot()
            for player in self.players:
                if self.continue_betting(player):
                    log = Log()
                    player.strategy(self)
                    log.pre_roll(self, player)
                    self.delta = self.evaluate_roll(player)
                    log.post_roll(self, player)
                    player.catalogue(self, log)
            self.rolls += 1

        for player in self.players:
            print player.__doc__
            player.tabulate()
            self.log(player)

    def evaluate_roll(self, player):
        if player.point is None:
            if self.dice.total in NATURALS:
                delta = player.bet.assess_naturals(self, player)
                self.come_out_naturals += 1
            elif self.dice.total in CRAPS:
                delta = player.bet.assess_craps(self, player)
                self.come_out_craps += 1
            elif self.dice.total in BOXES:
                delta = player.bet.assess_box(self, player)
            else:
                raise Exception('Invalid Roll')
        else:
            if self.dice.total == SEVEN:
                delta = player.bet.assess_seven_out(self, player)
            elif self.dice.total == YOLEVEN:
                delta = player.bet.assess_yoleven(player)
            elif self.dice.total in CRAPS:
                delta = player.bet.assess_craps(self, player)
            elif self.dice.total in BOXES:
                delta = player.bet.assess_box(self, player)
            else:
                raise Exception('Invalid Roll')
        player.log_bankroll()
        return delta

    def log(self, player):
        print 'POINTS WON:', self.points_won, '\t\tSEVEN OUTS:', self.points_lost
        print 'NATURALS:', self.come_out_naturals, '\t\tCRAPS:', self.come_out_craps
        print 'LONGEST ROLL:', self.longest_roll, '\tAVG ROLL:', self.rolls / float(self.shooters)
        line_plot(player.bankroll_history)
        # pie_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values())
        # bar_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values(), 11)

    def shoot(self):
        if self.input_rolls is None:
            self.dice.roll()
        else:
            self.dice.add_roll(self.input_rolls[self.rolls - 1])

        return self.dice

    def continue_betting(self, player):
        if self.input_rolls is None:
            if player.bankroll <= 0:
                return False
            else:
                # wait for the current shooter to seven-out
                if self.rolls >= 20000 and self.dice.history[self.rolls - 1] == 7:
                    return False
                else:
                    return True
        else:
            if player.bankroll <= 0 or self.rolls > len(self.input_rolls):
                return False
            else:
                return True

    def continue_playing(self):
        play = False
        for player in self.players:
            play = play or self.continue_betting(player)
        return play

    def update_seven_out_stats(self):
        self.shooters += 1
        self.longest_roll = max(self.longest_roll, self.dice.current_roll)
        self.dice.current_roll = 0
