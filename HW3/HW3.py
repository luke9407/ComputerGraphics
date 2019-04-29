import sys
sys.path.append('../')

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from parser import *

from util.quaternion import *
from util.vector import *

from spline.bspline import *
from spline.catmullrom import *

class SweptSurface:

    def __init__(self, data):
        self.fov = 45.0
        self.aspect = 1.0

        self.camera = [0.0, 0.0, 100.0]
        self.center = [0.0, 0.0, 0.0]
        self.up = [0.0, 1.0, 0.0]

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

        glEnable(GL_DEPTH_TEST)

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

        self.draw_cross_section()
        self.draw_cross_point()

        glutSwapBuffers()

    def draw_cross_section(self):
        glColor3f(0.0, 0.0, 0.0)
        for cross_section_spline in self.cross_section_splines:
            glBegin(GL_LINE_STRIP)
            for point in cross_section_spline:
                glVertex3f(point[0], point[1], point[2])
            glEnd()

    def draw_cross_point(self):
        spline_cnt = len(self.cross_point_splines)
        for i in range(0, spline_cnt):
            s1 = self.cross_point_splines[i]
            s2 = self.cross_point_splines[(i + 1) % spline_cnt]

            point_cnt = len(s1) - 1
            for j in range(0, point_cnt):
                glColor3f(
                    float(i) / float(spline_cnt),
                    float(j) / float(point_cnt),
                    float(i + j) / float(spline_cnt + point_cnt)
                )

                glBegin(GL_QUADS)
                glVertex3f(s1[j][0], s1[j][1], s1[j][2])
                glVertex3f(s1[j + 1][0], s1[j + 1][1], s1[j + 1][2])
                glVertex3f(s2[j + 1][0], s2[j + 1][1], s2[j + 1][2])
                glVertex3f(s2[j][0], s2[j][1], s2[j][2])
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


def main():
    args = sys.argv
    if len(args) != 2:
        sys.exit('No data file or too many arguments!')

    f = args.pop()
    parser = Parser(f)

    glutInit(args)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 800)
    glutInitWindowPosition(600, 50)

    glutCreateWindow("Assignment 3")

    swept_surface = SweptSurface(parser.parse())
    swept_surface.init()

    glutDisplayFunc(swept_surface.display)

    glutReshapeFunc(swept_surface.reshape)

    glutSpecialFunc(swept_surface.special)

    glutMouseFunc(swept_surface.mouse)

    glutMotionFunc(swept_surface.motion)

    glutMainLoop()


if __name__ == '__main__':
    main()
