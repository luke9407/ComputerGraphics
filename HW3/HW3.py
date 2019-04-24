from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.quaternion import *
from util.vector import *


class SweptSurface:

    def __init__(self):
        self.fov = 45.0
        self.aspect = 1.0

        self.camera = [0.0, -10.0, 0.0]
        self.center = [0.0, 0.0, 0.0]
        self.up = [0.0, 0.0, 1.0]

        self.action = 0
        self.last_mouse_window = None

    def init(self):
        glClearColor(0.74902, 0.847059, 0.847059, 1.0)

        glEnable(GL_DEPTH_TEST)

    def draw_axis(self):
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_LINE_LOOP)
        glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(30.0, 0.0, 0.0)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 1.0, 0.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 30.0, 0.0)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glColor3f(0.0, 0.0, 1.0)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 30.0)
        glEnd()

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        gluLookAt(
            self.camera[0], self.camera[1], self.camera[2],
            self.center[0], self.center[1], self.center[2],
            self.up[0], self.up[1], self.up[2]
        )

        glPushMatrix()
        self.draw_axis()
        glPopMatrix()

        glutSwapBuffers()

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

        gluPerspective(self.fov, self.aspect, 1.0, 200.0)

        glMatrixMode(GL_MODELVIEW)

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

            q_camera_new = q * p1 * -q
            q_up_new = q * p2 * -q

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

    glutInit(args)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 800)
    glutInitWindowPosition(600, 50)

    glutCreateWindow("Assignment 3")

    swept_surface = SweptSurface()
    swept_surface.init()

    glutDisplayFunc(swept_surface.display)

    glutReshapeFunc(swept_surface.reshape)

    glutMouseFunc(swept_surface.mouse)

    glutMotionFunc(swept_surface.motion)

    glutMainLoop()


if __name__ == '__main__':
    main()