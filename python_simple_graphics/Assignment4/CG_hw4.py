from args import parser
from polygon_clipping import polygon_clipping
from utils import get_verts_and_faces
from mathOps import (
    Vector3,
    Vector2,
    cross,
    multiplyMatVec,
    translate,
    scale,
)

# read arguments
args = parser.parse_args()

# read vertices and faces from smf file
with open(args.f, "r") as f:
    lines = f.readlines()

# parse the data into vertices and faces (lists)
vertices, faces = get_verts_and_faces(lines)


# 2d screen mapping
view_port_screen_coordinates_l = Vector2(0, 0)
view_port_screen_coordinates_h = Vector2(500, 500)
x_size, y_size = [501, 501]


# in VRC coordinates
PRP = Vector3(args.x, args.y, args.z)
# args.u args.v args.U and args.V are also in VRC coordinates

# in world coordinates
VRP = Vector3(args.X, args.Y, args.Z)  # look at
VPN = Vector3(args.q, args.r, args.w)
VUP = Vector3(args.Q, args.R, args.W)

# initialization for storing vertices in the pipeline
transformed_vertices = []

# Rotation matrix for view transformation
Ry = cross(cross(VPN.unit_vector(), VUP.unit_vector()), VPN.unit_vector())
R = [
    [*(cross(VUP, VPN).unit_vector()), 0],
    [*(Ry.unit_vector()), 0],
    [*(VPN.unit_vector()), 0],
    [0, 0, 0, 1],
]

for point in vertices:
    # If the model has any transformations local to it apply here
    pass

    # view transform
    transformed_vertex = Vector3(point[0], point[1], point[2]) - VRP
    transformed_vertex = multiplyMatVec(R, transformed_vertex)

    vrp = multiplyMatVec(R, Vector3(0, 0, 0))
    # normalized parallel projection
    if args.P:
        CW = Vector3((args.U + args.u) / 2, (args.V + args.v) / 2, 0)
        DOP = CW - PRP
        Hpar = [
            [1, 0, -DOP.x / DOP.z, 0],
            [0, 1, -DOP.y / DOP.z, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        transformed_vertex = multiplyMatVec(Hpar, transformed_vertex)

        # Tpar transformation
        transformed_vertex = transformed_vertex + Vector3(
            -(args.U + args.u) / 2, -(args.V + args.v) / 2, -args.F
        )
        Spar = Vector3(
            2 / (args.U - args.u), 2 / (args.V - args.v), 1 / (args.F - args.B)
        )
        transformed_vertex = scale(Spar, transformed_vertex)
    else:
        # normalized perspective projection
        transformed_vertex = transformed_vertex - PRP
        vrp = vrp - PRP

        CW = Vector3((args.U + args.u) / 2, (args.V + args.v) / 2, 0)
        DOP = CW - PRP
        Hpar = [
            [1, 0, -DOP.x / DOP.z, 0],
            [0, 1, -DOP.y / DOP.z, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
        transformed_vertex = multiplyMatVec(Hpar, transformed_vertex)

        # transform vrp as well
        vrp = multiplyMatVec(Hpar, vrp)

        # Sper transform
        a = (2 * vrp.z) / ((args.U - args.u) * (vrp.z + args.B))
        b = (2 * vrp.z) / ((args.V - args.v) * (vrp.z + args.B))
        c = -1 / (vrp.z + args.B)
        Sper = Vector3(a, b, c)
        transformed_vertex = scale(Sper, transformed_vertex)

        # Mcpp transformation
        zmin = args.B
        Mcpp = [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1 / (1 + zmin), (-zmin) / (1 + zmin)],
            [0, 0, -1, 0],
        ]

        transformed_vertex = multiplyMatVec(Mcpp, transformed_vertex, divide=True)

    # add the tranformed point to the list of transformed points
    transformed_vertices.append(transformed_vertex)


output_begin = f"""%!PS-Adobe-3.0
%%BeginSetup
  << /PageSize [{x_size} {y_size}] >> setpagedevice
%%EndSetup

%%%BEGIN
"""

# output bytes with additional lines to draw a border
output_end = """
0 0 moveto
0 500 lineto
500 500 lineto
500 0 lineto

stroke
%%%END\
"""

print(output_begin)
for face in faces:
    # get the vertices of the face
    p, q, r = face
    P, Q, R = (
        transformed_vertices[p - 1],
        transformed_vertices[q - 1],
        transformed_vertices[r - 1],
    )
    # map the normalized vertices to the standard output size
    Px = translate(
        P.x,
        -1,
        1,
        view_port_screen_coordinates_l.x,
        view_port_screen_coordinates_h.x,
    )
    Py = translate(
        P.y,
        -1,
        1,
        view_port_screen_coordinates_l.y,
        view_port_screen_coordinates_h.y,
    )
    Qx = translate(
        Q.x,
        -1,
        1,
        view_port_screen_coordinates_l.x,
        view_port_screen_coordinates_h.x,
    )
    Qy = translate(
        Q.y,
        -1,
        1,
        view_port_screen_coordinates_l.y,
        view_port_screen_coordinates_h.y,
    )
    Rx = translate(
        R.x,
        -1,
        1,
        view_port_screen_coordinates_l.x,
        view_port_screen_coordinates_h.x,
    )
    Ry = translate(
        R.y,
        -1,
        1,
        view_port_screen_coordinates_l.y,
        view_port_screen_coordinates_h.y,
    )

    # clip the polygon against the standard screen coordinates
    outputs = polygon_clipping([(Px, Py), (Qx, Qy), (Rx, Ry)], 0, 0, 500, 500)

    # remap the clipped polygons to the given screen coordinates
    new_out = []
    for point in outputs:
        x = translate(
            point[0],
            view_port_screen_coordinates_l.x,
            view_port_screen_coordinates_h.x,
            args.j,
            args.o,
        )
        y = translate(
            point[1],
            view_port_screen_coordinates_l.y,
            view_port_screen_coordinates_h.y,
            args.k,
            args.p,
        )
        new_out.append((x, y))

    # write to stdout
    outputs = new_out
    if len(outputs):
        x0, y0 = outputs[0]
        print(f"{int(x0)} {int(y0)} moveto")
        for output in outputs[1:]:
            x1, y1 = output
            print(f"{int(x1)} {int(y1)} lineto")
        print(f"{int(x0)} {int(y0)} lineto")


print(output_end)
