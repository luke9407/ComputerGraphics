import numpy as np
from math import pow

from util.quaternion import *
from util.vector import *

class CatmullRom:
    def __init__(self, interval):
        self.interval = interval
        self.m = np.array([
            [0.0, 2.0, 0.0, 0.0],
            [-1.0, 0.0, 1.0, 0.0],
            [2.0, -5.0, 4.0, -1.0],
            [-1.0, 3.0, -3.0, 1.0]
        ]) * 1/2

    def spline(self, points, closed):
        ret = []

        cnt = len(points)
        limit = cnt if closed else cnt - 1

        for i in range(0, limit):
            p0 = points[0] if i == 0 and not closed else points[(i - 1) % cnt]
            p1 = points[(i + 0) % cnt]
            p2 = points[(i + 1) % cnt]
            p3 = points[i + 1] if i == cnt - 2 and not closed else points[(i + 2) % cnt]

            ps = np.array([p0, p1, p2, p3])

            for j in range(0, self.interval + 1):
                t = float(j) / float(self.interval)
                ts = np.array([1.0, pow(t, 1), pow(t, 2), pow(t, 3)])
                ret.append(np.matmul(np.matmul(ts, self.m), ps))

        return ret

    def quaternion_spline(self, quaternions):
        ret = []

        cnt = len(quaternions)
        for i in range(0, cnt - 1):
            q0 = quaternions[0] if i == 0 else quaternions[i - 1]
            q1 = quaternions[i]
            q2 = quaternions[i + 1]
            q3 = quaternions[i + 1] if i == cnt - 2 else quaternions[i + 2]

            a = q1 * Quaternion.exp(
                (q0.inverse() * q2).ln().scale(1.0 / 6.0)
            )
            b = q2 * Quaternion.exp(
                -(q1.inverse() * q3).ln().scale(1.0 / 6.0)
            )

            for j in range(0, self.interval + 1):
                t = float(j) / float(self.interval)
                s1 = q1.slerp(a, t)
                s2 = a.slerp(b, t)
                s3 = b.slerp(q2, t)

                s4 = s1.slerp(s2, t)
                s5 = s2.slerp(s3, t)

                ret.append(s4.slerp(s5, t))

        return ret
