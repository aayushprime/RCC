import argparse, sys
from transformations import scale, rotate, translate
from clipping import clipping

parser = argparse.ArgumentParser(description="Drawing lines.")
parser.add_argument("-f", type=str, default="hw1.ps", help="Input file name.")
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
for line in lines[begin + 1 : end]:
    line = line.strip()
    if line == "":
        continue
    x1, y1, x2, y2, command = line.split(" ")
    if command == "Line":
        x1, y1, x2, y2 = apply_transformation(int(x1), int(y1), int(x2), int(y2))
        clipped = clipping(x1, y1, x2, y2, args.a, args.b, args.c, args.d)
        if clipped is None:
            pass
        else:
            x1, y1, x2, y2 = clipped
            outputs.append((x1, y1, x2, y2))
    else:
        pass

output_begin = f"""%!PS-Adobe-3.0
%%BeginSetup
  << /PageSize [{xsize} {ysize}] >> setpagedevice
%%EndSetup

%%%BEGIN
"""
output_end = """
stroke
%%%END

"""

print(output_begin)
for output in outputs:
    x1, y1, x2, y2 = output
    print(f"{x1} {y1} moveto")
    print(f"{x2} {y2} lineto")
print(output_end)
