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


aggregate = []
examples = 40
for i in range(examples):
    filename = 'simulation_results/random_failures' + str(i) + '.txt'
    f = open(filename, 'r').read().split('\n')[:-2]
    if not aggregate:
        aggregate = [(0, 0)] * len(f)
    for j, tup in enumerate(f):
        t = tup[1:-1].split(', ')
        aggregate[j] = (aggregate[j][0] + float(
            t[0]), aggregate[j][1] + float(t[1]))

aggregate = map(lambda x: (x[0] / examples, (x[1] / examples) / 10), aggregate)

fig, ax = plt.subplots()
axes = [ax, ax.twinx()]

colors = ['Red', 'Blue']
labels = ['Average travel time', 'Commuters who get to work']
units = ['Minutes', 'Percentage']
axcol = zip(axes, colors)
plots = []
for i in range(2):
    ax = axcol[i][0]
    plot, = ax.plot(range(len(aggregate)),
                    map(lambda x: x[i], aggregate), color=axcol[i][1], label=labels[i])
    plots.append(plot)
    ax.set_ylabel(units[i], color=axcol[i][1])
plt.legend(plots, labels)
plt.show()


# aggregate = []
# for i in range(40):
#     filename = 'simulation_results/fail_degree' + str(i) + '.txt'
#     f = open(filename, 'r').read().split('\n')[:-2]
#     if not aggregate:
#         aggregate = [(0, 0)] * len(f)
#     for j, tup in enumerate(f):
#         t = tup[1:-1].split(', ')
#         aggregate[j] = (aggregate[j][0] + float(
#             t[0]), aggregate[j][1] + float(t[1]))

# aggregate = map(lambda x: (x[0] / 40.0, x[1] / 40.0), aggregate)

# for i in range(2):
#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     ax.plot(range(len(aggregate)), map(lambda x: x[i], aggregate))
#     plt.show()
