from util import *
from netClasses import *
from heapq import *
import parsing
import random


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

    class Path(object):

        """docstring for Path"""

        def __init__(self):
            # super(Path, self).__init__()
            self.p = []
            self.cost = 0

        def add(self, np):
            self.cost += np.inter_peak
            if self.p and np.line != self.p[-1].line:
                self.cost += 2
            # self.p += [np]
            self.p.append(np)

        def pop_copy(self):
            res = Path()
            for x in range(len(self.p) - 1):
                res.add(self.p[x])
            return res
    path = Path()
    pq = []
    fixed = {}
    while start != end:
        if start.name not in fixed:
            fixed[start.name] = path.cost
            for conn in start.connections:
                if conn.end.name not in fixed:
                    path.add(conn)
                    heappush(pq, (path.cost, path))
                    path = path.pop_copy()
        if len(pq) == 0:
            return [], float('inf')
        cost, path = heappop(pq)
        start = path.p[-1].end
    return path.p, path.cost


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


def plot_degree_distribution(ug):
    import numpy as np
    import matplotlib.pyplot as plt
    degrees = degree_distribution(ug)
    freq = [0] * max(degrees)
    degs = range(0, max(degrees))
    print freq
    for i in degrees:
        freq[i - 1] += 1
    print len(degs), len(freq)
    fig = plt.figure()
    fig.suptitle('Degree distribution', fontsize=14, fontweight='bold')
    ax = fig.add_subplot(111)
    fig.subplots_adjust(top=0.85)
    ax.set_xlabel('Degree')
    ax.set_ylabel('Frequency')
    ax.plot(degs, freq)
    plt.show()
    print freq


def generate_people(ug, n):
    people = []
    for i in range(n):
        start = ug.stations[random.choice(list(ug.stations.keys()))]
        end = ug.stations[random.choice(list(ug.stations.keys()))]
        people.append(Person(start, end))
    return people


def random_remove_connections(ug, n):
    rems = set()
    for i in range(n):
        station = ug.stations[random.choice(list(ug.stations.keys()))]
        if not station.connections:
            continue
        rconn = random.choice(list(station.connections))
        rems.add(rconn)
        for station in ug.stations:
            s = ug[station]
            if rconn in s.connections:
                s.connections.remove(rconn)
    return rems


def replace_connections(ug, conns):
    for conn in conns:
        ug[conn.start.name].connections.add(conn)


def average_travel_time(ug, people):
    num_people = len(people)
    total_cost = 0.0
    for person in people:
        p, cost = path(ug, person.start, person.end)
        if p == []:
            num_people -= 1
            continue
        total_cost += cost
    return total_cost / num_people, num_people


def visualise(ug):
    import pygraphviz as pgv
    G = pgv.AGraph(strict=False)
    # G.node_attr['shape'] = 'Mcircle'
    for station in ug.stations:
        s = ug[station]
        for conn in s.connections:
            G.add_edge(
                conn.start, conn.end, color=__color_for_line[conn.line.name])
    G.draw('gviz.png', prog='neato')


def random_failures_to_file(ug):
    out = open('random_failures.txt', 'w')
    # print average_travel_time(ug, people)
    for j in xrange(100):
        num_people = 1000
        people = generate_people(ug, num_people)

        for i in xrange(100):
            removed = random_remove_connections(ug, i)
            ave_time, num_people = average_travel_time(ug, people)
            print i, ave_time, num_people
            out.write(str((ave_time, num_people)))
            out.write('\n')
            replace_connections(ug, removed)
        out.write('\n')


def degree_failures(ug):
    out = open('fail_degree.txt', 'w')
    for i in xrange(100):
        num_people = 1000
        people = generate_people(ug, num_people)

        connections = [y for x in ug.stations for y in list(ug[x].connections)]
        for c in connections:
            c.start.connections.remove(c)
            ave_time, num_people = average_travel_time(ug, people)
            ldegree, rdegree = len(c.start.connections), len(c.end.connections)
            out.write(str((ave_time, num_people, ldegree, rdegree)))
            print str((ave_time, num_people, ldegree, rdegree))
            out.write('\n')
            c.start.connections.add(c)
        out.write('\n')


def line_fail(ug):
    out = open('line_fail.txt', 'w')
    for i in xrange(100):
        num_people = 1000
        people = generate_people(ug, num_people)
        for line in ug.lines:
            line_name = ug.lines[line].name
            lconnections = [y for x in ug.stations for y in list(
                ug[x].connections) if y.line.name == line_name]
            # print map(lambda x: x.start.name, sorted(lconnections, key=lambda x: x.end.name))
            # ll = lconnections[:len(lconnections) / 2]
            # rr = lconnections[len(lconnections) / 2:]
            # for half in [ll, rr]:
            for c in lconnections:
                if c in c.start.connections:
                    c.start.connections.remove(c)
                    print 'removed'
            ave_time, num_people = average_travel_time(ug, people)
            out.write(str((ave_time, num_people, line_name)))
            print str((ave_time, num_people, line_name))
            for c in lconnections:
                c.start.connections.add(c)
        out.write('\n')


def terrorism(ug):
    out = open('terrorism.txt', 'w')
    connections = set(
        [y for x in ug.stations for y in list(ug[x].connections)])
    top_10_stations = map(lambda x: ug[x].name, sorted(
        ug.stations, key=lambda x: len(ug[x].connections)))[-10:]

    for i in xrange(100):

        num_people = 1000
        people = generate_people(ug, num_people)
        for s in top_10_stations:
            curr = ug[s]
            removed = set()
            for c in connections:
                if c.end.name == curr.name:
                    c.start.connections.remove(c)
                    removed.add(c)
            ave_time, num_people = average_travel_time(ug, people)
            out.write(str((ave_time, num_people, curr.name)))
            print str((ave_time, num_people, curr.name))
            for c in removed:
                c.start.connections.add(c)

            for c in connections:
                if c.end.name == curr.name:
                    c.start.connections.remove(c)
                    removed.add(c)

            for s2 in top_10_stations:
                if s != s2:
                    curr2 = ug[s2]
                    removed2 = set()
                    for c in connections:
                        if c.end.name == curr2.name:
                            c.start.connections.remove(c)
                            removed2.add(c)
                    ave_time, num_people = average_travel_time(ug, people)
                    out.write(
                        str((ave_time, num_people, curr.name, curr2.name)))
                    print str((ave_time, num_people, curr.name, curr2.name))
                    for c in removed2:
                        c.start.connections.add(c)

            for c in removed:
                c.start.connections.add(c)
            out.write('\n')


    # for i in xrange(100):
    #     num_people = 1000
    #     people = generate_people(ug, num_people)
__color_for_line = {'northern': 'black',
                    'central': 'red',
                    'hammersmith_&_city': 'pink',
                    'jubilee': 'dimgrey',
                    'bakerloo': 'brown',
                    'district': 'green',
                    'metropolitan': 'purple',
                    'east_london': 'orange',
                    'piccadilly': 'blue',
                    'victoria': 'royalblue',
                    'circle': 'yellow',
                    'waterloo_&_city': 'turquoise'}


def main():
    ug = parsing.load_underground()
    # for l in ug.lines:
    #     print l
    # plot_degree_distribution(ug)
    # for line in ug.lines:
    #   print line

    # print len(ug.stations)
    # ug['belsize_park'].pprint()

    # p, cost = path(ug, ug['belsize_park'], ug['green_park'])
    # for k in p:
    #     print k, k.min_time
    # print cost

# twopi, gvcolor, wc, ccomps, tred, sccmap, fdp, circo, neato, acyclic,
# nop, gvpr, dot, sfdp.

    try:
        random_failures_to_file(ug)
    except Exception, e:
        pass
    try:
        degree_failures(ug)
    except Exception, e:
        pass
    try:
        line_fail(ug)
    except Exception, e:
        pass
    try:
        terrorism(ug)
    except Exception, e:
        pass

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
