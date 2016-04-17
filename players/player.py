from bet import Bet
from tabulate import tabulate
from plotter import *


class Player(object):
    """Common base class for all players.
    Default: 2x odds."""

    def __init__(self, bankroll=500):
        self.bet = Bet()
        self.point = None
        self.bankroll = bankroll
        self.max_bank = bankroll
        self.min_bank = bankroll
        self.history = {}
        self.bankroll_history = []

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
        if self.bankroll > self.max_bank:
            self.max_bank = self.bankroll
        if self.bankroll < self.min_bank:
            self.min_bank = self.bankroll

    def log_bankroll(self):
        self.bankroll_history.append(self.bankroll)

    def catalogue(self, table, log):
        self.history[table.rolls] = log

    def tabulate(self):
        headers = ['#', 'Shooter', 'BankRoll', 'Wager', 'Dice', 'Point', 'Won', 'Lost']
        print tabulate(self.history.values(), headers)
        # print '\nBANKROLL:', self.bankroll_history[0], '-->', self.bankroll_history[-1], '\n'
        # print 'MAX BANKROLL:', self.max_bank, '\tMIN BANKROLL:', self.min_bank
        print '\nBANKROLL: {} --> {}\n'.format(self.bankroll_history[0], self.bankroll_history[-1])
        print 'MAX BANKROLL: {}\tMIN BANKROLL: {}'.format(self.max_bank, self.min_bank)

        # line_plot(self.bankroll_history)
        # pie_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values())
        # bar_chart([2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], self.dice.history.values(), 11)

    @staticmethod
    def get_odds(number, amount):
        if number in (4, 5, 6, 8, 9, 10):
            return 2 * amount
