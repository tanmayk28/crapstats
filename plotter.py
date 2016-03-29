from matplotlib import pyplot
from numpy import *
import bisect


def line_plot(x, y=None):
    if y is None:
        y = x
        x = xrange(1, x.__len__() + 1, 1)
    pyplot.plot(x, y)
    pyplot.draw()
    pyplot.pause(1)
    raw_input()
    pyplot.close()


def scatter_plot(x, y):
    pyplot.plot(x, y, 'b.')
    pyplot.xlim(min(x) - 1, max(x) + 1)
    pyplot.ylim(min(y) - 1, max(y) + 1)
    pyplot.show()


def bar_plot(labels, data):
    pos = arange(len(data))
    pyplot.xticks(pos + 0.4, labels)
    pyplot.bar(pos, data)
    pyplot.show()


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
    pyplot.figure(figsize=(7, 7))
    pyplot.pie(data, labels=labels, autopct='%1.2f%%')
    pyplot.show()
