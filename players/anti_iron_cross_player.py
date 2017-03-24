from players.player import Player


class AntiIronCrossPlayer(Player):
    """Anti Iron Cross Player - Plays the field and hops the 7."""

    def __init__(self, bankroll=500):
        super(AntiIronCrossPlayer, self).__init__(bankroll)
        # print AntiIronCrossPlayer.__doc__

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum

        bet.return_field_bet(self)
        bet.return_place_bets(self)
        bet.make_field_bet(self, amount)
        # bet.make_place_bet(self, 5, amount * 2, True)
        # bet.make_place_bet(self, 6, amount * 2, True)
        # bet.make_place_bet(self, 8, amount * 2, True)
        bet.make_hop_bet(self, 7, amount / 2)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        field = 'F [{}]'.format(bet.field)
        place = 'P' + str([k for k, v in bet.place.iteritems() if v])
        hop = 'H' + str([k for k, v in bet.hop.iteritems() if v])
        wager = " ".join((str(wager), str(hop), str(place), str(field)))
        return wager
