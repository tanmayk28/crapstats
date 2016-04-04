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
    passLine = 0
    dontPassLine = 0
    field = 0
    come = 0
    dontCome = 0
    place = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
    lay = {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
    comeOdds = {4: [0, 0], 5: [0, 0], 6: [0, 0], 8: [0, 0], 9: [0, 0], 10: [0, 0]}
    dontComeOdds = {4: [0, 0], 5: [0, 0], 6: [0, 0], 8: [0, 0], 9: [0, 0], 10: [0, 0]}
    hardways = {4: 0, 6: 0, 8: 0, 10: 0}

    def __init__(self):
        pass

    def make_pass_bet(self, table, amount):
        self.passLine += table.player.use_money(amount)

    def make_come_bet(self, table, amount):
        self.come += table.player.use_money(amount)

    def establish_pass_odds(self, table, amount):
        self.comeOdds[table.point][0] = self.passLine
        self.passLine = 0

        self.comeOdds[table.point][1] = table.player.use_money(amount)

    def establish_come_odds(self, number, table):
        amount = table.player.get_odds(number, self.come)
        self.comeOdds[number][0] = self.come
        self.come = 0

        self.comeOdds[number][1] = table.player.use_money(amount)

    def make_place_bet(self, number, table, amount):
        if table.point == number:
            return
        amount = self.find_next_multiple(number, amount)
        if self.place[number] != 0:
            amount -= self.place[number]
        self.place[number] += table.player.use_money(amount)

    def make_across_place_bet(self, table, amount):
        for number in BOXES:
            self.make_place_bet(number, table, amount)

    def assess_box(self, table):
        number = table.dice.total
        if table.point is None:
            table.point = number
        else:
            if number == table.point:
                table.point = None

        payout = self.payout_come_bet(number)
        payout += self.payout_place_bet(number)
        loss = 0

        table.player.add_money(payout)

        self.establish_come_odds(number, table)

        return payout, loss

    def assess_seven_out(self, table):
        self.passLine = 0
        table.point = None

        loss = self.clear_come_bets()
        loss += self.clear_place_bets()
        payout = self.payout_dont_come_bets()
        payout += self.payout_lay_bet()
        payout += self.payout_come_line()

        table.player.add_money(payout)
        table.update_seven_out_stats()
        return payout, loss

    def assess_yoleven(self, table):
        payout = self.payout_come_line()
        loss = 0

        table.player.add_money(payout)

        return payout, loss

    def assess_naturals(self, table):
        payout = loss = 0
        if self.passLine > 0:
            payout += self.passLine * 2
            table.player.add_money(self.passLine * 2)
            self.passLine = 0
            table.naturals_won += 1

        if self.dontPassLine > 0:
            loss += self.dontPassLine
            self.dontPassLine = 0
            table.naturals_lost += 1

        return payout, loss

    def assess_craps(self, table):
        payout = loss = 0
        if self.passLine > 0:
            loss += self.passLine
            self.passLine = 0
            table.craps_lost += 1

        if self.dontPassLine > 0:
            payout += self.dontPassLine * 2
            table.player.add_money(self.dontPassLine * 2)
            self.dontPassLine = 0
            table.craps_won += 1

        loss += self.clear_come_line()

        return payout, loss

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

    def clear_come_bets(self):
        loss = 0
        for come_bet in self.comeOdds.values():
            loss += come_bet[0] + come_bet[1]
            come_bet[0] = 0
            come_bet[1] = 0
        return loss

    def clear_place_bets(self):
        loss = 0
        for number in self.place.keys():
            loss += self.place[number]
            self.place[number] = 0
        return loss

    def clear_come_line(self):
        loss = self.come
        self.come = 0
        return loss

    def get_wager(self):
        wager = self.passLine + self.dontPassLine + self.field + self.come + self.dontCome
        wager += sum(self.place.values()) + sum(self.lay.values()) + sum(self.hardways.values())
        for bet in self.comeOdds.values():
            wager += sum(bet)
        for bet in self.dontComeOdds.values():
            wager += sum(bet)
        return wager

    def get_total_come_bets(self):
        bets = 0
        for bet in self.comeOdds.values():
            if bet[0] > 0:
                bets += 1
        return bets

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
