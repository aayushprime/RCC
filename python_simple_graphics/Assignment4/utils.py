def get_verts_and_faces(lines):
    """
    Simple parser function for the .smf file format.
    """
    v = []
    f = []

    for line in lines:
        line = line.strip()
        if line:
            if line[0] == "v":
                lineAsFloat = list(map(float, line.split()[1:]))
                v.append(lineAsFloat)
            else:
                lineAsInt = list(map(int, line.split()[1:]))
                f.append(lineAsInt)
    return v, f
