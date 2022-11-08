import argparse

parser = argparse.ArgumentParser(description="Draw smf on viewport.")
parser.add_argument("-f", type=str, default="cube.smf", help="Input file name.")

# view port bounds
parser.add_argument(
    "-j",
    type=int,
    default=0,
    help="Integer lower bound in x dimension of viewport screen coordinates.",
)
parser.add_argument(
    "-k",
    type=int,
    default=0,
    help="Integer lower bound in y dimension of viewport screen coordinates.",
)
parser.add_argument(
    "-o",
    type=int,
    default=500,
    help="Integer upper bound in x dimension of viewport screen coordinates.",
)
parser.add_argument(
    "-p",
    type=int,
    default=500,
    help="Integer lower bound in y dimension of viewport screen coordinates.",
)

# PRP point coordinates
parser.add_argument(
    "-x",
    type=float,
    default=0.0,
    help="floating point x of Projection Reference Point (PRP) in VRC coordinates.",
)
parser.add_argument(
    "-y",
    type=float,
    default=0.0,
    help="floating point y of Projection Reference Point (PRP) in VRC coordinates.",
)
parser.add_argument(
    "-z",
    type=float,
    default=1.0,
    help="floating point z of Projection Reference Point (PRP) in VRC coordinates.",
)

# VRP point coordinates
parser.add_argument(
    "-X",
    type=float,
    default=0.0,
    help="floating point x of View Reference Point (VRP) in world coordinates.",
)
parser.add_argument(
    "-Y",
    type=float,
    default=0.0,
    help="floating point y of View Reference Point (VRP) in world coordinates.",
)
parser.add_argument(
    "-Z",
    type=float,
    default=0.0,
    help="floating point z of View Reference Point (VRP) in world coordinates.",
)

# VPN point coordinates
parser.add_argument(
    "-q",
    type=float,
    default=0.0,
    help="floating point x of View Plane Normal vector (VPN) in world coordinates.",
)
parser.add_argument(
    "-r",
    type=float,
    default=0.0,
    help="floating point y of View Plane Normal vector (VPN) in world coordinates.",
)
parser.add_argument(
    "-w",
    type=float,
    default=-1.0,
    help="floating point z of View Plane Normal vector (VPN) in world coordinates.",
)

# VUP point coordinates
parser.add_argument(
    "-Q",
    type=float,
    default=0.0,
    help="floating point x of View Up Vector (VUP) in world coordinates.",
)
parser.add_argument(
    "-R",
    type=float,
    default=1.0,
    help="floating point y of View Up Vector (VUP) in world coordinates.",
)
parser.add_argument(
    "-W",
    type=float,
    default=0.0,
    help="floating point z of View Up Vector (VUP) in world coordinates.",
)

# We know: VUP is not parallel to VPN
# VRC window bounds
parser.add_argument(
    "-u",
    type=float,
    default=-0.7,
    help="floating point u min of the VRC window in VRC coordinates.",
)
parser.add_argument(
    "-v",
    type=float,
    default=-0.7,
    help="floating point v min of the VRC window in VRC coordinates.",
)
parser.add_argument(
    "-U",
    type=float,
    default=0.7,
    help="floating point u max of the VRC window in VRC coordinates.",
)
parser.add_argument(
    "-V",
    type=float,
    default=0.7,
    help="floating point v max of the VRC window in VRC coordinates.",
)

# perspective projection/parallel projection
parser.add_argument(
    "-P",
    action="store_true",
    help="Use parallel projection. If this flag is not present, use perspective projection",
)

# front and back face of frustum
parser.add_argument(
    "-F",
    type=float,
    default=0.6,
    help="Front face of frustum",
)
parser.add_argument(
    "-B",
    type=float,
    default=-0.6,
    help="Backface of frustum",
)
