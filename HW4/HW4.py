import sys
import os
sys.path.append(os.path.join(sys.path[0], '..'))

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.parser import *

from util.quaternion import *
from util.vector import *

from util.spline.bspline import *
from util.spline.catmullrom import *


class Shading:

    def __init__(self, data):
        self.fov = 45.0
        self.aspect = 1.0

        self.camera = [0.0, 0.0, 120.0]
        self.center = [0.0, 0.0, 0.0]
        self.up = [0.0, 1.0, 0.0]

        self.box_alpha = 0.3

        self.action = 0
        self.last_mouse_window = None

        self.data = data

        if self.data['curve_type'] == 'BSPLINE':
            self.spline = BSpline(3)
        else:
            self.spline = CatmullRom(3)

        self.geometric_spline = CatmullRom(3)

        self.cross_section_splines = []
        self.cross_point_splines = []

    def init(self):
        glClearColor(0.74902, 0.847059, 0.847059, 1.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glEnable(GL_COLOR_MATERIAL)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_NORMALIZE)
        glEnable(GL_LIGHTING)

        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0])

        glEnable(GL_LIGHT1)
        glLight(GL_LIGHT1, GL_AMBIENT, (0.0, 0.0, 0.0, 1.0))
        glLight(GL_LIGHT1, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
        glLight(GL_LIGHT1, GL_SPECULAR, (1.0, 1.0, 1.0, 1.0))
        glLight(GL_LIGHT1, GL_POSITION, (1.0, 1.0, 1.0, 1.0))
        glLight(GL_LIGHT1, GL_SPOT_CUTOFF, 45.0)
        glLight(GL_LIGHT1, GL_SPOT_DIRECTION, (0.0, 0.0, 0.0, 1.0))
        glLight(GL_LIGHT1, GL_SPOT_EXPONENT, 2.0)

        self.init_splines()

    def init_splines(self):
        scaling_spline = self.geometric_spline.spline(self.data['scalings'], False)
        rotation_spline = self.geometric_spline.quaternion_spline(self.data['rotations'])
        position_spline = self.geometric_spline.spline(self.data['positions'], False)

        points = {}
        for cross_section in self.data['cross_sections']:
            s = self.spline.spline(cross_section['points'], True)
            scaling = cross_section['scaling']
            rotation = cross_section['rotation']
            position = cross_section['position']

            q = rotation
            q_inv = q.inverse()

            cross_section_spline = []
            for j, point in enumerate(s):
                scaled = Quaternion.imaginary([point[0] * scaling, point[1], point[2] * scaling])
                rotated = (q * scaled * q_inv).toList()
                translated = Vector.toList(Vector.fromList(position) + Vector.fromList(rotated))

                cross_section_spline.append(translated)

                if j not in points:
                    points[j] = []

                points[j].append(point)
            self.cross_section_splines.append(cross_section_spline)

        for i in points:
            s = self.geometric_spline.spline(points[i], False)
            cross_point_spline = []
            for j, point in enumerate(s):
                scaling = scaling_spline[j]
                rotation = rotation_spline[j]
                position = position_spline[j]

                q = rotation
                q_inv = rotation.inverse()

                scaled = Quaternion.imaginary([point[0] * scaling, point[1], point[2] * scaling])
                rotated = (q * scaled * q_inv).toList()
                translated = Vector.toList(Vector.fromList(position) + Vector.fromList(rotated))

                cross_point_spline.append(translated)
            self.cross_point_splines.append(cross_point_spline)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        gluLookAt(
            self.camera[0], self.camera[1], self.camera[2],
            self.center[0], self.center[1], self.center[2],
            self.up[0], self.up[1], self.up[2]
        )

        glPushMatrix()
        glTranslatef(25.0, -4.0, 0.0)
        self.draw_box(5.0, 'bronze')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-25.0, -4.0, 0.0)
        self.draw_box(5.0, 'chrome')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(25.0, -4.0, 25.0)
        self.draw_box(5.0, 'copper')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-25.0, -4.0, 25.0)
        self.draw_box(5.0, 'gold')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, -4.0, 25.0)
        self.draw_box(5.0, 'silver')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-25.0, -4.0, -25.0)
        self.draw_box(5.0, 'green_plastic')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, -4.0, -25.0)
        self.draw_box(5.0, 'red_rubber')
        glPopMatrix()

        glPushMatrix()
        glTranslatef(25.0, -4.0, -25.0)
        self.draw_box(5.0, 'emerald')
        glPopMatrix()

        self.draw_cross_point()

        glPushMatrix()
        glTranslatef(0.0, -4.0, 0.0)
        self.draw_box(15.0)
        glPopMatrix()

        glutSwapBuffers()

    def draw_cross_point(self):
        materials = ['bronze', 'chrome', 'copper', 'gold', 'silver', 'green_plastic', 'red_rubber', 'emerald']
        spline_cnt = len(self.cross_point_splines)
        v_camera = Vector.fromList(self.camera) - Vector.fromList(self.center)
        for i in range(0, spline_cnt):
            s1 = self.cross_point_splines[i]
            s2 = self.cross_point_splines[(i + 1) % spline_cnt]

            self.set_material(materials[i % len(materials)])

            point_cnt = len(s1) - 1
            for j in range(0, point_cnt):
                glBegin(GL_TRIANGLES)

                normal = v_camera.calculate_normal(s1[j], s1[j + 1], s2[j + 1])
                glNormal3f(normal[0], normal[1], normal[2])
                glVertex3f(s1[j][0], s1[j][1], s1[j][2])
                glVertex3f(s1[j + 1][0], s1[j + 1][1], s1[j + 1][2])
                glVertex3f(s2[j + 1][0], s2[j + 1][1], s2[j + 1][2])

                normal = v_camera.calculate_normal(s2[j + 1], s1[j], s2[j])
                glNormal3f(normal[0], normal[1], normal[2])
                glVertex3f(s2[j + 1][0], s2[j + 1][1], s2[j + 1][2])
                glVertex3f(s2[j][0], s2[j][1], s2[j][2])
                glVertex3f(s1[j][0], s1[j][1], s1[j][2])
                glEnd()

    def draw_box(self, length, mat=''):
        cube = [
            [[0.0, 0.0, 0.0], [length, 0.0, 0.0], [length, length, 0.0]],
            [[length, length, 0.0], [0.0, length, 0.0], [0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [0.0, length, 0.0], [0.0, length, length]],
            [[0.0, length, length], [0.0, 0.0, length], [0.0, 0.0, 0.0]],
            [[0.0, 0.0, 0.0], [length, 0.0, 0.0], [length, 0.0, length]],
            [[length, 0.0, length], [0.0, 0.0, length], [0.0, 0.0, 0.0]],
            [[0.0, length, 0.0], [length, length, 0.0], [length, length, length]],
            [[length, length, length], [0.0, length, length], [0.0, length, 0.0]],
            [[length, 0.0, 0.0], [length, length, 0.0], [length, length, length]],
            [[length, length, length], [length, 0.0, length], [length, 0.0, 0.0]],
            [[0.0, 0.0, length], [length, 0.0, length], [length, length, length]],
            [[length, length, length], [0.0, length, length], [0.0, 0.0, length]]
        ]
        normals = [
            [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], [-1.0, 0.0, 0.0], [-1.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, -1.0, 0.0],
            [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]
        ]

        if mat is not '':
            self.set_material(mat)

        v_camera = Vector.fromList(self.camera) - Vector.fromList(self.center)
        order = {'back': {}, 'front': {}}
        for idx, cube_info in enumerate(cube):
            normal = normals[idx]
            inner = v_camera.inner(Vector.fromList(normal))
            if inner > 0:
                order['front'][idx] = normal
            else:
                order['back'][idx] = normal

        glBegin(GL_TRIANGLES)
        for pos in ['back', 'front']:
            idxs = order[pos]
            for idx in idxs:
                surface = cube[idx]
                normal = idxs[idx]
                if mat is '':
                    color = [0.0, 0.0, 0.0]
                    for idx, point in enumerate(surface):
                        if sum(point) >= 2.0 * length:
                            color[idx - 1] = 1.0
                    glColor4f(color[0], color[1], color[2], 0.5)
                glNormal3f(normal[0], normal[1], normal[2])
                for point in surface:
                    glVertex3f(point[0], point[1], point[2])
        glEnd()

    def reshape(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if h == 0:
            h = 1
        if w == 0:
            w = 1

        if w <= h:
            self.aspect = h / w
        else:
            self.aspect = w / h

        gluPerspective(self.fov, self.aspect, 1.0, 1000.0)

        glMatrixMode(GL_MODELVIEW)

    def special(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            v_camera = Vector.fromList(self.camera)
            v_center = Vector.fromList(self.center)

            if (v_camera - v_center).size() > 1.5:
                v = v_camera + (v_center - v_camera).normalize().scale(0.3)
                self.camera = v.toList()
        if key == GLUT_KEY_LEFT:
            v_camera = Vector.fromList(self.camera)
            v_center = Vector.fromList(self.center)

            v = v_camera + (v_camera - v_center).normalize().scale(0.3)

            self.camera = v.toList()
        if key == GLUT_KEY_UP:
            self.fov += 1

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, 1.0, 1000.0)
            glMatrixMode(GL_MODELVIEW)

        if key == GLUT_KEY_DOWN:
            self.fov -= 1
            if self.fov <= 1.0:
                self.fov = 1.0

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, 1.0, 1000.0)
            glMatrixMode(GL_MODELVIEW)

        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            self.action = 1
            self.last_mouse_window = [x, y]
        else:
            self.action = 0
        glutPostRedisplay()

    def motion(self, x, y):
        win_x = x - self.last_mouse_window[0]
        win_y = y - self.last_mouse_window[1]

        if win_x != 0.0 or win_y != 0.0:
            v_view = Vector.fromList(self.camera) - Vector.fromList(self.center)
            v = self.mouse_to_world_vector(win_x, win_y).scale(0.3)

            v_camera_new = v_view + v

            axis = v_view.outer(v_camera_new).normalize()
            angle = v_view.angle(v_camera_new)

            p1 = Quaternion.imaginary(v_view.toList())
            p2 = Quaternion.imaginary(self.up)
            v = Quaternion.imaginary(axis.toList())
            q = Quaternion.q(v, -angle)
            q_inv = q.inverse()

            q_camera_new = q * p1 * q_inv
            q_up_new = q * p2 * q_inv

            self.camera = (Quaternion.imaginary(self.center) + q_camera_new).toList()
            self.up = q_up_new.toList()

        self.last_mouse_window = [x, y]
        glutPostRedisplay()

    def mouse_to_world_vector(self, win_x, win_y):
        v_camera = Vector.fromList(self.camera)
        v_center = Vector.fromList(self.center)

        v_view = v_camera - v_center

        v_z = v_view.normalize()
        v_x = Vector.fromList(self.up).outer(v_z).normalize()
        v_y = v_x.outer(v_z).normalize()

        v = v_x.scale(win_x) + v_y.scale(win_y)

        return v

    @staticmethod
    def set_material(name):
        if name == 'bronze':
            ambient = [0.2125, 0.1275, 0.054, 1.0]
            diffuse = [0.714, 0.4284, 0.18144]
            specular = [0.393548, 0.271906, 0.166721]
            shininess = 0.2
        elif name == 'chrome':
            ambient = [0.25, 0.25, 0.25, 1.0]
            diffuse = [0.4, 0.4, 0.4]
            specular = [0.774597, 0.774597, 0.774597]
            shininess = 0.6
        elif name == 'copper':
            ambient = [0.19125, 0.0735, 0.0225, 1.0]
            diffuse = [0.7038, 0.27048, 0.0828]
            specular = [0.256777, 0.137622, 0.086014]
            shininess = 0.1
        elif name == 'gold':
            ambient = [0.24725, 0.1995, 0.0745, 1.0]
            diffuse = [0.75164, 0.60648, 0.22648]
            specular = [0.628281, 0.555802, 0.366065]
            shininess = 0.4
        elif name == 'silver':
            ambient = [0.19225, 0.19225, 0.19225, 1.0]
            diffuse = [0.50754, 0.50754, 0.50754]
            specular = [0.508273, 0.508273, 0.508273]
            shininess = 0.4
        elif name == 'green_plastic':
            ambient = [0.0, 0.0, 0.0, 1.0]
            diffuse = [0.1, 0.35, 0.1]
            specular = [0.45, 0.55, 0.45]
            shininess = 0.4
        elif name == 'red_rubber':
            ambient = [0.05, 0.0, 0.0, 1.0]
            diffuse = [0.5, 0.4, 0.4]
            specular = [0.7, 0.04, 0.04]
            shininess = 0.078125
        else:
            ambient = [0.0215, 0.1745, 0.0215, 1.0]
            diffuse = [0.07568, 0.61424, 0.07568]
            specular = [0.633, 0.727811, 0.633]
            shininess = 0.6

        glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterial(GL_FRONT_AND_BACK, GL_SHININESS, shininess * 128.0)
        glColor3f(diffuse[0], diffuse[1], diffuse[2])


def main():
    args = sys.argv

    f = os.path.join(os.path.dirname(__file__), '../sample/my.txt')
    parser = Parser(f)

    glutInit(args)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 800)
    glutInitWindowPosition(600, 50)

    glutCreateWindow("Assignment 4")

    shading = Shading(parser.parse())
    shading.init()

    glutDisplayFunc(shading.display)

    glutReshapeFunc(shading.reshape)

    glutSpecialFunc(shading.special)

    glutMouseFunc(shading.mouse)

    glutMotionFunc(shading.motion)

    glutMainLoop()


if __name__ == '__main__':
    main()
