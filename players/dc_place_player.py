from players.player import Player


class DCPlacePlayer(Player):
    """DC Place Player - Plays the DC and places the same number"""

    def __init__(self, bankroll=500):
        super(DCPlacePlayer, self).__init__(bankroll)
        # print DCPlacePlayer.__doc__

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum * 6

        if self.point is None and bet.get_total_dont_come_bets() == 0:
            bet.return_place_bets(self)
            pass
        elif bet.get_wager() == 0:
            bet.make_dont_come_bet(self, amount)
        elif bet.get_total_dont_come_bets() == 0:
            bet.return_place_bets(self)
            bet.make_dont_come_bet(self, amount)
        elif bet.get_total_dont_come_bets() == 1 and bet.get_total_place_bets() == 0:
            bet.make_place_bet(self, table.dice.history[-2], amount, True)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        dontCome = 'DC' + str([k for k, v in bet.dontComeOdds.iteritems() if v[0]])
        place = 'P' + str([k for k, v in bet.place.iteritems() if v])
        wager = " ".join((str(wager), str(dontCome), str(place)))
        return wager

    @staticmethod
    def get_dont_come_odds(number, amount):
        return 0