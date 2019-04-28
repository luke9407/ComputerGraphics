from math import cos, sin, sqrt, acos, pi
from vector import *

EPS = 0.0001

class Quaternion:
    def __init__(self, w, x, y, z):
        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        return 'w : {0}, x : {1}, y : {2}, z : {3}, size : {4}'.format(
            self.w,
            self.x,
            self.y,
            self.z,
            sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        )

    def __neg__(self):
        return Quaternion(-self.w, -self.x, -self.y, -self.z)

    def __sub__(self, other):
        w = self.w - other.w
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z

        return Quaternion(w, x, y, z)

    def __add__(self, other):
        w = self.w + other.w
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z

        return Quaternion(w, x, y, z)

    def __mul__(self, other):
        w = -self.x * other.x - self.y * other.y - self.z * other.z + self.w * other.w
        x = self.x * other.w + self.y * other.z - self.z * other.y + self.w * other.x
        y = -self.x * other.z + self.y * other.w + self.z * other.x + self.w * other.y
        z = self.x * other.y - self.y * other.x + self.z * other.w + self.w * other.z

        return Quaternion(w, x, y, z)

    def size(self):
        return sqrt(
            self.w * self.w +
            self.x * self.x +
            self.y * self.y +
            self.z * self.z
        )

    def inverse(self):
        return Quaternion(self.w, -self.x, -self.y, -self.z)

    def scale(self, mul):
        return Quaternion(
            self.w * mul,
            self.x * mul,
            self.y * mul,
            self.z * mul
        )

    def divide(self, denominator):
        return Quaternion(
            self.w / denominator,
            self.x / denominator,
            self.y / denominator,
            self.z / denominator
        )

    def percent(self, other):
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def normalize(self):
        size = self.size()
        return self.divide(size)

    @staticmethod
    def exp(v):
        theta = v.size()
        if theta < EPS:
            sc = 1
        else:
            sc = sin(theta) / theta

        v = v.scale(sc).toList()
        return Quaternion(cos(theta), v[0], v[1], v[2])

    def ln(self):
        sc = sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
        theta = atan2(sc, self.w)

        if sc > EPS:
            sc = theta / sc
        else:
            sc = 1.0

        return Vector(sc * self.x, sc * self.y, sc * self.z)

    def slerp(self, other, t):
        c = self.percent(other)

        if 1.0 + c > EPS:
            if 1.0 - c > EPS:
                theta = acos(c)
                sinom = sin(theta)

                return (self.scale((1 - t) * theta) + other.scale(t * theta)).divide(sinom)
            else:
                return (self.scale(1 - t) + other.scale(t)).normalize()
        else:
            return self.scale(sin((0.5 - t) * pi)) + other.scale(sin(t * pi))

    def toList(self):
        return [self.x, self.y, self.z]

    @staticmethod
    def imaginary(v):
        return Quaternion(0.0, v[0], v[1], v[2])

    @staticmethod
    def q(v, angle):
        cosine = cos(angle / 2)
        sine = sin(angle / 2)

        w = cosine
        x = v.x * sine
        y = v.y * sine
        z = v.z * sine

        return Quaternion(w, x, y, z)
