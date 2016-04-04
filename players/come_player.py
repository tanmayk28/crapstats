from players.player import Player


class ComePlayer(Player):
    """Come Player - Plays pass line with come bets with 3x-4x-5x odds.\nDefault : 3 point molly strategy."""

    def __init__(self, bankroll=500, points=3):
        super(ComePlayer, self).__init__(bankroll)
        print ComePlayer.__doc__
        self.max_points = points

    def strategy(self, table):
        bet = table.bet
        amount = table.minimum
        if table.point is None:
            bet.make_pass_bet(table, amount)
        elif bet.comeOdds[table.point][1] == 0:
            bet.establish_pass_odds(table, self.get_odds(table.point, amount))
            bet.make_come_bet(table, amount)
        else:
            if bet.get_total_come_bets() < self.max_points:
                bet.make_come_bet(table, amount)

    @staticmethod
    def get_odds(number, amount):
        if number in (6, 8):
            return 5 * amount
        elif number in (5, 9):
            return 4 * amount
        elif number in (4, 10):
            return 3 * amount
