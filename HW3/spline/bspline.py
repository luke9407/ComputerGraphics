import numpy as np
from math import pow

class BSpline:
    def __init__(self, interval):
        self.interval = interval
        self.m = np.array([
            [-1.0, 3.0, -3.0, 1.0],
            [3.0, -6.0, 3.0, 0.0],
            [-3.0, 0.0, 3.0, 0.0],
            [1.0, 4.0, 1.0, 0.0]
        ]) * 1/6

    def spline(self, points, closed):
        ret = []

        cnt = len(points)
        for i in range(0, cnt):
            ps = np.array([
                points[(i - 1) % cnt],
                points[(i + 0) % cnt],
                points[(i + 1) % cnt],
                points[(i + 2) % cnt]
            ])

            for j in range(0, self.interval + 1):
                t = float(j) / float(self.interval)
                ts = np.array([pow(t, 3), pow(t, 2), pow(t, 1), 1.0])
                ret.append(np.matmul(np.matmul(ts, self.m), ps))

        return ret
