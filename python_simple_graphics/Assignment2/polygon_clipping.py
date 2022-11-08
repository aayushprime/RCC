def intersection_helper(p1, p2):
    A = p1[1] - p2[1]
    B = p2[0] - p1[0]
    C = p1[0] * p2[1] - p2[0] * p1[1]
    return A, B, -C


def polygon_clipping(outputlist, xmin, ymin, xmax, ymax):
    clipPolygon = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]

    clipPolygonEdges = [
        (clipPolygon[k], clipPolygon[k + 1]) for k in range(len(clipPolygon) - 1)
    ]
    clipPolygonEdges.append((clipPolygon[-1], clipPolygon[0]))

    for clipEdge in clipPolygonEdges:

        def intersection(point, previous_point):
            clipEdgeStart, clipEdgeEnd = clipEdge
            line1 = intersection_helper(point, previous_point)
            line2 = intersection_helper(clipEdgeStart, clipEdgeEnd)
            D = line1[0] * line2[1] - line1[1] * line2[0]
            Dx = line1[2] * line2[1] - line1[1] * line2[2]
            Dy = line1[0] * line2[2] - line1[2] * line2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x, y
            else:
                return None

        def inside(point):
            clipEdgeStart, clipEdgeEnd = clipEdge
            x1, y1 = clipEdgeStart
            x2, y2 = clipEdgeEnd
            x, y = point
            p = (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
            if p < 0:
                return False
            else:
                return True

        inputlist = outputlist
        outputlist = []

        for i in range(len(inputlist)):
            current_point = inputlist[i]
            previous_point = inputlist[(i + 1) % len(inputlist)]

            if inside(previous_point):
                if not inside(current_point):
                    outputlist.append(intersection(current_point, previous_point))
                outputlist.append(previous_point)
            elif inside(current_point):
                outputlist.append(intersection(current_point, previous_point))

    return outputlist


if __name__ == "__main__":
    clipped = polygon_clipping(
        [(0, 0), (150, 0), (150, 150), (0, 150)], 50, 50, 100, 100
    )
    print(clipped)
