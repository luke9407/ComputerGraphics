from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from util.quaternion import *
from util.vector import *

import math


class Car:

    def __init__(self):
        self.rotate_wheel = 0.0

        self.camera = [6.0, 6.0, 6.0]
        self.center = [0.0, 0.0, 0.0]
        self.up = [0.0, 0.0, 1.0]

        self.length = 0.0
        self.angle = 0.0

        self.dolly = 0.0

        self.fov = 45.0
        self.aspect = 1.0

        # action = 0 -> Noop
        # action = 1 -> Translate
        # action = 2 -> Trackball Rotate
        self.action = 0

        self.last_mouse_window = None

    def init(self):
        glClearColor(0.74902, 0.847059, 0.847059, 1.0)

        glEnable(GL_DEPTH_TEST)

    def drawAxis(self):
        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_LINE_LOOP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(30.0, 0.0, 0.0)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 30.0, 0.0)
        glEnd()

        glBegin(GL_LINE_LOOP)
        glVertex3f(0.0, 0.0, 0.0)
        glVertex3f(0.0, 0.0, 30.0)
        glEnd()

        i = 1
        glPointSize(5.0)
        glBegin(GL_POINTS)
        while i <= 5:
            glColor3f(1.0, 0.0, 0.0)
            glVertex3f(float(i), 0.0, 0.0)
            glColor3f(0.0, 1.0, 0.0)
            glVertex3f(0.0, float(i), 0.0)
            glColor3f(0.0, 0.0, 1.0)
            glVertex3f(0.0, 0.0, float(i))

            i += 1
        glEnd()

    def drawCar(self):
        self.drawTopFront()

        glPushMatrix()
        glTranslatef(0.0, -0.9, 0.0)
        self.drawTopBack()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.0, -0.5, -0.5)
        self.drawBottom()

        glPushMatrix()
        glTranslatef(0.41, 0.65, -0.25)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        self.drawWheel()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.31, 0.65, -0.25)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        self.drawWheel()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0.41, -0.65, -0.25)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        self.drawWheel()
        glPopMatrix()

        glPushMatrix()
        glTranslatef(-0.31, -0.65, -0.25)
        glRotatef(90.0, 0.0, 0.0, 1.0)
        self.drawWheel()
        glPopMatrix()

        glPopMatrix()

    def drawTopFront(self):
        vertices = [
            [0.4, 0.4, 0.25], [-0.4, 0.4, 0.25], [-0.4, -0.3, 0.25], [0.4, -0.3, 0.25],
            [0.4, 0.4, 0.25], [0.4, 0.5, -0.25], [-0.4, 0.5, -0.25], [-0.4, 0.4, 0.25],
            [0.4, 0.4, 0.25], [0.4, -0.3, 0.25], [0.4, -0.3, -0.25], [0.4, 0.5, -0.25],
            [-0.4, -0.3, -0.25], [-0.4, 0.5, -0.25], [-0.4, 0.4, 0.25], [-0.4, -0.3, 0.25],
            [-0.4, -0.3, -0.25], [-0.4, -0.3, 0.25], [0.4, -0.3, 0.25], [0.4, -0.3, -0.25],
            [-0.4, -0.3, -0.25], [0.4, -0.3, -0.25], [0.4, 0.5, -0.25], [-0.4, 0.5, -0.25]
        ]
        self.drawCube(vertices, [1.0, 1.0, 1.0])

        glPushMatrix()

        glTranslatef(0.0, 0.51, -0.25)

        degree = math.degrees(math.atan(0.2))
        glRotatef(degree, 1.0, 0.0, 0.0)

        glColor(0.0, 0.0, 0.0)

        glBegin(GL_QUADS)

        glVertex3f(0.35, 0.0, 0.05)
        glVertex3f(0.35, 0.0, 0.45)
        glVertex3f(-0.35, 0.0, 0.45)
        glVertex3f(-0.35, 0.0, 0.05)

        glEnd()

        glPopMatrix()

    def drawTopBack(self):
        vertices = [
            [0.4, 0.6, 0.2], [0.1, 0.6, 0.2], [0.1, -0.6, 0.2], [0.4, -0.6, 0.2],
            [0.4, 0.6, 0.2], [0.4, 0.6, -0.25], [0.1, 0.6, -0.25], [0.1, 0.6, 0.2],
            [0.4, 0.6, 0.2], [0.4, -0.6, 0.2], [0.4, -0.6, -0.25], [0.4, 0.6, -0.25],
            [0.1, -0.6, -0.25], [0.1, 0.6, -0.25], [0.1, 0.6, 0.2], [0.1, -0.6, 0.2],
            [0.1, -0.6, -0.25], [0.1, -0.6, 0.2], [0.4, -0.6, 0.2], [0.4, -0.6, -0.25],
            [0.1, -0.6, -0.25], [0.4, -0.6, -0.25], [0.4, 0.6, -0.25], [0.1, 0.6, -0.25]
        ]
        self.drawCube(vertices, [1.0, 1.0, 0.0])

        vertices = [
            [-0.4, 0.6, 0.2], [-0.1, 0.6, 0.2], [-0.1, -0.6, 0.2], [-0.4, -0.6, 0.2],
            [-0.4, 0.6, 0.2], [-0.4, 0.6, -0.25], [-0.1, 0.6, -0.25], [-0.1, 0.6, 0.2],
            [-0.4, 0.6, 0.2], [-0.4, -0.6, 0.2], [-0.4, -0.6, -0.25], [-0.4, 0.6, -0.25],
            [-0.1, -0.6, -0.25], [-0.1, 0.6, -0.25], [-0.1, 0.6, 0.2], [-0.1, -0.6, 0.2],
            [-0.1, -0.6, -0.25], [-0.1, -0.6, 0.2], [-0.4, -0.6, 0.2], [-0.4, -0.6, -0.25],
            [-0.1, -0.6, -0.25], [-0.4, -0.6, -0.25], [-0.4, 0.6, -0.25], [-0.1, 0.6, -0.25]
        ]
        self.drawCube(vertices, [1.0, 1.0, 0.0])

        glPushMatrix()

        glTranslatef(0.0, -0.6, 0.15)

        angle = 30.0 + self.angle
        length = 2.0 + self.length

        glRotatef(angle, 1.0, 0.0, 0.0)
        vertices = [
            [0.1, length, 0.1], [-0.1, length, 0.1], [-0.1, 0.0, 0.1], [0.1, 0.0, 0.1],
            [0.1, length, 0.1], [0.1, length, -0.1], [-0.1, length, -0.1], [-0.1, length, 0.1],
            [0.1, length, 0.1], [0.1, 0.0, 0.1], [0.1, 0.0, -0.1], [0.1, length, -0.1],
            [-0.1, 0.0, -0.1], [-0.1, length, -0.1], [-0.1, length, 0.1], [-0.1, 0.0, 0.1],
            [-0.1, 0.0, -0.1], [-0.1, 0.0, 0.1], [0.1, 0.0, 0.1], [0.1, 0.0, -0.1],
            [-0.1, 0.0, -0.1], [0.1, 0.0, -0.1], [0.1, length, -0.1], [-0.1, length, -0.1]
        ]
        self.drawCube(vertices, [0.0, 1.0, 0.0])

        glPushMatrix()

        glTranslatef(0.0, length, 0.08)
        glRotatef(-angle, 1.0, 0.0, 0.0)

        topX = topY = 0.5
        topZ = 0.08
        vertices = [
            [topX, topY, topZ], [-topX, topY, topZ], [-topX, -topY, topZ], [topX, -topY, topZ],
            [topX, topY, topZ], [topX, topY, -topZ], [-topX, topY, -topZ], [-topX, topY, topZ],
            [topX, topY, topZ], [topX, -topY, topZ], [topX, -topY, -topZ], [topX, topY, -topZ],
            [-topX, -topY, -topZ], [-topX, topY, -topZ], [-topX, topY, topZ], [-topX, -topY, topZ],
            [-topX, -topY, -topZ], [-topX, -topY, topZ], [topX, -topY, topZ], [topX, -topY, -topZ],
            [-topX, -topY, -topZ], [topX, -topY, -topZ], [topX, topY, -topZ], [-topX, topY, -topZ]
        ]
        self.drawCube(vertices, [0.0, 0.0, 1.0])

        fenceHeight = 0.1
        thickness = 0.03

        vertices = [
            [thickness, topY - thickness, fenceHeight], [-thickness, topY - thickness, fenceHeight], [-thickness, -topY + thickness, fenceHeight], [thickness, -topY + thickness, fenceHeight],
            [thickness, topY - thickness, fenceHeight], [thickness, topY - thickness, -fenceHeight], [-thickness, topY - thickness, -fenceHeight], [-thickness, topY - thickness, fenceHeight],
            [thickness, topY - thickness, fenceHeight], [thickness, -topY + thickness, fenceHeight], [thickness, -topY + thickness, -fenceHeight], [thickness, topY - thickness, -fenceHeight],
            [-thickness, -topY + thickness, -fenceHeight], [-thickness, topY - thickness, -fenceHeight], [-thickness, topY - thickness, fenceHeight], [-thickness, -topY + thickness, fenceHeight],
            [-thickness, -topY + thickness, -fenceHeight], [-thickness, -topY + thickness, fenceHeight], [thickness, -topY + thickness, fenceHeight], [thickness, -topY + thickness, -fenceHeight],
            [-thickness, -topY + thickness, -fenceHeight], [thickness, -topY + thickness, -fenceHeight], [thickness, topY - thickness, -fenceHeight], [-thickness, topY - thickness, -fenceHeight]
        ]

        glPushMatrix()
        glTranslatef(topX - thickness, 0.0, topZ + fenceHeight)
        self.drawCube(vertices, [1.0, 0.0, 0.0])
        glPopMatrix()

        glPushMatrix()
        glRotatef(90.0, 0.0, 0.0, 1.0)
        glTranslatef(topX - thickness, 0.0, topZ + fenceHeight)
        self.drawCube(vertices, [1.0, 0.0, 0.0])
        glPopMatrix()

        glPushMatrix()
        glRotatef(180.0, 0.0, 0.0, 1.0)
        glTranslatef(topX - thickness, 0.0, topZ + fenceHeight)
        self.drawCube(vertices, [1.0, 0.0, 0.0])
        glPopMatrix()

        glPushMatrix()
        glRotatef(270.0, 0.0, 0.0, 1.0)
        glTranslatef(topX - thickness, 0.0, topZ + fenceHeight)
        self.drawCube(vertices, [1.0, 0.0, 0.0])
        glPopMatrix()

        glPopMatrix()

        glPopMatrix()

    def drawBottom(self):
        vertices = [
            [0.4, 1.0, 0.25], [-0.4, 1.0, 0.25], [-0.4, -1.0, 0.25], [0.4, -1.0, 0.25],
            [0.4, 1.0, 0.25], [0.4, 1.0, -0.25], [-0.4, 1.0, -0.25], [-0.4, 1.0, 0.25],
            [0.4, 1.0, 0.25], [0.4, -1.0, 0.25], [0.4, -1.0, -0.25], [0.4, 1.0, -0.25],
            [-0.4, -1.0, -0.25], [-0.4, 1.0, -0.25], [-0.4, 1.0, 0.25], [-0.4, -1.0, 0.25],
            [-0.4, -1.0, -0.25], [-0.4, -1.0, 0.25], [0.4, -1.0, 0.25], [0.4, -1.0, -0.25],
            [-0.4, -1.0, -0.25], [0.4, -1.0, -0.25], [0.4, 1.0, -0.25], [-0.4, 1.0, -0.25]
        ]
        self.drawCube(vertices, [0.529412, 0.807843, 0.980392])

    def drawCube(self, vertices, cube_color, draw_edge=True, adjust=0.01, edge_color=[0.0, 0.0, 0.0]):
        glColor(cube_color[0], cube_color[1], cube_color[2])
        glBegin(GL_QUADS)
        for vertex in vertices:
            glVertex3f(vertex[0], vertex[1], vertex[2])
        glEnd()

        if draw_edge:
            glColor(edge_color[0], edge_color[1], edge_color[2])
            glBegin(GL_LINES)
            for vertex in vertices:
                glVertex3f(
                    vertex[0] + (adjust if vertex[0] > 0 else -adjust),
                    vertex[1] + (adjust if vertex[1] > 0 else -adjust),
                    vertex[2] + (adjust if vertex[2] > 0 else -adjust)
                )
            glEnd()

    def drawWheel(self):
        glColor(0.0, 0.0, 0.0)

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.1, 0.0)

        i = 0
        while i < 360:
            if i == 180:
                glColor(1.0, 1.0, 1.0)
            rad = (i * math.pi / 180) + self.rotate_wheel
            glVertex3f(0.3 * math.cos(rad), 0.1, 0.3 * math.sin(rad))
            i += 1

        glEnd()

        glColor(0.0, 0.0, 0.0)

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)

        i = 0
        while i < 360:
            if i == 180:
                glColor(1.0, 1.0, 1.0)
            rad = (i * math.pi / 180) + self.rotate_wheel
            glVertex3f(0.3 * math.cos(rad), 0.0, 0.3 * math.sin(rad))
            i += 1

        glEnd()

        glColor(0.0, 0.0, 0.0)

        glBegin(GL_QUAD_STRIP)

        i = 0
        while i < 360:
            rad = (i * math.pi / 180)
            glVertex3f(0.3 * math.cos(rad), 0.0, 0.3 * math.sin(rad))
            glVertex3f(0.3 * math.cos(rad), 0.1, 0.3 * math.sin(rad))
            i += 1

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
        self.drawCar()
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

    def special(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            vCamera = Vector.fromList(self.camera)
            vCenter = Vector.fromList(self.center)

            if (vCamera - vCenter).size() > 1.5:
                v = vCamera + (vCenter - vCamera).normalize().scale(0.3)
                self.camera = v.toList()
        if key == GLUT_KEY_LEFT:
            vCamera = Vector.fromList(self.camera)
            vCenter = Vector.fromList(self.center)

            v = vCamera + (vCamera - vCenter).normalize().scale(0.3)

            self.camera = v.toList()
        if key == GLUT_KEY_UP:
            self.fov += 1

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, 1.0, 200.0)
            glMatrixMode(GL_MODELVIEW)

        if key == GLUT_KEY_DOWN:
            self.fov -= 1
            if self.fov <= 1.0:
                self.fov = 1.0

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, 1.0, 200.0)
            glMatrixMode(GL_MODELVIEW)

        glutPostRedisplay()

    def keyboard(self, key, x, y):
        if key == 'r':
            self.fov = 45.0

            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(self.fov, self.aspect, 1.0, 200.0)
            glMatrixMode(GL_MODELVIEW)

            vCamera = Vector.fromList(self.camera)
            vCenter = Vector.fromList(self.center)

            self.camera = (vCenter + (vCamera - vCenter).normalize().scale(math.sqrt(108))).toList()
        glutPostRedisplay()

    def mouse(self, button, state, x, y):
        if state == GLUT_DOWN:
            if button == GLUT_LEFT_BUTTON:
                self.action = 1
                self.last_mouse_window = [x, y]
            else:
                self.action = 2
                self.last_mouse_window = [x, y]
        else:
            self.action = 0

        glutPostRedisplay()

    def motion(self, x, y):
        winX = x - self.last_mouse_window[0]
        winY = y - self.last_mouse_window[1]

        if winX != 0.0 or winY != 0.0:
            if self.action == 1:
                v = self.mouseToWorldVector(winX, winY)
                v = (-v).scale(0.01)

                vCameraNew = Vector.fromList(self.camera) + v
                vCenterNew = Vector.fromList(self.center) + v

                self.camera = vCameraNew.toList()
                self.center = vCenterNew.toList()
            elif self.action == 2:
                vView = Vector.fromList(self.camera) - Vector.fromList(self.center)
                v = self.mouseToWorldVector(winX, winY).scale(0.3)

                vCameraNew = vView + v

                axis = vView.outer(vCameraNew).normalize()
                angle = vView.angle(vCameraNew)

                p1 = Quaternion.imaginary(vView.toList())
                p2 = Quaternion.imaginary(self.up)
                v = Quaternion.imaginary(axis.toList())
                q = Quaternion.q(v, -angle)

                qCameraNew = q * p1 * -q
                qUpNew = q * p2 * -q

                self.camera = (Quaternion.imaginary(self.center) + qCameraNew).toList()
                self.up = qUpNew.toList()

        self.last_mouse_window = [x, y]
        glutPostRedisplay()

    def mouseToWorldVector(self, winX, winY):
        vCamera = Vector.fromList(self.camera)
        vCenter = Vector.fromList(self.center)

        vView = vCamera - vCenter

        vZ = vView.normalize()
        vX = Vector.fromList(self.up).outer(vZ).normalize()
        vY = vX.outer(vZ).normalize()

        v = vX.scale(winX) + vY.scale(winY)

        return v


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 800)
    glutInitWindowPosition(600, 50)

    glutCreateWindow("Car")

    car = Car()
    car.init()

    glutDisplayFunc(car.display)

    glutReshapeFunc(car.reshape)

    glutSpecialFunc(car.special)

    glutKeyboardFunc(car.keyboard)

    glutMouseFunc(car.mouse)

    glutMotionFunc(car.motion)

    glutMainLoop()


if __name__ == '__main__':
    main()