import math


class Vector3:
    """
    A class to represent a point in 3D space.
    """

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self):
        return iter([self.x, self.y, self.z])

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __div__(self, other):
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return "(%g, %g, %g)" % (self.x, self.y, self.z)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)

    def unit_vector(self):
        mag = abs(self)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)


class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def __div__(self, other):
        return Vector2(self.x / other.x, self.y / other.y)

    def __abs__(self):
        return math.sqrt(self.x**2 + self.y**2)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return "(%g, %g)" % (self.x, self.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def unit_vector(self):
        return self / abs(self)


def translate(value, leftMin, leftMax, rightMin, rightMax):
    """
    Map a value within range leftMin to leftMax to a corresponding value between rightMin and rightMax using linear interpolation.
    """
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)


def cross(a, b):
    """
    Compute the cross product of 2 vectors and return the result as a new vector.
    """
    c = [a.y * b.z - a.z * b.y, a.z * b.x - a.x * b.z, a.x * b.y - a.y * b.x]
    return Vector3(c[0], c[1], c[2])


def multiplyMat(X, Y):
    """
    Multiply X and Y matrices and return the result as a new matrix.
    """

    result = [
        [sum(a * b for a, b in zip(X_row, Y_col)) for Y_col in zip(*Y)] for X_row in X
    ]

    res = []
    for r in result:
        res.append(r)
    return res


def multiplyMatVec(X, V, divide=False):
    """
    Multiply a matrix and a vector and return the result as a new vector.
    If divide is true, then the result vector is normalized. (division by the last element of the result vector)
    """
    res = multiplyMat(X, [[V.x], [V.y], [V.z], [1]])
    res = [*[item for sublist in res for item in sublist]]
    if divide:
        res = [r / res[3] for r in res]
    return Vector3(*res[:-1])


def scale(v, s):
    """
    Simple transformation functions to scale a vector by another.
    """
    return Vector3(v.x * s.x, v.y * s.y, v.z * s.z)
