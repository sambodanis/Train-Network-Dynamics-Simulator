import netClasses as nc
import os
import re


def visualise(stations, adjacencies):
    import pydot
    graph = pydot.Dot(graph_type='graph')
    for station in stations:
        graph.add_node(pydot.Node(station))
    print 'done stations'
    for adj in adjacencies:
        graph.add_edge(pydot.Edge(adj[0], adj[1]))
    print 'done connections'
    graph.write_png('example1_graph.png')


def read_LUGtxt():
    f = open('londonUnderground.txt', 'rb').read()
    stations, adjacencies = map(lambda x: x.split('\n'), f.split('\n\n'))
    adjacencies = map(lambda x: x.strip('()').split(', '), adjacencies)
    return adjacencies


def adj_to_ug(adjacencies):
    stations = {}
    lines = {}
    for k in adjacencies:
        station, connect, line = map(
            lambda x: x if x.find('_<') == -1 else x[:x.find('_<')],
            map(lambda x: x.lower().strip('\''), k))
        line = line[:-5]
        if station not in stations:
            stations[station] = nc.Station(station)
        # stations[station].add_connection(connect) # Complex connections added
        # later

        if line not in stations[station].lines:
            stations[station].add_line(line)

        if line not in lines:
            lines[line] = nc.Line(line)
        lines[line].add_station(station)

    ug = nc.Underground(lines, stations)
    return ug


def read_station_distance():
    f = open('station_distances copy.txt', 'rb').read()
    lines = f.split('\n')[1:]  # Ignore schema on first line
    connections = set()
    for conn in lines:
        conn = conn.split('\t')
        line = conn[0].lower()
        if line[-1] == ' ':
            line = line[:-1]
        if line == 'h & c':
            line = 'Hammersmith & City'
        line, direction, frm, to = map(lambda x: x if x[-1] != '_' else x[:-1],
                                       map(lambda x: x if x.find('_(') == -1 else x[:x.find('_(')],
                                           map(lambda x: '_'.join(x.lower().split(' ')), [line, conn[1], conn[2], conn[3]])))
        dist = conn[4]
        min_time = conn[5]
        am_peak = conn[6]
        inter_peak = conn[7]
        connections.add(
            nc.Connection(line=line, start=frm, end=to, direction=direction,
                          dist=dist, min_time=min_time, am_peak=am_peak, inter_peak=inter_peak))
    return connections


def merge_ug_connections(ug, conns):
    for conn in conns:
        if conn.start in ug.stations():
            ug[conn.start].connections = conn
        else:
            print conn.start, 'not found'


def ug_from_dist_file(conn):
    stations = {}
    lines = {}
    for c in conn:
        if c.start not in stations:
            stations[c.start] = nc.Station(c.start)
        stations[c.start].add_connection(c)

        if c.line not in lines:
            lines[c.line] = nc.Line(c.line)
        lines[c.line].add_station(stations[c.start])
        lines[c.line].directions.add(c.direction)
        c.line = lines[c.line]
        stations[c.start].add_line(c.line)
        c.start = stations[c.start]
    for c in conn:
        c.end = stations[c.end]
    ug = nc.Underground(stations=stations, lines=lines)
    return ug


def calc_capacity(station, year_s_c):
    scale = 1000000  # millions
    # max_capacity = 3.5
    year_s_c *= scale
    daily_capacity = year_s_c / 365
    hours_open = 24 - 5
    average_time_between_trips = 1 / 60.0 * 3
    trips_per_day = hours_open / average_time_between_trips
    # daily_capacity = year_s_c / max_capacity
    momentary_capcity = daily_capacity / trips_per_day
    return momentary_capcity


def add_wiki_capacities(ug):
    f = open('stationListWikipedia.txt', 'rb').read().split('|-')
    stations = map(lambda x: '_'.join(x.split(' || ')[0].
                   split('\n')[1].rstrip(']').
                   split('|')[-1].split(' ')).lower(), f)
    stations = map(lambda x: x if x.find(
        '_(') == -1 else x[:x.find('_(')], stations)
    stations = map(lambda x: ''.join([y for y in x if y != '\'']), stations)
    stations = map(
        lambda x: ''.join([y if y != '-' else '_' for y in x]), stations)
    stations = map(
        lambda x: ''.join([y if y != '.' else '' for y in x]), stations)

    subs = {'heathrow_terminals_1,_2,_3': 'heathrow_123',
            'heathrow_terminal_4': 'heathrow_terminal_four',
            'heathrow_terminal_5': 'heathrow_terminal_five',
            'kings_cross_st._pancras': 'kings_cross_st_pancras'}
    stations = [s if s not in subs else subs[s] for s in stations]
    # for s in stations:
    #     if s in subs:
    #         s = subs[s]
    #         print s
    capacities = map(lambda x: float(re.findall('[0-9]*\.[0-9]+', x)[0]), f)
    total_capacity = sum(capacities)
    s_and_c = zip(stations, capacities)

    for k in s_and_c:
        s, c = k
        if s in ug.stations:
            ug[s].capacity = calc_capacity(ug[s], c)
            # print s, ug[s].capacity

    # If station has no capacity, then set it to average neighbour capacity
    for s in ug.stations:
        station = ug[s]
        if station.capacity == 0:
            a = [x.end.capacity for x in station.connections]
            station.capacity = sum(a) / len(a)


def load_underground():
    # adjacencies = read_LUGtxt()
    # ug = adj_to_ug(adjacencies)
    connections = read_station_distance()
    # ug = merge_ug_connections(ug, connections)
    ug = ug_from_dist_file(connections)

    add_wiki_capacities(ug)

    return ug


def main():
    ug = load_underground()
    # print[x for x in ug['belsize_park'].connections], [x for x in
    # ug['belsize_park'].lines]

    # uground = nc.Underground(net)

    # print net['Belsize_Park']
    # visualise(stations, adjacencies)


if __name__ == '__main__':
    main()
