from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


class SweptSurface:

    def __init__(self):
        self.fov = 45.0
        self.aspect = 1.0

        self.camera = [0.0, -10.0, 0.0]
        self.center = [0.0, 0.0, 0.0]
        self.up = [0.0, 0.0, 1.0]

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

    # def mouseToWorldVector(self, winX, winY):
    #     vCamera = Vector.fromList(self.camera)
    #     vCenter = Vector.fromList(self.center)
    #
    #     vView = vCamera - vCenter
    #
    #     vZ = vView.normalize()
    #     vX = Vector.fromList(self.up).outer(vZ).normalize()
    #     vY = vX.outer(vZ).normalize()
    #
    #     v = vX.scale(winX) + vY.scale(winY)
    #
    #     return v


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

    glutMainLoop()


if __name__ == '__main__':
    main()