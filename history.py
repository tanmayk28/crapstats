
class History(object):

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

    def __init__(self, bet):
        self.passLine = bet.passLine
        self.dontPassLine = bet.dontPassLine
        self.field = bet.field
        self.come = bet.come
        self.dontCome = bet.dontCome
        self.place = bet.place
        self.lay = bet.lay
        self.comeOdds = bet.comeOdds
        self.dontComeOdds = bet.dontComeOdds
        self.hardways = bet.hardways