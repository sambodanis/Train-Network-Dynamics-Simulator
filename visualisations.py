import numpy as np
import matplotlib.pyplot as plt
f = open('t.txt', 'rb').read()
lines = f.split('\n')
lines = lines[:-1]
time_to_work = [0] * len(lines)

for l, i in enumerate(lines):
    curr = i[1:-1]
    curr = curr.split(', ')
    time_to_work[l] = (float(curr[0]), float(curr[1]))

for i in range(2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(range(len(time_to_work)), map(lambda x: x[i], time_to_work))
    plt.show()
