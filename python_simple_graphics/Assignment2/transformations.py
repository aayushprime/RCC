from math import sin, cos, radians


def scale(x, y, s):
    return x * s, y * s


def rotate(x, y, angle, xm=0, ym=0):
    angle = radians(angle)
    xr = (x - xm) * cos(angle) - (y - ym) * sin(angle) + xm
    yr = (x - xm) * sin(angle) + (y - ym) * cos(angle) + ym
    return round(xr), round(yr)


def translate(x, y, tx=0, ty=0):
    return x + tx, y + ty


if __name__ == "__main__":
    x, y = 4, 4
    print(scale(x, y, 2))
    print(rotate(x, y, 45))
    print(translate(x, y, 2))
