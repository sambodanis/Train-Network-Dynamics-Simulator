import numpy as np
import matplotlib.pyplot as plt

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


# aggregate = []
# examples = 40
# for i in range(examples):
#     filename = 'simulation_results/random_failures' + str(i) + '.txt'
#     f = open(filename, 'r').read().split('\n')[:-2]
#     if not aggregate:
#         aggregate = [[0, 0]] * len(f)
#     for j, tup in enumerate(f):
#         t = tup[1:-1].split(', ')
#         aggregate[j] = [aggregate[j][x] + float(
#                         t[x]) for x in range(len(t))]

# aggregate = map(lambda x: (x[0] / examples, (x[1] / examples) / 10), aggregate)

# fig, ax = plt.subplots()
# axes = [ax, ax.twinx()]

# colors = ['Red', 'Blue']
# labels = ['Average travel time', 'Commuters who get to work']
# units = ['Minutes', 'Percentage']
# axcol = zip(axes, colors)
# plots = []
# for i in range(2):
#     ax = axcol[i][0]
#     plot, = ax.plot(range(len(aggregate)),
#                     map(lambda x: x[i], aggregate), color=axcol[i][1], label=labels[i])
#     plots.append(plot)
#     ax.set_ylabel(units[i], color=axcol[i][1])
#     ax.set_xlabel('Failures')
# plt.legend(plots, labels)
# fig.suptitle('Random engineering failures', fontsize=18, fontweight='bold')
# plt.show()

# aggregate = []
# station_list = []
# examples = 100
# for i in range(examples):
#     filename = 'simulation_results/line_fail' + str(i) + '.txt'
#     f = open(filename, 'r').read().split('\n')[:-2]
#     if not aggregate:
#         aggregate = [(0, 0, 0)] * len(f)
#         station_list = [x[1:-1].split(', ')[-1] for x in f]
#     for j, tup in enumerate(f):
#         t = tup[1:-1].split(', ')
#         aggregate[j] = [aggregate[j][x] + float(
#                         t[x]) for x in range(len(t) - 1)]

# aggregate = zip(
#     map(lambda x: (x[0] / examples, (x[1] / examples) / 10), aggregate), station_list)
# for i, a in enumerate(aggregate):
#     aggregate[i] = (a[0][0], a[0][1], a[1][1:-1])
# aggregate.sort(key=lambda x: x[1])

# fig, ax = plt.subplots()

# axes = [ax, ax.twinx()]
# width = 0.35
# colors = ['Red', 'Blue']
# labels = ['Average travel time', 'Commuters who get to work']
# units = ['Minutes', 'Percentage']
# rects1 = axes[0].bar(range(len(aggregate)),
#              [x[0] for x in aggregate], width, color='r')

# rects2 = axes[1].bar(map(lambda x: x + width, range(len(aggregate))),
#              [x[1] for x in aggregate], width, color='b')
# ax.set_xticklabels([x[2] for x in aggregate])
# ax.set_xticks(map(lambda x: x + width, range(len(aggregate))))
# for tick in ax.xaxis.get_major_ticks():
#     tick.label.set_fontsize(11)
# plt.legend([rects1, rects2], labels, loc='lower right')
# axes[0].set_ylim(35, 39)
# axes[1].set_ylim(65, 100)
# axes[0].set_ylabel(units[0], color=colors[0])
# axes[1].set_ylabel(units[1], color=colors[1])
# ax.set_xlabel('Line')
# fig.suptitle('Line Failures', fontsize=18, fontweight='bold')
# plt.show()


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
ax.set_xlabel('Degree sum of adjacient stations')
fig.suptitle('Link removal by end node degree sum',
             fontsize=18, fontweight='bold')
plt.show()
