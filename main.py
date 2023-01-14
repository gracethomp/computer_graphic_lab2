import math

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

vertices = (
    (3, -1, -3),
    (3, 1, -3),
    (1, 1, -3),
    (1, -1, -3),
    (3, -1, -1),
    (3, 1, -1),
    (1, -1, -1),
    (1, 1, -1)
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
    glColor3f(0, 1, 1)
    for edge in edges:
        for vertex in edge:
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
                x = (c + r * math.cos(s * math.tau / r_seg)) * math.cos(t * math.tau / c_seg) + 1
                y = (c + r * math.cos(s * math.tau / r_seg)) * math.sin(t * math.tau / c_seg)
                z = r * math.sin(s * math.tau / r_seg) + 1

                u = (i + k) / r_seg
                v = t / c_seg

                glTexCoord2d(u, v)
                glNormal3f(20 * x + 2, 20 * y, 20 * z)
                glVertex3d(2 * x, 2 * y, 2 * z)

    glEnd()


def draw_func():
    glBegin(GL_POINTS)
    glColor3f(0.8, 0.0, 0.8)
    k = 0
    while k < 5:
        x = 1 + k
        y = 0
        k += 0.1
        while x < 10:
            x += 0.005
            y += 0.005
            j = math.sin(y) * math.sqrt(x)
            glVertex3f(x, y, j)
    glEnd()


def main():
    pygame.init()
    display = pygame.display.set_mode((0, 0), DOUBLEBUF | OPENGL, vsync=1)
    gluPerspective(45, 1920 / 1080, 0.1, 50)

    glTranslatef(0, 0.0, -15)
    display_center = [display.get_size()[i] // 2 for i in range(2)]
    mouse_move = [0, 0]
    pygame.mouse.set_pos(display_center)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEMOTION:
                mouse_move = [event.pos[i] - display_center[i] for i in range(2)]
        pygame.mouse.set_pos(display_center)
        keypress = pygame.key.get_pressed()
        glRotatef(mouse_move[0] * 0.05, 0, 1, 0.0)
        glRotatef(mouse_move[1] * 0.05, 1.0, 0.0, 0.0)
        if keypress[pygame.K_w]:
            glTranslatef(0, 0, 0.1)
        if keypress[pygame.K_s]:
            glTranslatef(0, 0, -0.1)
        if keypress[pygame.K_d]:
            glTranslatef(-0.1, 0, 0)
        if keypress[pygame.K_a]:
            glTranslatef(0.1, 0, 0)
        if keypress[pygame.K_DOWN]:
            glTranslatef(0, 1, 0)
        if keypress[pygame.K_UP]:
            glTranslatef(0, -1, 0)
        if keypress[pygame.K_o]:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glOrtho(-1.0, 1.0, -1.0, 1.0, 5, 100)
        if keypress[pygame.K_p]:
            glFrustum(2, -1, -2, 2, -100, 1000)

        if keypress[pygame.K_ESCAPE]:
            pygame.quit()
            quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        cube()
        torus(0.1, 0.2, 40, 40)
        draw_func()
        pygame.display.flip()
        pygame.time.wait(10)


main()
