from util import *
from netClasses import *
from heapq import *
import parsing
import random
# import numpy as np
# import matplotlib.pyplot as plt


class State(object):

    """docstring for State"""

    def __init__(self, ug):
        self.ug = ug
        # self.trains = {}

    def add_train(self, train):
        self.ug.trains.add(train)
        # for s in self.trains:
        #   print self.trains[s][1]

    def connect(self, train):
        t = self.ug.get_connection(train.location, train.line, train.direction)
        if not t:
            train.reverse_direction()
            t = self.ug.get_connection(
                train.location, train.line, train.direction)
        if not t:
            print train
            print train.location.connections
            for conn in train.location.connections:
                print conn
            print train.line.directions
        return t

    def travel(self, time):
        for train in self.ug.trains:
            time_taken = 0.0
            curr_conn = self.connect(train)
            # for train in self.ug.trains:
            #   print train
            # print curr_conn
            while True:
                if (1.0 - train.percent_done) * curr_conn.min_time + time_taken < time:
                    time_taken += (
                        1.0 - train.percent_done) * curr_conn.min_time
                    train.percent_done = 0.0
                    train.location = curr_conn.end
                    curr_conn = self.connect(train)
                    train.location.visitors += 1
                else:
                    train.percent_done = (
                        time - time_taken) / curr_conn.min_time
                    break
            time_taken = 0.0


def path(ug, start, end):
    path = []
    pq = []
    fixed = {}
    # heappush(pq, (0, [start]))
    while start != end:
        if start.name not in fixed:
            fixed[start.name] = sum([x.min_time for x in path])
            for conn in start.connections:
                if conn.end.name not in fixed:
                    path += [conn]
                    heappush(pq, (sum([x.min_time for x in path]), path))
                    path = path[:-1]
        if len(pq) == 0:
            return []
        cost, path = heappop(pq)
        start = path[-1].end
    return path, cost


def degree_distribution(ug):
    degs = sorted([len(ug[x].connections) for x in ug.stations])
    return degs


def generate_trains(ug, n):
    trains = []
    for i in range(n):
        station = ug.stations[random.choice(list(ug.stations.keys()))]
        line = random.choice(list(station.lines))
        direction = random.choice(list(line.directions))
        trains.append(Train(i, station, line, direction))
    return trains


def main():
    ug = parsing.load_underground()
    # for line in ug.lines:
    #   print line
    # degrees = degree_distribution(ug)
    # freq = [0] * 10
    # degs = range(1, 11)
    # print freq
    # for i in degrees:
    #   freq[i-1] += 1
    # plt.plot(degs, freq)
    # plt.show()
    # print len(ug.stations)
    # ug['belsize_park'].pprint()
    p, cost = path(ug, ug['belsize_park'], ug['waterloo'])
    for k in p:
        print k, k.min_time
    print cost

    # s = State(ug)
    # map(lambda x: s.add_train(x), generate_trains(ug, 525))
    # s.add_train(Train(2, 'euston', 'northern', 'southbound'))
    # s.travel(600)
    # for train in s.ug.trains:
    # print train
    # total_v = sum([ug[x].visitors for x in ug.stations])
    # for station in sorted(ug.stations, key=lambda x: ug[x].visitors):
    #     s = ug[station]
    #     print '%s, %d, %.2f%%' % (s.name, s.visitors, float(s.visitors) / total_v * float(100))
    # print 'Station, visitors, percentage of total (%d)' % total_v
    # ug.trains.clear()
    # ug.
    # map(lambda x: s.add_train(x), generate_trains(ug, 1000))
    # s.travel(10)
    # for train in s.ug.trains:
    # print train
    # Floyd Warshall method for reachability
if __name__ == '__main__':
    main()
