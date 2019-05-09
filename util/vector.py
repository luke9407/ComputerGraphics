from math import sqrt, atan2

class Vector:
    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return 'x : {0}, y : {1}, z : {2}, size : {3}'.format(self.x, self.y, self.z, self.size())

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return self.x != other.x or self.y != other.y or self.z or other.z

    def __neg__(self):
        return Vector(-self.x, -self.y, -self.z)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def toList(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def fromList(v):
        return Vector(v[0], v[1], v[2])

    def scale(self, mul):
        return Vector(self.x * mul, self.y * mul, self.z * mul)

    def normalize(self):
        s = self.size()

        x = self.x / s
        y = self.y / s
        z = self.z / s

        return Vector(x, y, z)

    def size(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def inner(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def outer(self, other):
        x = self.y * other.z - self.z * other.y
        y = self.z * other.x - self.x * other.z
        z = self.x * other.y - self.y * other.x

        return Vector(x, y, z)

    def angle(self, other):
        y = (other - self).size()
        x = self.size()
        return atan2(y, x)

    def calculate_normal(self, p0, p1, p2):
        v_p0 = Vector.fromList(p0)
        v_p1 = Vector.fromList(p1)
        v_p2 = Vector.fromList(p2)

        v1 = v_p1 - v_p0
        v2 = v_p2 - v_p0

        normal = v1.outer(v2)
        if normal.inner(v_p0 - self) > 0:
            normal = -normal

        return normal.toList()
