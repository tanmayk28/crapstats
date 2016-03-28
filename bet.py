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

    def establish_pass_odds(self, number, table, amount):
        self.comeOdds[number][0] = self.passLine
        self.passLine = 0

        self.comeOdds[number][1] = table.player.use_money(amount)

    def establish_come_odds(self, number, table, amount):
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

    def assess_seven_out(self, table):
        table.shooters += 1
        self.passLine = 0
        table.point = None

        self.clear_come_bets()
        self.clear_place_bets()
        payout = 0
        payout += self.payout_dont_come_bets()
        payout += self.payout_lay_bet()

        table.player.add_money(payout)

    def assess_naturals(self, table):
        table.player.add_money(self.passLine * 2)
        self.passLine = 0
        table.player.naturals_won += 1

        self.dontPassLine = 0
        table.player.naturals_lost += 1

    def assess_craps(self, table):
        self.passLine = 0
        table.player.craps_lost += 1

        table.player.add_money(self.dontPassLine * 2)
        self.dontPassLine = 0
        table.player.craps_won += 1

    def assess_box(self, table, dice):
        payout = 0
        if table.point is None:
            table.point = dice.total
        else:
            if dice.total == table.point:
                table.point = None

        payout += self.payout_come_bet(dice.total)
        payout += self.payout_place_bet(dice.total)

        # TODO Props and Hardways

        table.player.add_money(payout)

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

    def clear_come_bets(self):
        money_lost = 0
        for come_bet in self.comeOdds.values():
            money_lost += come_bet[0] + come_bet[1]
            come_bet[0] = 0
            come_bet[1] = 0
        return money_lost

    def clear_place_bets(self):
        money_lost = 0
        for number in self.place.keys():
            money_lost += self.place[number]
            self.place[number] = 0
        return money_lost

    def get_wager(self):
        wager = self.passLine + self.dontPassLine + self.field + self.come + self.dontCome
        wager += sum(self.place.values()) + sum(self.lay.values()) + sum(self.hardways.values())
        for bet in self.comeOdds.values():
            wager += sum(bet)
        for bet in self.dontComeOdds.values():
            wager += sum(bet)
        return wager

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
