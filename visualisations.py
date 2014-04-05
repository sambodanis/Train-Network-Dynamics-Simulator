import numpy as np
import matplotlib.pyplot as plt
# import multipolyfit as mpf

# f = open('t.txt', 'rb').read()
# lines = f.split('\n')
# lines = lines[:-1]
# time_to_work = [0] * len(lines)

# for l, i in enumerate(lines):
#     curr = i[1:-1]
#     curr = curr.split(', ')
#     time_to_work[l] = (float(curr[0]), float(curr[1]))

# for i in range(2):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.plot(range(len(time_to_work)), map(lambda x: x[i], time_to_work))
#     plt.show()

# -----------------------
# Random failures
# -----------------------

aggregate = []
examples = 1  # 40
for i in range(examples):
    filename = 'simulation_results/random_failures' + str(i) + '.txt'
    f = open(filename, 'r').read().split('\n')[:-2]
    if not aggregate:
        aggregate = [[0, 0]] * len(f)
    for j, tup in enumerate(f):
        t = tup[1:-1].split(', ')
        aggregate[j] = [aggregate[j][x] + float(
                        t[x]) for x in range(len(t))]

aggregate = map(
    lambda x: (x[0] / examples, 100 - (x[1] / examples) / 10), aggregate)

fig, ax = plt.subplots()
axes = [ax, ax.twinx()]

colors = ['Red', 'Blue']
labels = ['Average travel time', 'Commuters who cannot get to work']
units = ['Minutes', 'Percentage']
axcol = zip(axes, colors)
plots = []
for i in range(2):
    ax = axcol[i][0]
    plot, = ax.plot(range(len(aggregate)),
                    map(lambda x: x[i], aggregate), color=axcol[i][1], label=labels[i], linewidth=1.5)
    plots.append(plot)
    ax.set_ylabel(units[i], color=axcol[i][1])
    ax.set_xlabel('Failures')

plt.legend(plots, labels, prop={'size': 10})
fig.suptitle(
    'Random engineering failures, ' +
    str(examples) + ' trial' + ('s' if examples > 1 else ''),
    fontsize=18, fontweight='bold')
for x in axes:
    for item in ([x.title, x.xaxis.label, x.yaxis.label] +
                 x.get_xticklabels() + x.get_yticklabels()):
        item.set_fontsize(18)
plt.savefig('Graphs/randomFailures1.jpeg')

# -----------------------
# Line failures
# -----------------------

aggregate = []
station_list = []
examples = 100
for i in range(examples):
    filename = 'simulation_results/line_fail' + str(i) + '.txt'
    f = open(filename, 'r').read().split('\n')[:-2]
    if not aggregate:
        aggregate = [(0, 0, 0)] * len(f)
        station_list = [x[1:-1].split(', ')[-1] for x in f]
    for j, tup in enumerate(f):
        t = tup[1:-1].split(', ')
        aggregate[j] = [aggregate[j][x] + float(
                        t[x]) for x in range(len(t) - 1)]

aggregate = zip(
    map(lambda x: (x[0] / examples, (x[1] / examples) / 10), aggregate), station_list)
for i, a in enumerate(aggregate):
    aggregate[i] = (a[0][0], a[0][1], a[1][1:-1])
aggregate.sort(key=lambda x: x[1])

fig, ax = plt.subplots()

axes = [ax, ax.twinx()]
width = 0.35
colors = ['Red', 'Blue']
labels = ['Average travel time', 'Commuters who get to work']
units = ['Minutes', 'Percentage']
rects1 = axes[0].bar(range(len(aggregate)),
             [x[0] for x in aggregate], width, color='r')

rects2 = axes[1].bar(map(lambda x: x + width, range(len(aggregate))),
             [x[1] for x in aggregate], width, color='b')
ax.set_xticklabels([' '.join(x[2].split('_')).capitalize()
                    for x in aggregate])
ax.set_xticks(map(lambda x: x + width, range(len(aggregate))))
for i, tick in enumerate(ax.xaxis.get_major_ticks()):
    tick.label.set_fontsize(7)
    tick.set_pad((i % 2) * 10 + 2)
plt.legend([rects1, rects2], labels, loc='upper left', prop={'size': 10})
axes[0].set_ylim(35, 39)
axes[1].set_ylim(65, 100)
axes[0].set_ylabel(units[0], color=colors[0])
axes[1].set_ylabel(units[1], color=colors[1])
ax.set_xlabel('Line')
fig.suptitle('Line Failures', fontsize=18, fontweight='bold')
for x in axes:
    for item in ([x.title, x.xaxis.label, x.yaxis.label] +
                 x.get_yticklabels()):
        item.set_fontsize(18)
plt.tight_layout(pad=1.5)
plt.savefig('Graphs/lineFailures.jpeg')

# -----------------------
# Degree failures
# -----------------------

aggregate = []
examples = 5
for i in range(examples):
    filename = 'simulation_results/fail_degree' + str(i) + '.txt'
    f = open(filename, 'r').read().split('\n')[:-2]
    if not aggregate:
        aggregate = [[0, 0, 0]] * len(f)
    for j, tup in enumerate(f):
        t = tup[1:-1].split(', ')
        aggregate[j] = [aggregate[j][x] + float(
                        t[x]) for x in range(len(t) - 2)] + [int(t[2]) + int(t[3])]

aggregate = map(
    lambda x: (x[0] / examples, (x[1] / examples) / 10, x[2]), aggregate)
aggregate.sort(key=lambda x: x[2])
freqs = [None] * max(aggregate, key=lambda x: x[2])[2]

for x in aggregate:
    if not freqs[x[2] - 1]:
        freqs[x[2] - 1] = ([x[0]], [x[1]])
    else:
        freqs[x[2] - 1][0].append(x[0])
        freqs[x[2] - 1][1].append(x[1])

aggregate = map(
    lambda x: (sum(x[0]) / len(x[0]), sum(x[1]) / len(x[1])), freqs)

fig, ax = plt.subplots()

axes = [ax, ax.twinx()]
width = 0.35
colors = ['Red', 'Blue']
labels = ['Average travel time', 'Commuters who get to work']
units = ['Minutes', 'Percentage']
rects1 = axes[0].bar(range(len(aggregate)),
             [x[0] for x in aggregate], width, color='r')

rects2 = axes[1].bar(map(lambda x: x + width, range(len(aggregate))),
             [x[1] for x in aggregate], width, color='b')

ax.set_xticklabels([i + 1 for i, x in enumerate(aggregate)])
ax.set_xticks(map(lambda x: x + width, range(len(aggregate))))
for tick in ax.xaxis.get_major_ticks():
    tick.label.set_fontsize(11)
plt.legend([rects1, rects2], labels, loc='lower right')
axes[0].set_ylim(37.4, 37.7)
axes[1].set_ylim(98, 100)
axes[0].set_ylabel(units[0], color=colors[0])
axes[1].set_ylabel(units[1], color=colors[1])
for x in axes:
    for item in ([x.title, x.xaxis.label, x.yaxis.label] +
                 x.get_yticklabels()):
        item.set_fontsize(18)
ax.set_xlabel('Degree sum of adjacient stations')
fig.suptitle('Link removal by end node degree sum',
             fontsize=18, fontweight='bold')
plt.savefig('Graphs/degreeFailure.jpeg')

# -----------------------
# Terrorism failures
# -----------------------

aggregate = []
examples = 22
for i in range(examples):
    filename = 'simulation_results/terrorism' + str(i) + '.txt'
    f = open(filename, 'r').read().split('\n')[:-2]
    if not aggregate:
        aggregate = [[0, 0, 0]] * len(f)
    for j, tup in enumerate(f):
        t = tup[1:-1].split(', ')
        if t != ['']:
            aggregate[j] = [aggregate[j][x] + float(
                            t[x]) for x in range(2)] + [x[1:-1] for x in t[2:]]

aggregate = map(
    lambda x: (x[0] / examples, (x[1] / examples) / 10, x[2:]), aggregate)

aggregate.sort(key=lambda x: x[2][0])

stations = []
for x in range(9, len(aggregate), 10):
    stations.append(aggregate[x:x + 10])

# row and column sharing
f, axes = plt.subplots(
    5, 2)  # , sharex='col', sharey='row')
width = 0.35


axes = [y for x in axes for y in x]
axes = [[x, x.twinx()] for x in axes]
labels = ['Average travel time', 'Commuters who get to work']
units = ['Minutes', 'Percentage']
colors = ['r', 'b']
lines = []
plt.locator_params(nbins=len(stations))
i = 0
for axx in axes:
    for k, ax in enumerate(axx):
        lines.append(
            ax.bar(map(lambda x: x + k * width, range(len(stations[i]))),
                   [x[k] for x in stations[i]], width, color=colors[k]))
        ax.set_ylabel(units[k], color=colors[k])
        for z, item in enumerate([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_yticklabels()):
                if z == 0:
                    item.set_fontsize(4)
                else:
                    item.set_fontsize(8)
        if k == 0:
            ax.set_ylim(30, 50)
            ax.set_xticklabels([' '.join(x[2][-1].split('_')).capitalize()
                               for x in stations[i]])
            ax.set_xticks(map(lambda x: x + width, range(len(stations[i]))))
            ax.set_title(
                ' '.join(stations[i][0][2][0].split('_')).capitalize())
            for k, tick in enumerate(ax.xaxis.get_major_ticks()):
                tick.label.set_fontsize(5)
                tick.set_pad((k % 2) * 5 + 5)
        else:
            ax.set_ylim(80, 100)
    i += 1
f.suptitle('Terrorist Attacks', weight='extra bold')
f.tight_layout()
plt.figlegend(lines, labels,
              ncol=5, labelspacing=0.1, loc=(.25, -0.01), prop={'size': 8})

plt.savefig('Graphs/terrorism.jpeg')
