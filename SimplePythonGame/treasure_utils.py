MOVEMENT_SYMBOLS = "><v^"
EMPTY_SYMBOL = "."
TREASURE_SYMBOL = "+"
BREADCRUMB_SYMBOL = "X"
MOVEMENT_SYMBOLS_3D = "*|"


def get_nth_row_from_map(map: str, n: int, width: int, height: int):
    """Get the nth row from the map."""
    assert len(map) == width * height
    if n >= height or n < 0:
        return ""
    return map[n * width : (n + 1) * width]


def print_treasure_map(map: str, width: int, height: int):
    """Print the treasure map."""
    assert len(map) == width * height
    for n in range(height):
        print(map[n * width : (n + 1) * width])


def change_char_in_map(
    map: str, x: int, y: int, char: str, width: int, height: int
) -> str:
    """Change a character in the map (str) and return the new map."""
    assert len(map) == width * height
    assert x >= 0 and x < width
    assert y >= 0 and y < height
    assert len(char) == 1
    return map[: y * width + x] + char + map[y * width + x + 1 :]


def get_proportion_travelled(map: str) -> float:
    """Get the proportion of the map that has been travelled."""
    return round(map.count(BREADCRUMB_SYMBOL) / len(map), 2)


def get_nth_map_from_3D_map(map: str, n: int, width: int, height: int, depth: int):
    """Get the nth map from the 3D map."""
    assert len(map) == width * height * depth
    if n >= depth or n < 0:
        return ""
    return map[n * width * height : (n + 1) * width * height]


def print_3D_treasure_map(map: str, width: int, height: int, depth: int):
    """Print the 3D treasure map."""
    assert len(map) == width * height * depth
    for n in range(depth):
        print_treasure_map(
            map[n * width * height : (n + 1) * width * height], width, height
        )
        print()


def change_char_in_3D_map(
    map: str, x: int, y: int, z: int, char: str, width: int, height: int, depth: int
) -> str:
    """Change a character in the 3D map (str) and return the new map."""
    assert len(map) == width * height * depth
    assert x >= 0 and x < width
    assert y >= 0 and y < height
    assert z >= 0 and z < depth
    assert len(char) == 1
    return (
        map[: (z * width * height) + (y * width) + x]
        + char
        + map[(z * width * height) + (y * width) + x + 1 :]
    )


if __name__ == "__main__":
    # Test get_nth_row_from_map
    print(get_nth_row_from_map("^..>>>,,v", 1, 3, 3))
    print(get_nth_row_from_map("......", 0, 2, 3))
    # Test print_treasure_map
    print_treasure_map("<..vvv..^", 3, 3)
    print_treasure_map("<..vvv..", 2, 4)
    # Test change_char_in_map
    print(change_char_in_map(".........", 1, 1, "X", 3, 3))
    # Test get_proportion_travelled
    print(get_proportion_travelled(".X..X.XX."))
    # Test get_nth_map_from_3D_map
    print(get_nth_map_from_3D_map(".X.XXX.X..v.vXv.v.", 0, 3, 3, 2))
    print(get_nth_map_from_3D_map(".X.XXX.X..v.vXv.v.", 1, 3, 3, 2))
    # Test print_3D_treasure_map
    print_3D_treasure_map(".X.XXX.X..v.vXv.v.", 3, 3, 2)
    # Test change_char_in_3D_map
    print_3D_treasure_map(
        change_char_in_3D_map(".X.XXX.X..v.vXv.v.", 0, 0, 0, "#", 3, 3, 2), 3, 3, 2
    )
