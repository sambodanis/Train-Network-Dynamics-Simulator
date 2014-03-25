from util import *
# import heapdict as hd
from heapq import *
import random

class Underground(object):
    """docstring for Underground"""
    
    def __init__(self, lines, stations):
        self._lines = lines
        # self.stations = stations
        self.stations = stations

    def __getitem__(self, station):
        return self.stations[station]

    def get_connection(self, station, line, direction):
        possible_conns = self.stations[station]._connections
        conns = filter(lambda x: x._line == line and 
                      x._direction == direction,
                      possible_conns)
        if len(conns) > 0:
            return random.choice(conns)
        else:
            return None

    def lines(self):
        return self._lines.keys()


    def path(self, start, end):
        visited = set()
        prev = {}
        h = []
        heappush(h, (start, 0))
        # for s in self.stations:
        #   if s.name != start:
        #       heappush(h, (s, float('inf')))
        while len(h) > 0:
            curr, dist = heappop(h)
            print curr, dist
            if curr == end:
                route = []
                while curr != start:
                    route.append(curr)
                    curr, dist = prev[curr]
                route.append(curr)
                route.reverse()
                return route
            for conn in self.stations[curr]._connections:
                print conn,
                alt = dist + conn._min_time
                print alt
                if conn._end not in prev or alt < prev[conn._end][1]:
                    new = (conn._end, alt)
                    heappush(h, new)
                    prev[conn._end] = (curr, dist)
        return None

directions = {'northbound': 'southbound',
              'eastbound': 'westbound',
              'outer': 'inner'}
        
def reverse_direction(direction):
    res = None
    for k in directions:
        print direction, k, directions[k]
        if k == direction:
            res = directions[k]
            break
        elif directions[k] == direction:
            res = k
            break
    print 't', res
    return res

class Train(object):
    """docstring for Train"""
    def __init__(self, _id, start, line, direction):
        self.id = _id
        self.location = start
        self.line = line
        self.direction = direction      

    def reverse_direction(self):
        self.direction = reverse_direction(self.direction)

    def __str__(self):
        return ', '.join([str(self.id), self.location, self.line, self.direction])

    def __repr__(self):
        return self.__str__()

class Connection(object):
    """docstring for Connection"""
    def __init__(self, line, start, end, direction, dist, min_time, am_peak, inter_peak):
        self._start = start
        self._end = end
        self._line = line
        self._direction = direction
        self._dist = float(dist)
        self._min_time = float(min_time)
        self._am_peak = float(am_peak)
        self._inter_peak = float(inter_peak)

    def __str__(self):
        return ' -> '.join([self._start._name, self._end._name])

    def __repr__(self):
        return self.__str__()
        
        
class Station(object):
    """docstring for Station"""
    def __init__(self, name):
        self._name = name
        self._lines = set()
        self._connections = set()

    def __str__(self):
        return self._name

    def __repr__(self):
        return self.__str__()

    def pprint(self):
        print ', '.join([self._name] + 
            ['LINES'] + sorted(list(self._lines)) + 
            ['CONNECTIONS'] + sorted(list(self._connections)))

    def add_connection(self, conn):
        self._connections.add(conn)

    def add_line(self, line):
        self._lines.add(line)

class Line(object):
    """docstring for Line"""
    def __init__(self, name):
        self._name = name
        self.directions = set()
        self._stations = set()

    def __str__(self):
        return self._name

    def __repr__(self):
        return self.__str__()

    def pprint(self):
        print ', '.join(sorted(list(self._stations)))

    def add_station(self, station):
        self._stations.add(station)
        
