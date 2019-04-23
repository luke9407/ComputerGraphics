from math import cos, sin, sqrt

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
        denominator = self.w * self.w + self.x * self.x + self.y * self.y + self.z * self.z

        w = self.w / denominator
        x = - self.x / denominator
        y = - self.y / denominator
        z = - self.z / denominator

        return Quaternion(w, x, y, z)

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
