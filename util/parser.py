from util.quaternion import *

class Parser:
    def __init__(self, f):
        self.f = f

    def parse(self):
        parsed = {
            'curve_type': None, 'cross_sections': [],
            'scalings': [], 'rotations': [], 'positions': [],
        }

        with open(self.f, 'r') as f:
            parsed['curve_type'] = self.read_line(f).upper()
            cross_section_count = int(self.read_line(f))
            control_point_count = int(self.read_line(f))

            cross_section_iter = 0
            while cross_section_iter < cross_section_count:
                cross_section = {
                    'points': [],
                    'scaling': None, 'rotation': None, 'position': None
                }

                control_point_iter = 0
                while control_point_iter < control_point_count:
                    point = self.read_line(f).split()
                    point = [float(point[0]), 0.0, float(point[1])]
                    cross_section['points'].append(point)

                    control_point_iter += 1

                scaling = float(self.read_line(f))
                cross_section['scaling'] = scaling
                parsed['scalings'].append(scaling)

                rotation = self.read_line(f).split()
                angle = float(rotation[0])
                axis = Quaternion.imaginary([float(rotation[1]), float(rotation[2]), float(rotation[3])])
                q = Quaternion.q(axis, angle)
                cross_section['rotation'] = q
                parsed['rotations'].append(q)

                position = map(float, self.read_line(f).split())
                cross_section['position'] = position
                parsed['positions'].append(position)

                parsed['cross_sections'].append(cross_section)
                cross_section_iter += 1

        return parsed

    def read_line(self, f):
        while True:
            line = f.readline().partition('#')[0].strip()
            if line:
                return line