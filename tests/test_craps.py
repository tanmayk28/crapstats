from players import *
from table import Table

BANKROLL = 500
MINIMUM = 10

"""Use : python -m pytest tests/"""


def test_place_bets():
    players = [Player(BANKROLL)]
    player = players[0]
    table = Table(MINIMUM, players, None)
    bet = player.bet
    dice = table.dice

    bet.make_place_bet(player, 6, MINIMUM)
    assert bet.get_wager() == 12
    assert bet.place[6] == 12
    assert player.bankroll == 488

    dice.total = 6
    bet.assess_box(table, player)
    assert bet.get_wager() == 12
    assert bet.place[6] == 12
    assert player.bankroll == 502
    assert player.point == 6

    bet.make_place_bet(player, 5, MINIMUM)
    dice.total = 5
    bet.assess_box(table, player)

    bet.make_place_bet(player, 4, MINIMUM)
    dice.total = 4
    bet.assess_box(table, player)

    dice.total = 5
    bet.assess_box(table, player)
    dice.total = 8
    bet.assess_box(table, player)
    dice.total = 9
    bet.assess_box(table, player)
    bet.make_place_bet(player, 10, MINIMUM)

    assert bet.get_wager() == 42
    assert bet.place == {4: 10, 5: 10, 6: 12, 8: 0, 9: 0, 10: 10}
    assert player.bankroll == 518

    bet.make_place_bet(player, 5, MINIMUM)
    bet.make_place_bet(player, 8, MINIMUM)
    bet.make_across_place_bet(player, MINIMUM)

    assert bet.get_wager() == 64
    assert bet.place == {4: 10, 5: 10, 6: 12, 8: 12, 9: 10, 10: 10}
    assert player.bankroll == 496

    bet.assess_seven_out(table, player)

    assert bet.get_wager() == 0
    assert bet.place == {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
    assert player.bankroll == 496


def test_across_place_bets():
    players = [Player(BANKROLL)]
    player = players[0]
    table = Table(MINIMUM, players, None)
    bet = player.bet

    bet.make_across_place_bet(player, MINIMUM)

    assert bet.get_wager() == 64
    assert bet.place == {4: 10, 5: 10, 6: 12, 8: 12, 9: 10, 10: 10}
    assert player.bankroll == 436

    bet.assess_seven_out(table, player)

    assert bet.get_wager() == 0
    assert bet.place == {4: 0, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0}
    assert player.bankroll == 436
