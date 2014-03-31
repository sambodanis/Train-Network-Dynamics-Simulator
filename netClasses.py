from util import *
# import heapdict as hd
from heapq import *
import random


class Underground(object):

    """docstring for Underground"""

    def __init__(self, lines, stations):
        self.lines = lines
        # self.stations = stations
        self.stations = stations
        self.trains = set()

    def __getitem__(self, station):
        return self.stations[station]

    # def add_train(self, train):
    #     self.trains.add(train)

    def get_connection(self, station, line, direction):
        possible_conns = station.connections
        conns = filter(lambda x: x.line == line and
                       x.direction == direction,
                       possible_conns)
        if len(conns) > 0:
            return random.choice(conns)
        else:
            return None

    def lines(self):
        return self.lines.keys()

__directions = {'northbound': 'southbound',
                'eastbound': 'westbound',
                'outer': 'inner'}


def reverse_direction(direction):
    res = None
    for k in __directions:
        if k == direction:
            res = __directions[k]
            break
        elif __directions[k] == direction:
            res = k
            break
    return res


class Train(object):

    """docstring for Train"""

    def __init__(self, _id, start, line, direction, percent_done=0.0):
        self.id = _id
        self.location = start
        self.line = line
        self.direction = direction
        self.percent_done = percent_done

    def reverse_direction(self):
        self.direction = reverse_direction(self.direction)

    def __str__(self):
        return ', '.join([str(self.id), self.location.name, self.line.name, self.direction, str(self.percent_done)])

    def __repr__(self):
        return self.__str__()


class Person(object):

    """docstring for Person"""

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __str__(self):
        return self.start.name + ' -> ' + self.end.name

    def __repr__(self):
        return self.__str__()


class Connection(object):

    """docstring for Connection"""

    def __init__(self, line, start, end, direction, dist, min_time, am_peak, inter_peak):
        self.start = start
        self.end = end
        self.line = line
        self.direction = direction
        self.dist = float(dist)
        self.min_time = float(min_time)
        self.am_peak = float(am_peak)
        self.inter_peak = float(inter_peak)

    def __str__(self):
        return ' '.join([self.start.name, '->', self.end.name, self.line.name, self.direction])

    def __repr__(self):
        return self.__str__()


class Station(object):

    """docstring for Station"""

    def __init__(self, name):
        self.name = name
        self.lines = set()
        self.connections = set()
        self.visitors = 0
        self._capacity = 0
        self.platform_capacity = 0

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        self._capacity = value
        self.platform_capacity = value / (2 * len(self.connections))

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def pprint(self):
        print ', '.join([self.name] +
                        ['LINES'] + map(str, sorted(list(self.lines))) +
                        ['CONNECTIONS'] + map(str, sorted(list(self.connections))))

    def add_connection(self, conn):
        self.connections.add(conn)

    def add_line(self, line):
        self.lines.add(line)


class Line(object):

    """docstring for Line"""

    def __init__(self, name):
        self.name = name
        self.directions = set()
        self.stations = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def pprint(self):
        print ', '.join(sorted(list(self.stations)))

    def add_station(self, station):
        self.stations.add(station)
