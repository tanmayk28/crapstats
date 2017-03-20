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
        bet.make_field_bet(self, amount)
        bet.make_hop_bet(self, 7, amount / 2)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        field = 'F [{}]'.format(bet.field)
        hop = 'H' + str([k for k, v in bet.hop.iteritems() if v])
        wager = " ".join((str(wager), str(hop), str(field)))
        return wager
