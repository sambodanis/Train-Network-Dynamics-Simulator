import netClasses as nc
import os

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
        station, connect, line = map(lambda x: x if x.find('_<') == -1 else x[:x.find('_<')], 
                                 map(lambda x: x.lower().strip('\''), k))
        line = line[:-5]
        if station not in stations:
            stations[station] = nc.Station(station)
        # stations[station].add_connection(connect) # Complex connections added later
        
        if line not in stations[station]._lines:
            stations[station].add_line(line)

        if line not in lines:
            lines[line] = nc.Line(line)
        lines[line].add_station(station)

    ug = nc.Underground(lines, stations)
    return ug

def read_station_distance():
    f = open('station_distances.txt', 'rb').read()
    lines = f.split('\n')[1:] # Ignore schema on first line
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
            map(lambda x: '_'.join(x.lower().split(' ')) , [line, conn[1], conn[2], conn[3]])))
        dist = conn[4]
        min_time = conn[5]
        am_peak = conn[6]
        inter_peak = conn[7]
        connections.add(nc.Connection(line=line, start=frm, end=to, direction=direction, 
            dist=dist, min_time=min_time, am_peak=am_peak, inter_peak=inter_peak))
    return connections

def merge_ug_connections(ug, conns):
    for conn in conns:
        if conn._start in ug.stations():
            ug[conn._start]._connections = conn
        else:
            print conn._start, 'not found'

def ug_from_dist_file(conn):
    stations = {}
    lines = {}
    for c in conn:
        if c._start not in stations:
            stations[c._start] = nc.Station(c._start)
        stations[c._start].add_connection(c)

        if c._line not in lines:
            lines[c._line] = nc.Line(c._line)
        # lines[c._line].add_station(c._start)
        lines[c._line].add_station(stations[c._start])
        lines[c._line].directions.add(c._direction)
        c._line = lines[c._line]
        stations[c._start].add_line(c._line)
        c._start = stations[c._start]
    for c in conn:
        c._end = stations[c._end]
    ug = nc.Underground(stations=stations, lines=lines)
    return ug


def load_underground():
    # adjacencies = read_LUGtxt()
    # ug = adj_to_ug(adjacencies)
    connections = read_station_distance()
    # ug = merge_ug_connections(ug, connections)
    ug = ug_from_dist_file(connections)
    print [x._end._name for x in ug['belsize_park']._connections], [x._name for x in ug['belsize_park']._lines]
    return ug


def main():
    load_underground()


    # uground = nc.Underground(net)

    # print net['Belsize_Park']
    # visualise(stations, adjacencies)


if __name__ == '__main__':
    main()