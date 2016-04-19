from players.player import Player


class BasicPlayer(Player):
    """Basic Player - Plays pass line with 2x odds.\nDefault: Places (6, 8)."""

    def __init__(self, bankroll=500):
        super(BasicPlayer, self).__init__(bankroll)
        # print BasicPlayer.__doc__

    def strategy(self, table):
        if self.point is None:
            self.bet.make_pass_bet(self, table.minimum)
        elif self.bet.comeOdds[self.point][1] == 0:
            self.bet.establish_pass_odds(self, table.minimum * 2)
            # self.bet.make_across_place_bet(self, table.minimum)
            self.bet.make_place_bet(self, 6, table.minimum)
            self.bet.make_place_bet(self, 8, table.minimum)
        else:
            # self.bet.make_across_place_bet(self, table.minimum)
            self.bet.make_place_bet(self, 8, table.minimum)
            self.bet.make_place_bet(self, 8, table.minimum)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        come = 'C' + str([k for k, v in bet.comeOdds.iteritems() if v[0]])
        place = 'P' + str([k for k, v in bet.place.iteritems() if v])
        wager = " ".join((str(wager), str(come), str(place)))
        return wager

    @staticmethod
    def get_come_odds(number, amount):
        if number in (4, 5, 6, 8, 9, 10):
            return 2 * amount
