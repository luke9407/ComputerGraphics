from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from time import sleep
import math


class Car:

    def __init__(self):
        self.rotate_x = 0.0
        self.rotate_y = 0.0
        self.rotate_z = 0.0

        self.rotate_car = 0.0
        self.rotate_wheel = 0.0

        self.last_car_center = [3.0, 2.0]
        self.last_car_pos = 0.0

        self.length = 0.0
        self.angle = 0.0

        self.pos = 0.0

        self.scale = 0.0

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

    def drawCar(self):
        glTranslatef(self.last_car_center[0], self.last_car_center[1], 1.25)
        glRotatef(self.rotate_car, 0.0, 0.0, 1.0)
        glTranslatef(0.0, self.pos - self.last_car_pos, 0.0)

        theta = math.radians(-self.rotate_car)

        car_center_x = self.last_car_center[0] + math.sin(theta) * (self.pos - self.last_car_pos)
        car_center_y = self.last_car_center[1] + math.cos(theta) * (self.pos - self.last_car_pos)

        self.last_car_center = [car_center_x, car_center_y]
        self.last_car_pos = self.pos

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

        gluLookAt(10.0 + self.scale, 10.0 + self.scale, 6.0 + self.scale, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

        # glRotatef(self.rotate_x, 1.0, 0.0, 0.0)
        # glRotatef(self.rotate_y, 0.0, 1.0, 0.0)
        # glRotatef(self.rotate_z, 0.0, 0.0, 1.0)

        glPushMatrix()
        self.drawAxis()
        glPopMatrix()

        glRotatef(self.rotate_x, 1.0, 0.0, 0.0)
        glRotatef(self.rotate_y, 0.0, 1.0, 0.0)
        glRotatef(self.rotate_z, 0.0, 0.0, 1.0)

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
            gluPerspective(45.0, h / w, 1.0, 200.0)
        else:
            gluPerspective(45.0, w / h, 1.0, 200.0)

        glMatrixMode(GL_MODELVIEW)

    def keyboard(self, key, x, y):
        if key == 'd':
            self.pos += 0.1
            self.rotate_wheel += 5
        if key == 'a':
            self.pos -= 0.1
            self.rotate_wheel -= 5
        if key == 'w':
            self.rotate_car += 5
            # self.rotate_wheel += 5
        if key == 's':
            self.rotate_car -= 5
            # self.rotate_wheel -= 5
        if key == 'i':
            self.angle += 5
            if self.angle >= 90.0:
                self.angle = 90.0
        if key == 'k':
            self.angle -= 5
            if self.angle <= 0:
                self.angle = 0
        if key == 'l':
            self.length += 0.5
            if self.length >= 4.0:
                self.length = 4.0
        if key == 'j':
            self.length -= 0.5
            if self.length <= 0:
                self.length = 0
        glutPostRedisplay()

    def special(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            self.rotate_z += 5
            self.rotate_wheel += 5
        if key == GLUT_KEY_LEFT:
            self.rotate_z -= 5
            self.rotate_wheel -= 5
        if key == GLUT_KEY_UP:
            self.scale += 1
        if key == GLUT_KEY_DOWN:
            self.scale -= 1
            if self.scale <= 0:
                self.scale = 0
        glutPostRedisplay()

    def idle(self):
        self.rotate_z += 5
        sleep(0.1)
        glutPostRedisplay()


def main():
    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)

    glutInitWindowSize(800, 800)
    glutInitWindowPosition(100, 100)

    glutCreateWindow("Car")

    car = Car()
    car.init()

    glutDisplayFunc(car.display)

    glutReshapeFunc(car.reshape)

    glutKeyboardFunc(car.keyboard)

    glutSpecialFunc(car.special)

    # glutIdleFunc(car.idle)

    glutMainLoop()


if __name__ == '__main__':
    main()