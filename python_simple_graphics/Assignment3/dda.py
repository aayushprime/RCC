def DDA(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == dy == 0:
        return []

    # calculate steps required for generating pixels
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    # calculate increment in x & y for each steps
    x_increment = float(dx / steps)
    y_increment = float(dy / steps)

    coords = []

    for i in range(0, int(steps + 1)):
        # Draw pixels
        coords.append((int(x1), int(y1)))
        x1 += x_increment
        y1 += y_increment
    return coords


if __name__ == "__main__":
    print([k for k in DDA(75, 450, 25, 350)])
