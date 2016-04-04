from table import Table
from players import *

__author__ = 'T'

bankroll = 500
minimum = 5

if __name__ == '__main__':
    player = ComePlayer(bankroll)
    table = Table(minimum, player)
    table.simulate()
