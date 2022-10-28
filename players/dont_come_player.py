from players.player import Player


class DontComePlayer(Player):
    """Dont Come Player - Plays dont pass line with dont come bets with 3x-4x-5x odds.\nDefault : 3 point molly."""

    def __init__(self, bankroll=500, points=3):
        super(DontComePlayer, self).__init__(bankroll)
        # print DontComePlayer.__doc__
        self.max_points = points

    def strategy(self, table):
        bet = self.bet
        amount = table.minimum
        if self.point is None:
            bet.make_dont_pass_bet(self, amount)
        elif bet.dontComeOdds[self.point][1] == 0:
            bet.establish_dont_pass_odds(self, self.get_dont_come_odds(self.point, amount))
            if bet.get_total_dont_come_bets() < self.max_points:
                bet.make_dont_come_bet(self, amount)
        else:
            if bet.get_total_dont_come_bets() < self.max_points:
                bet.make_dont_come_bet(self, amount)

    @staticmethod
    def get_wager(bet):
        wager = bet.get_wager()
        # come = {k: sum(v) for k, v in bet.comeOdds.items() if v[0]}
        dontCome = 'DC' + str([k for k, v in bet.dontComeOdds.items() if v[0]])
        wager = " ".join((str(wager), str(dontCome)))
        return wager

    @staticmethod
    def get_dont_come_odds(number, amount):
        if number in (4, 5, 6, 8, 9, 10):
            return 6 * amount
