import math


def scanLine(edge_table, y_min, y_max):
    active_edge = []  # array to store active edge list
    out = []
    # go from y min to y max
    for curr_y in range(y_min, y_max + 1):
        i = 0
        while i < len(active_edge):
            if active_edge[i][2] == curr_y:
                active_edge.pop(i)
            else:
                i += 1
        for e in range(len(active_edge)):
            if e % 2:
                active_edge[e][1] += active_edge[e][3]
                active_edge[e][0] = math.floor(active_edge[e][1])
            else:
                active_edge[e][1] += active_edge[e][3]
                active_edge[e][0] = math.ceil(active_edge[e][1])
        active_edge += edge_table[curr_y]
        active_edge.sort()
        for cur in range(0, len(active_edge) - 1, 2):
            for x in range(active_edge[cur][0], active_edge[cur + 1][0] + 1):
                out.append((x, curr_y))

    return out
