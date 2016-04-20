from players.player import Player


class IronCrossPlayer(Player):
    """IronCrossPlayer Player - Plays the field and places 5, 6, 8.\nDefault : Takes all bets down after 5 hits"""

    def __init__(self, bankroll=500):
        super(IronCrossPlayer, self).__init__(bankroll)
        # print IronCrossPlayer.__doc__

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum

        if self.point is None:
            pass
        elif bet.get_wager() == 0:
            bet.make_field_bet(self, amount)
            bet.make_place_bet(self, 5, amount)
            bet.make_place_bet(self, 6, amount)
            bet.make_place_bet(self, 8, amount)
        elif bet.get_field_bet() == 0:
            bet.make_field_bet(self, amount)
        elif bet.get_wager() > amount * 4:
            pass

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        come = 'F [{}]'.format(bet.field)
        wager = " ".join((str(wager), str(come)))
        return wager
