CRAPS = (2, 3, 12)
BOXES = (4, 5, 6, 8, 9, 10)
NATURALS = (7, 11)
SEVEN = 7
YOLEVEN = 11

ODDS = {
    'pass': (1, 1),
    'come': (1, 1),
    'place': {
        6: (7, 6), 8: (7, 6),
        5: (7, 5), 9: (7, 5),
        4: (9, 5), 10: (9, 5)
    },
    'odds': {
        6: (6, 5), 8: (6, 5),
        5: (3, 2), 9: (3, 2),
        4: (2, 1), 10: (2, 1)
    }
}


# TODO Props, Hardways, DontCome, Lays, Field

class Bet(object):
    def __init__(self):
        self.passLine = 0
        self.dontPassLine = 0
        self.field = 0
        self.come = 0
        self.dontCome = 0
        self.place = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
        self.lay = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
        self.comeOdds = {4: [0, 0], 5: [0, 0], 6: [0, 0], 8: [0, 0], 9: [0, 0], 10: [0, 0]}
        self.dontComeOdds = {4: [0, 0], 5: [0, 0], 6: [0, 0], 8: [0, 0], 9: [0, 0], 10: [0, 0]}
        self.hardways = {4: 0, 6: 0, 8: 0, 10: 0}

    def make_pass_bet(self, player, amount):
        self.passLine += player.use_money(amount)

    def make_come_bet(self, player, amount):
        self.come += player.use_money(amount)

    def make_place_bet(self, player, number, amount):
        if player.point == number:
            return
        amount = self.find_next_multiple(number, amount)
        if self.place[number] != 0:
            amount -= self.place[number]
        self.place[number] += player.use_money(amount)

    def make_across_place_bet(self, player, amount):
        for number in BOXES:
            self.make_place_bet(player, number, amount)

    def make_dont_pass_bet(self, player, amount):
        self.dontPassLine += player.use_money(amount)

    def make_dont_come_bet(self, player, amount):
        self.dontCome += player.use_money(amount)

    def establish_pass_odds(self, player, amount):
        self.comeOdds[player.point][0] = self.passLine
        self.passLine = 0

        self.comeOdds[player.point][1] = player.use_money(amount)

    def establish_come_odds(self, number, player):
        amount = player.get_odds(number, self.come)
        self.comeOdds[number][0] = self.come
        self.come = 0

        self.comeOdds[number][1] = player.use_money(amount)

    def establish_dont_pass_odds(self, player, amount):
        self.dontComeOdds[player.point][0] = self.dontPassLine
        self.dontPassLine = 0

        self.dontComeOdds[player.point][1] = player.use_money(amount)

    def establish_dont_come_odds(self, number, player):
        amount = player.get_odds(number, self.dontCome)
        self.dontComeOdds[number][0] = self.dontCome
        self.dontCome = 0

        self.dontComeOdds[number][1] = player.use_money(amount)

    def assess_box(self, dice, player):
        status = None
        number = dice.total
        if player.point is None:
            player.point = number
        else:
            if number == player.point:
                status = 'POINT'
                player.point = None

        payout = self.payout_come_bet(number)
        payout += self.payout_place_bet(number)
        loss = self.clear_dont_come_bet(number)

        player.add_money(payout)

        self.establish_come_odds(number, player)
        self.establish_dont_come_odds(number, player)

        return payout, loss, status

    def assess_seven_out(self, player):
        status = 'SEVEN_OUT'
        self.passLine = 0
        player.point = None

        loss = self.clear_come_bets()
        loss += self.clear_place_bets()
        loss += self.clear_dont_come_line()
        payout = self.payout_dont_come_bets()
        payout += self.payout_lay_bet()
        payout += self.payout_come_line()

        player.add_money(payout)
        return payout, loss, status

    def assess_yoleven(self, player):
        payout = self.payout_come_line()
        loss = self.dontCome
        self.dontCome = 0

        player.add_money(payout)

        return payout, loss, None

    def assess_naturals(self, dice, player):
        payout = loss = 0
        status = 'NATURALS'
        if self.passLine > 0:
            payout += self.passLine * 2
            self.passLine = 0

        if self.dontPassLine > 0:
            loss += self.dontPassLine
            self.dontPassLine = 0

        if dice.total == SEVEN:
            p, l = self.assess_come_out_seven()
            payout += p
            loss += l

        player.add_money(payout)
        return payout, loss, status

    def assess_come_out_seven(self):
        payout = loss = 0

        loss += sum([v[0] for k, v in self.comeOdds.iteritems()])
        payout += sum([v[1] for k, v in self.comeOdds.iteritems()])
        self.comeOdds = {k: [0, 0] for k, v in self.comeOdds.iteritems()}

        payout += self.payout_dont_come_bets()

        return payout, loss

    def assess_craps(self, dice, player):
        number = dice.total
        payout = loss = 0
        status = None
        if self.passLine > 0:
            loss += self.passLine
            self.passLine = 0
            status = 'CRAPS'

        if self.dontPassLine > 0:
            if number == 12:
                payout += self.dontPassLine
            else:
                payout += self.dontPassLine * 2
            self.dontPassLine = 0
            status = 'CRAPS'

        if number == 12:
            payout += self.dontCome
            self.dontCome = 0
        else:
            payout += self.payout_dont_come_line()
        loss += self.clear_come_line()

        player.add_money(payout)
        return payout, loss, status

    def payout_come_bet(self, number):
        bet = self.comeOdds[number][0]
        odds = self.comeOdds[number][1]
        payout = bet + self.odds_calculation(bet, ODDS['come'])
        payout += odds + self.odds_calculation(odds, ODDS['odds'][number])
        self.comeOdds[number][0] = self.comeOdds[number][1] = 0
        return payout

    def payout_place_bet(self, number):
        return self.odds_calculation(self.place[number], ODDS['place'][number])

    def payout_dont_come_bets(self):
        payout = 0
        for number in BOXES:
            bet = self.dontComeOdds[number][0]
            odds = self.dontComeOdds[number][1]
            payout += bet + self.odds_calculation(bet, ODDS['come'])
            payout += odds + self.odds_calculation(odds, tuple(reversed(ODDS['odds'][number])))
            self.dontComeOdds[number][0] = self.dontComeOdds[number][1] = 0
        return payout

    def payout_lay_bet(self):
        payout = 0
        for number in BOXES:
            payout += self.odds_calculation(self.lay[number], tuple(reversed(ODDS['place'][number])))
        return payout

    def payout_come_line(self):
        payout = self.come + self.odds_calculation(self.come, ODDS['come'])
        self.come = 0
        return payout

    def payout_dont_come_line(self):
        payout = self.dontCome + self.odds_calculation(self.dontCome, ODDS['come'])
        self.dontCome = 0
        return payout

    def clear_come_bets(self):
        loss = sum([sum(v) for k, v in self.comeOdds.iteritems()])
        self.comeOdds = {k: [0, 0] for k, v in self.comeOdds.iteritems()}
        return loss

    def clear_place_bets(self):
        loss = sum([v for k, v in self.place.iteritems()])
        self.place = {k: 0 for k, v in self.place.iteritems()}
        return loss

    def clear_come_line(self):
        loss = self.come
        self.come = 0
        return loss

    def clear_dont_come_bet(self, number):
        loss = sum(self.dontComeOdds[number])
        self.dontComeOdds[number] = [0, 0]
        return loss

    def clear_dont_come_line(self):
        loss = self.dontCome
        self.dontCome = 0
        return loss

    def get_wager(self):
        wager = self.passLine + self.dontPassLine + self.field + self.come + self.dontCome
        wager += sum(self.place.values()) + sum(self.lay.values()) + sum(self.hardways.values())
        wager += sum([sum(v) for k, v in self.comeOdds.iteritems()])
        wager += sum([sum(v) for k, v in self.dontComeOdds.iteritems()])
        return wager

    def get_total_come_bets(self):
        return len([k for k, v in self.comeOdds.iteritems() if sum(v)])

    def get_total_dont_come_bets(self):
        return len([k for k, v in self.dontComeOdds.iteritems() if sum(v)])

    @staticmethod
    def odds_calculation(amount, odds):
        x = odds[0]
        y = odds[1]
        return int(amount / y * x)

    @staticmethod
    def find_next_multiple(number, amount):
        multiplier = ODDS['place'][number][1]
        if amount % multiplier == 0:
            return amount
        return multiplier + (amount - amount % multiplier)
