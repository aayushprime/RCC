import random
from treasure_utils import *


def generate_treasure_map_row(width: int, is3D: bool = False) -> str:
    """Generate a row of the treasure map.
    1/6 chance of empty symbol
    5/6 chance of treasure symbol

    If is3D is true, then one symbol is replaced by hole or ladder symbol. (with 50% chance)
    """
    row = ""
    for _ in range(width):
        # if we get 1 from (1-6) the we add empty symbol (1/6 chance)
        if random.randint(1, 6) == 1:
            row += EMPTY_SYMBOL
        # otherwise we add one of the movement symbols randomly (5/6 chance)
        else:
            row += random.choice(MOVEMENT_SYMBOLS)

    # if we are generating a 3D map we will replace one of the symbols with hole or ladder symbol (50% chance)
    if is3D and random.choice([0, 1]) == 1:
        index = random.randint(0, width - 1)
        row = row[:index] + random.choice(MOVEMENT_SYMBOLS_3D) + row[index + 1 :]

    return row


def generate_treasure_map(width: int, height: int, is3D: bool = False) -> str:
    """Generate a treasure map."""

    map = ""
    for _ in range(height):
        map += generate_treasure_map_row(width, is3D)

    # this if is here because the function is called in generate_3D_treasure_map
    # we don't want to replace the first symbol of each map(depth dimension) to right movement symbol
    if not is3D:
        # replace first symbol with right symbol
        map = MOVEMENT_SYMBOLS[0] + map[1:]

    return map


def generate_3D_treasure_map(width: int, height: int, depth: int) -> str:
    """Generate a 3D treasure map."""
    map = ""
    for _ in range(depth):
        map += generate_treasure_map(width, height, True)
    # replace first symbol of map0 with right movement symbol
    map = MOVEMENT_SYMBOLS[0] + map[1:]
    return map


def follow_trail(
    map: str,
    start_row: int,
    start_col: int,
    depth_index: int,
    width: int,
    height: int,
    depth: int,
    number_of_tiles: int,
) -> str:
    """Follow the trail, print number of symbols visited, treasures found and return the new map."""
    x = start_col
    y = start_row
    z = depth_index

    # initialize variables needed for looping correctly
    last_movement_symbol = get_nth_map_from_3D_map(map, 0, width, height, depth)[
        y * width + x
    ]
    steps = 0
    treasures_found = 0

    # if number of tiles == -1, then we want to loop until we find a breadcrumb
    infinite = number_of_tiles == -1
    while number_of_tiles != steps or infinite:

        # get the current symbol
        current_symbol = get_nth_map_from_3D_map(map, z, width, height, depth)[
            y * width + x
        ]
        # we replace current symbol with breadcrumb by default
        replace_current_symbol = True

        # if the current symbol is treasure, return the map
        if current_symbol == TREASURE_SYMBOL:
            treasures_found += 1
            current_symbol = last_movement_symbol
            # we don't want to replace the treasure symbol with breadcrumb symbol
            replace_current_symbol = False
        # if the current symbol is empty, continue to next step
        elif current_symbol == EMPTY_SYMBOL:
            # we don't want to replace the empty symbol with breadcrumb symbol
            replace_current_symbol = False
            # if the current symbol is empty, move in the direction of last movement symbol
            current_symbol = last_movement_symbol
        # if the current symbol is breadcrumb, stop the loop
        elif current_symbol == BREADCRUMB_SYMBOL:
            break

        if replace_current_symbol:
            # change the current symbol to breadcrumb
            map = change_char_in_3D_map(
                map, x, y, z, BREADCRUMB_SYMBOL, width, height, depth
            )

        last_movement_symbol = current_symbol

        # if the current symbol is ladder, go up
        if current_symbol == MOVEMENT_SYMBOLS_3D[1]:
            z -= 1
        # if the current symbol is hole, go down
        elif current_symbol == MOVEMENT_SYMBOLS_3D[0]:
            z += 1
        # if the current symbol is right, go right
        elif current_symbol == MOVEMENT_SYMBOLS[0]:
            x += 1
        # if the current symbol is left, go left
        elif current_symbol == MOVEMENT_SYMBOLS[1]:
            x -= 1
        # if the current symbol is down, go down
        elif current_symbol == MOVEMENT_SYMBOLS[2]:
            y -= 1
        # if the current symbol is up, go up
        elif current_symbol == MOVEMENT_SYMBOLS[3]:
            y += 1

        # if we move out of the map, move back to other side of map
        x %= width
        y %= height
        z %= depth

        # increase steps count
        steps += 1

    print(f"Treasures collected: {treasures_found}")
    print(f"Symbols visited: {steps}")
    return map


if __name__ == "__main__":
    # seed = 9003
    # random.seed(seed)
    # print(generate_treasure_map_row(10, False))
    # random.seed(seed)
    # print(generate_treasure_map_row(10, True))
    # print(generate_treasure_map(10, 10, True))
    # print_3D_treasure_map(generate_3D_treasure_map(3, 3, 3), 3, 3, 3)
    print_3D_treasure_map(follow_trail(">+....", 0, 0, 0, 3, 2, 1, 3), 3, 2, 1)
    print_3D_treasure_map(follow_trail(">>v..v", 0, 0, 0, 3, 2, 1, 1), 3, 2, 1)
    print_3D_treasure_map(follow_trail(">>v..v", 0, 0, 0, 3, 2, 1, 2), 3, 2, 1)
    print_3D_treasure_map(follow_trail(">>v..v", 0, 0, 0, 3, 2, 1, 100), 3, 2, 1)
