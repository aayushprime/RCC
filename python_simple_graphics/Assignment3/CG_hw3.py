import argparse, sys
from dda import DDA
from transformations import scale, rotate, translate, interpolate
from polygon_clipping import polygon_clipping
from scanline import scanLine
from collections import defaultdict

parser = argparse.ArgumentParser(description="Drawing lines.")
parser.add_argument("-f", type=str, default="hw3.ps", help="Input file name.")
parser.add_argument("-s", type=float, default=1.0, help="Scaling factor about origin.")
parser.add_argument(
    "-r", type=int, default=0, help="Rotate in degrees CCwise about origin."
)
parser.add_argument("-m", type=int, default=0, help="Translation in X.")
parser.add_argument("-n", type=int, default=0, help="Translation in Y.")
parser.add_argument("-a", type=int, default=0, help="Lower bound in X.")
parser.add_argument("-b", type=int, default=0, help="Lower bound in Y.")
parser.add_argument("-c", type=int, default=499, help="Upper bound in X.")
parser.add_argument("-d", type=int, default=499, help="Upper bound in Y.")


parser.add_argument(
    "-j",
    type=int,
    default=0,
    help="lower bound in the x dimension of the viewport window.",
)
parser.add_argument(
    "-k",
    type=int,
    default=0,
    help="lower bound in the y dimension of the viewport window.",
)
parser.add_argument(
    "-o",
    type=int,
    default=200,
    help="upper bound in the x dimension of the viewport window.",
)
parser.add_argument(
    "-p",
    type=int,
    default=200,
    help="upper bound in the y dimension of the viewport window.",
)


args = parser.parse_args()

# screen size
xsize = args.c - args.a + 1
ysize = args.d - args.b + 1

# read in the file
try:
    f = open(args.f, "r")
    lines = f.readlines()
except:
    print("Error reading file.", file=sys.stderr)
    sys.exit()


def apply_transformation(x1, y1, x2, y2):
    # order of operations
    # Scale, Rotate, Translate

    x1, y1 = scale(x1, y1, args.s)
    x2, y2 = scale(x2, y2, args.s)
    x1, y1 = rotate(x1, y1, args.r)
    x2, y2 = rotate(x2, y2, args.r)
    x1, y1 = translate(x1, y1, args.m, args.n)
    x2, y2 = translate(x2, y2, args.m, args.n)
    return x1, y1, x2, y2


outputs = []

# process the lines
begin = list(map(lambda x: "%%%BEGIN" in x.strip(), lines)).index(True)
end = list(map(lambda x: "%%%END" in x.strip(), lines)).index(True)

# parse postscript into polygons
output = []
i = 0
for line in lines[begin + 1 : end]:
    line = line.strip()
    if line == "":
        continue
    if line == "stroke":
        outputs.append(output)
        output = []
        continue
    x, y, command = " ".join(line.split()).split(" ")
    if command in ["moveto", "lineto"]:
        x, y = int(x), int(y)
        x, y = scale(x, y, args.s)
        x, y = rotate(x, y, args.r)
        x, y = translate(x, y, args.m, args.n)
        output.append((x, y))
    else:
        pass

poly_out = []
for poly in outputs:
    clipped_poly = polygon_clipping(poly, args.a, args.b, args.c, args.d)
    poly_out.append(clipped_poly)

# screen buffer array
screen_buffer = [[0 for _ in range(501)] for _ in range(501)]

# world to viewport transformation
for poly in poly_out:
    viewport_poly = []
    for point in poly:
        x, y = point
        x = int(interpolate(x, args.a, args.c, args.j, args.o))
        y = int(interpolate(y, args.b, args.d, args.k, args.p))
        viewport_poly.append((x, y))

    if viewport_poly:
        viewport_polyE = [
            (viewport_poly[k], viewport_poly[k + 1])
            for k in range(len(viewport_poly) - 1)
        ]
        # polygon edges
        viewport_polyE.append((viewport_poly[-1], viewport_poly[0]))

        # scanline filling algorithm
        # find yman and ymin
        ymax = max([max(x[0][1], x[1][1]) for x in viewport_polyE])
        ymin = min([min(x[0][1], x[1][1]) for x in viewport_polyE])
        # create an edge table
        t_edges = defaultdict(list)
        for edge in viewport_polyE:
            x, y = edge[0]
            x1, y1 = edge[1]
            if y > y1:
                x, y, x1, y1 = x1, y1, x, y
            if y == y1:
                continue
            if x1 == x:
                slope_inv = 0
            else:
                slope_inv = (x1 - x) / (y1 - y)

            t_edges[y].append([x, x, y1, slope_inv])

        for point in scanLine(t_edges, ymin, ymax):
            screen_buffer[point[0]][point[1]] = 1

        # DDA LINE ONLY
        # for edge in viewport_polyE:
        #     x1, y1 = edge[0]
        #     x2, y2 = edge[1]
        #     for point in DDA(x1, y1, x2, y2):
        #         screen_buffer[point[0] - 1][point[1] - 1] = 1

# write screen buffer
print("P1")
print("501 501")
for row in list(zip(*screen_buffer))[::-1]:
    for pixel in row:
        print(pixel, end=" ")
    print("")
