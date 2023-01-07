import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (3, -1, -1),
    (3, 1, -1),
    (1, 1, -1),
    (1, -1, -1),
    (3, -1, 1),
    (3, 1, 1),
    (1, -1, 1),
    (1, 1, 1)
)

edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7)
)


def cube():
    glBegin(GL_POLYGON)
    for edge in edges:
        for vertex in edge:
            glColor3f(0, 1, 1)
            glVertex3fv(vertices[vertex])
    glEnd()


def torus(r, c, r_seg, c_seg):
    glBegin(GL_LINES)
    glColor3f(1, 1, 1)
    for i in range(0, r_seg):
        for j in range(0, c_seg + 1):
            for k in range(0, 2):
                s = (i + k) % r_seg + 0.5
                t = j % (c_seg + 1)
                x = (c + r * math.cos(s * math.tau / r_seg)) * math.cos(t * math.tau / c_seg)
                y = (c + r * math.cos(s * math.tau / r_seg)) * math.sin(t * math.tau / c_seg)
                z = r * math.sin(s * math.tau / r_seg)

                u = (i + k) / r_seg
                v = t / c_seg

                glTexCoord2d(u, v)
                glNormal3f(2 * x, 2 * y, 2 * z)
                glVertex3d(2 * x, 2 * y, 2 * z)

    glEnd()



def main():
    pygame.init()
    display = (1200, 800)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(-1.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        torus(0.1, 0.2, 40, 40)
        pygame.display.flip()
        pygame.time.wait(10)


main()
