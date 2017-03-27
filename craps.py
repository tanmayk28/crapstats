from table import Table
from players import *

__author__ = 'T'

bankroll = 6000
minimum = 10
max_rolls = 2500

if __name__ == '__main__':
    # rolls = [8, 8, 8, 7, 5, 5, 5, 11, 6, 10, 10, 6, 10, 7, 4, 3, 6, 8, 4, 3, 6, 8, 4, 5, 5, 5, 10, 8, 6,
    #          4, 3, 12, 5, 7, 10, 7, 4, 9, 9, 7, 4, 7, 6, 6, 12, 7, 5, 7, 6, 11, 4, 6, 5, 7, 10, 6, 4, 8,
    #          10, 8, 11, 6, 5, 4, 4, 6, 7, 8, 7, 6, 12, 4, 6, 6, 10, 4, 7, 7, 5, 10, 12, 5, 5, 3, 7]
    rolls = [5, 10, 10, 10, 3, 11, 9, 5, 9, 10, 8, 8, 7]
    players = list()
    players.append(BasicPlayer(bankroll))
    # players.append(ComePlayer(bankroll))
    # players.append(DontComePlayer(bankroll))
    # players.append(FieldPlayer(bankroll))
    # players.append(IronCrossPlayer(bankroll))
    # players.append(AntiIronCrossPlayer(bankroll))
    # players.append(DCPlacePlayer(bankroll))
 
    table = Table(minimum, players, max_rolls, None)
    table.simulate()
