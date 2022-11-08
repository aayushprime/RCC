# define constants to represent bit positions
INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000


def clipping(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    # Cohen-Sutherland algorithm
    def calculatePositionCode(x, y):
        code = INSIDE
        if x < xmin:  # point is to the left of rectangle
            code |= LEFT
        elif x > xmax:  # point is to the right of rectangle
            code |= RIGHT
        if y < ymin:  # point is below the rectangle
            code |= BOTTOM
        elif y > ymax:  # point is above the rectangle
            code |= TOP
        return code

    # compute outcodes for P0, P1, and whatever point lies outside the clip rectangle
    code1 = calculatePositionCode(x1, y1)
    code2 = calculatePositionCode(x2, y2)
    accept = False
    while True:
        if code1 == 0 and code2 == 0:
            # If both endpoints lie within rectangle
            accept = True
            break
        elif code1 & code2 != 0:
            # If both endpoints are outside rectangle, in same region
            break
        else:
            # Line needs to be clipped
            # At least one of the points is outside the rectangle, pick it
            x = 1.0
            y = 1.0
            code_out = code1 if code1 != 0 else code2
            # Find intersection point
            # using formulas y = y1 + slope * (x - x1), x = x1 + (1 / slope) * (y - y1)
            if code_out & TOP:
                # point is above the clip rectangle
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & BOTTOM:
                # point is below the clip rectangle
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & RIGHT:
                # point is to the right of clip rectangle
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & LEFT:
                # point is to the left of clip rectangle
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            # Now intersection point x,y is found
            # We replace point outside rectangle by intersection point
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = calculatePositionCode(x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = calculatePositionCode(x2, y2)
    if accept:
        return (int(x1), int(y1), int(x2), int(y2))
    else:
        return None


if __name__ == "__main__":
    x, y = 4, 4
    print(clipping(x, y, 8, 8, 0, 0, 6, 6))
    print(clipping(x, y, 8, 8, 5, 5, 6, 6))
