from players.player import Player


class IronCrossPlayer(Player):
    """Iron Cross Player - Plays the field and places 5, 6, 8.\nDefault : Takes all bets down after 5 hits"""

    def __init__(self, bankroll=500):
        super(IronCrossPlayer, self).__init__(bankroll)
        # print IronCrossPlayer.__doc__

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum

        if self.point is None:
            bet.return_place_bets(self)
            bet.return_field_bet(self)
        elif bet.get_wager() == 0:
            bet.make_field_bet(self, amount)
            bet.make_place_bet(self, 5, amount * 1.5, True)
            bet.make_place_bet(self, 6, amount * 1.5, True)
            bet.make_place_bet(self, 8, amount * 1.5, True)
        elif bet.get_field_bet() == 0:
            bet.make_field_bet(self, amount)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        field = 'F [{}]'.format(bet.field)
        place = 'P' + str([k for k, v in bet.place.iteritems() if v])
        wager = " ".join((str(wager), str(place), str(field)))
        return wager
