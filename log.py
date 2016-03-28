class Log(object):
    def __init__(self):
        # roll
        self.dice = None
        self.result = None
        self.won = None
        self.lost = None

        # player
        self.start_bank = None
        self.end_bank = None
        self.start_wager = 0
        self.end_wager = 0

        # table
        self.rollNumber = None
        self.shooter = None

    def pre_roll(self, table):
        self.rollNumber = table.rolls
        self.shooter = table.shooters
        self.start_bank = table.player.bankroll
        self.start_wager = table.bet.get_wager()

    def post_roll(self, table):
        self.dice = table.player.dice.total
        self.end_bank = table.player.bankroll
        self.end_wager = table.bet.get_wager()

    def __str__(self):
        log = [self.rollNumber,
               self.shooter,
               self.start_bank,
               self.start_wager,
               self.dice,
               self.end_wager,
               self.end_bank]
        return log.__str__()

    def __iter__(self):
        return iter([self.rollNumber, self.shooter, self.start_bank, self.start_wager,
                     self.dice, self.end_wager, self.end_bank])
