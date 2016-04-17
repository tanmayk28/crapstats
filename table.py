from log import Log
from dice import Dice
from plotter import *

CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11


class Table(object):
    def __init__(self, minimum, players, max_rolls, input_rolls):
        self.players = players
        self.dice = Dice()
        self.input_rolls = input_rolls
        self.minimum = minimum
        self.max_rolls = max_rolls

        # metadata
        self.shooters = 1
        self.rolls = 1
        self.longest_roll = 0
        self.points_made = 0
        self.seven_outs = 0
        self.come_out_naturals = 0
        self.come_out_craps = 0
        self.roll_history = []
        self.roll_status = (0, 0, None)
        self.table_status = []

    def simulate(self):
        while self.continue_playing():
            self.shoot()
            for player in self.players:
                if self.continue_betting(player):
                    log = Log()
                    player.strategy(self)
                    log.pre_roll(self, player)
                    self.roll_status = self.evaluate_roll(player)
                    log.post_roll(self, player)
                    player.catalogue(self, log)
                    self.table_status.append(self.roll_status[2])
            self.assess_post_roll()

        for player in self.players:
            print player.__doc__
            player.tabulate()
            self.log(player)

    def evaluate_roll(self, player):
        if player.point is None:
            if self.dice.total in NATURALS:
                delta = player.bet.assess_naturals(self.dice, player)
            elif self.dice.total in CRAPS:
                delta = player.bet.assess_craps(player)
            elif self.dice.total in BOXES:
                delta = player.bet.assess_box(self.dice, player)
            else:
                raise Exception('Invalid Roll')
        else:
            if self.dice.total == SEVEN:
                delta = player.bet.assess_seven_out(player)
            elif self.dice.total == YOLEVEN:
                delta = player.bet.assess_yoleven(player)
            elif self.dice.total in CRAPS:
                delta = player.bet.assess_craps(player)
            elif self.dice.total in BOXES:
                delta = player.bet.assess_box(self.dice, player)
            else:
                raise Exception('Invalid Roll')
        player.log_bankroll()
        return delta

    def log(self, player):
        print 'POINTS WON: {}\t\tSEVEN OUTS: {}'.format(self.points_made, self.seven_outs)
        print 'NATURALS: {}\t\tCRAPS: {}'.format(self.come_out_naturals, self.come_out_craps)
        print 'LONGEST ROLL: {}\tAVG ROLL: {}'.format(self.longest_roll, self.rolls / float(self.shooters))
        line_plot(player.bankroll_history)
        # pie_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values())
        # bar_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values(), 11)

    def assess_post_roll(self):
        if self.table_status and len(set(self.table_status)) != 1:
            raise Exception('Invalid Roll Calculation')

        self.rolls += 1

        if self.table_status[0] == 'POINT':
            self.points_made += 1
        elif self.table_status[0] == 'SEVEN_OUT':
            self.update_seven_out_stats()
        elif self.table_status[0] == 'NATURALS':
            self.come_out_naturals += 1
        elif self.table_status[0] == 'CRAPS':
            self.come_out_craps += 1

        self.table_status = []

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
                if self.rolls >= self.max_rolls and self.dice.history[self.rolls - 1] == 7:
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
        self.seven_outs += 1
        self.shooters += 1
        self.longest_roll = max(self.longest_roll, self.dice.current_roll)
        self.dice.current_roll = 0
