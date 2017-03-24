from bet import Bet
from tabulate import tabulate
from plotter import *
from collections import OrderedDict


class Player(object):
    """Common base class for all players.\nDefault: 2x odds."""

    def __init__(self, bankroll=500):
        self.bet = Bet()
        self.point = None
        self.bankroll = bankroll

        # stats
        self.max_bank = bankroll
        self.min_bank = bankroll
        self.points_made = 0
        self.seven_outs = 0
        self.come_out_naturals = 0
        self.come_out_craps = 0
        self.longest_roll = 0

        # logging
        self.history = OrderedDict()
        self.bankroll_history = [bankroll]

    def add_money(self, amount):
        self.bankroll += amount
        self.update_max_min()

    def use_money(self, amount):
        if amount > self.bankroll:
            amount = self.bankroll
        self.bankroll -= amount
        self.update_max_min()
        return amount

    def update_max_min(self):
        self.max_bank = max(self.bankroll, self.max_bank)
        self.min_bank = min(self.bankroll, self.min_bank)

    def log_bankroll(self):
        self.bankroll_history.append(self.bankroll)

    def catalogue(self, table, log):
        self.history[table.rolls] = log
        self.longest_roll = max(self.longest_roll, table.dice.current_roll)

    def collect_wager(self):
        self.bankroll += self.bet.get_wager()
        self.log_bankroll()

    def tabulate(self):
        headers = ['#', 'Shooter', 'BankRoll', 'Wager', 'Dice', 'Point', 'Won', 'Lost']
        print tabulate(self.history.values(), headers)
        print 'Wager on table: {}'.format(self.bet.get_wager())
        print '\nBANKROLL: {} --> {}\n'.format(self.bankroll_history[0], self.bankroll_history[-1])
        print 'MAX BANKROLL: {}\tMIN BANKROLL: {}'.format(self.max_bank, self.min_bank)
        print 'POINTS WON: {}\t\tSEVEN OUTS: {}'.format(self.points_made, self.seven_outs)
        print 'NATURALS: {}\t\tCRAPS: {}'.format(self.come_out_naturals, self.come_out_craps)
        print 'LONGEST ROLL: {}\tAVG ROLL: {}'.format(self.longest_roll, self.get_avg_roll())

        # line_plot(self.bankroll_history)
        # pie_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values())
        # bar_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values(), 11)

    def get_avg_roll(self):
        last_log = self.history[self.history.keys()[-1]]
        return last_log.rollNumber / float(last_log.shooter)

    @staticmethod
    def get_come_odds(number, amount):
        if number in (4, 5, 6, 8, 9, 10):
            return 2 * amount

    @staticmethod
    def get_dont_come_odds(number, amount):
        if number in (6, 8):
            return int(2.4 * amount)
        elif number in (5, 9):
            return 3 * amount
        elif number in (4, 10):
            return 4 * amount
