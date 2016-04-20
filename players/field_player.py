from players.player import Player


class FieldPlayer(Player):
    """Field Player - Plays Martingale strategy on the field.\nDefault : Doubles on loss. Resets on win."""

    def __init__(self, bankroll=500):
        super(FieldPlayer, self).__init__(bankroll)
        # print FieldPlayer.__doc__
        self.last_bet = 0

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum
        current_bet = bet.get_field_bet()

        if self.last_bet == 0:
            bet.make_field_bet(self, amount)
            self.last_bet = amount
        elif current_bet == 0:
            bet.make_field_bet(self, self.last_bet * 2)
            self.last_bet *= 2
        elif current_bet > amount:
            self.add_money(current_bet)
            bet.clear_field_bet()
            bet.make_field_bet(self, amount)
            self.last_bet = amount
        elif current_bet == amount:
            pass

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        come = 'F [{}]'.format(bet.field)
        wager = " ".join((str(wager), str(come)))
        return wager
