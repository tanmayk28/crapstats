from dice import Dice
from tabulate import tabulate


class Player(object):
    """Common base class for all players"""

    def __init__(self, bankroll=500):
        self.bankroll = bankroll
        self.max_bank = bankroll
        self.min_bank = bankroll
        self.naturals_won = 0
        self.naturals_lost = 0
        self.craps_won = 0
        self.craps_lost = 0
        self.dice = Dice()
        self.history = {}

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

    def shoot(self):
        self.dice.roll()
        return self.dice

    def catalogue(self, table, log):
        self.history[table.rolls] = log

    def tabulate(self):
        headers = ['#', 'Shooter', 'BankRoll', 'Wager', 'Dice', 'Wager', 'BankRoll', 'Won', 'Lost']
        print tabulate(self.history.values(), headers)
        print '\nBANKROLL:', self.history.items()[0][1].start_bank, '-->', self.history.items()[-1][1].end_bank
        print 'MAX BANKROLL:', self.max_bank
        print 'MIN BANKROLL:', self.min_bank
