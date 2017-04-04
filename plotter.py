from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, FormatStrFormatter
from matplotlib import style
from numpy import *
from collections import Counter
import bisect
import pandas as pd

# style.use('ggplot')


def line_plot(players):
    for player in players:
        y = player.bankroll_history
        x = xrange(1, player.bankroll_history.__len__() + 1, 1)

        plt.plot(x, y, label=player.__class__.__name__)

    plt.legend()
    plt.title('Bankroll over time')
    plt.ylabel('Bankroll')
    plt.xlabel('Dice Rolls')
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()


def hist_plot(rolls):
    counter = Counter(rolls)
    plt.bar(counter.keys(), counter.values())
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()


def plot_stats(players, dice):
    rolls = dice.history[1:]
    hardways = dice.hardway_history[1:]
    plt.figure(figsize=(16, 6), tight_layout=True).canvas.set_window_title('CrapStats')

    bankroll = plt.subplot2grid((2, 4), (0, 0), rowspan=2, colspan=3)
    dicerolls = plt.subplot2grid((2, 4), (0, 3), rowspan=1, colspan=1)

    # Compute and plot bankroll line graph
    for player in players:
        y = player.bankroll_history
        x = xrange(1, player.bankroll_history.__len__() + 1, 1)

        bankroll.plot(x, y, label=player.__class__.__name__)
        # Display the final bankroll in the line graph
        bankroll.text(x[-1], y[-1], '{0:.0f}'.format(y[-1]),
                      fontsize='small', fontweight='bold', fontstretch='condensed', fontstyle='italic')

    # Compute and plot dicerolls bar graph
    counter = Counter(rolls)
    hardway_counter = Counter(hardways)
    bars = dicerolls.bar(counter.keys(), counter.values())
    hw_bars = dicerolls.bar(hardway_counter.keys(), hardway_counter.values(), color='#d62728')

    # Bankroll line graph text formatting
    bankroll.legend()
    bankroll.set_title('Bankroll history')
    bankroll.set_ylabel('Bankroll')
    bankroll.set_xlabel('Dice Rolls')

    # Dicerolls bar graph text formatting
    major_locator = MultipleLocator(1)
    dicerolls.xaxis.set_major_locator(major_locator)
    dicerolls.set_title('Roll counter')
    dicerolls.set_ylabel('# rolls')
    dicerolls.set_xlabel('Dice Number')
    chart_bottom, chart_top = dicerolls.get_ylim()
    chart_height = chart_top - chart_bottom
    for bar in bars:
        ht = bar.get_height()
        wt = bar.get_width()
        roll_percent = ht + (chart_height * -0.05)
        roll_total = ht + (chart_height * 0.005)
        dicerolls.text(bar.get_x() + wt / 2 + 0.06, roll_percent, '{0:.0f}%'.format(ht/len(rolls) * 100),
                       ha='center', rotation='vertical', fontstyle='oblique', fontstretch='condensed')
        dicerolls.text(bar.get_x() + wt / 2, roll_total, '{0:.0f}'.format(ht),
                       ha='center', fontsize='x-small', fontweight='bold', fontstretch='condensed', fontstyle='italic')
    for bar in hw_bars:
        ht = bar.get_height()
        wt = bar.get_width()
        roll_percent = ht + (chart_height * -0.05)
        roll_total = ht + (chart_height * 0.005)
        dicerolls.text(bar.get_x() + wt / 2, roll_total, '{0:.0f}'.format(ht),
                       ha='center', fontsize='x-small', fontweight='bold', fontstretch='condensed', fontstyle='italic')
    dicerolls.text(3, chart_top + (chart_height * -0.1), 'Total rolls : {}'.format(len(rolls)),
                   ha='center', fontsize='x-small', fontweight='bold', fontstretch='condensed', family='sans')

    # Figure formatting and exit on input
    # plt.tight_layout()
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()


def scatter_plot(x, y):
    plt.plot(x, y, 'b.')
    plt.xlim(min(x) - 1, max(x) + 1)
    plt.ylim(min(y) - 1, max(y) + 1)
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()


def bar_plot(labels, data):
    pos = arange(len(data))
    plt.xticks(pos + 0.4, labels)
    plt.bar(pos, data)
    plt.figure(figsize=(7, 7))
    plt.pie(data, labels=labels, autopct='%1.2f%%')
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()


def histogram_plot(data, bins=None, nbins=5):
    minx, maxx = min(data), max(data)
    space = (maxx - minx) / float(nbins)
    if not bins: bins = arange(minx, maxx, space)
    binned = [bisect.bisect(bins, x) for x in data]
    l = ['%.1f' % x for x in list(bins) + [maxx]] if space < 1 else [str(int(x)) for x in list(bins) + [maxx]]
    displab = [x + '-' + y for x, y in zip(l[:-1], l[1:])]
    bar_plot(displab, [binned.count(x + 1) for x in range(len(bins))])


def bar_chart(x, y, numbins=5):
    datarange = max(x) - min(x)
    bin_width = float(datarange) / numbins
    pos = min(x)
    bins = [0 for i in range(numbins + 1)]

    for i in range(numbins):
        bins[i] = pos
        pos += bin_width
    bins[numbins] = max(x) + 1
    binsum = [0 for i in range(numbins)]
    bincount = [0 for i in range(numbins)]
    binaverage = [0 for i in range(numbins)]

    for i in range(numbins):
        for j in range(len(x)):
            if x[j] >= bins[i] and x[j] < bins[i + 1]:
                bincount[i] += 1
                binsum[i] += y[j]

    for i in range(numbins):
        binaverage[i] = float(binsum[i]) / bincount[i]
    bar_plot(range(numbins), binaverage)


def pie_chart(labels, data):
    plt.figure(figsize=(7, 7))
    plt.pie(data, labels=labels, autopct='%1.2f%%')
    plt.draw()
    plt.pause(1)
    raw_input()
    plt.close()
