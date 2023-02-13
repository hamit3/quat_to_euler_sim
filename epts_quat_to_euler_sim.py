#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
from pygame.locals import *
# generate random integer values
from random import seed
from random import randint
import csv
import time
import math
import numpy as np
import PSpincalc as sp


counter = 0
ax = ay = az = 0.0

yaw = []
pitch = []
roll = []

def resize(width, height):
    if height==0:
        height=1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0*width/height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init():
    glShadeModel(GL_SMOOTH)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClearDepth(1.0)
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    

def drawText(position, textString):     
    font = pygame.font.SysFont ("Courier", 18, True)
    textSurface = font.render(textString, True, (255,255,255,255), (0,0,0,255))     
    textData = pygame.image.tostring(textSurface, "RGBA", True)     
    glRasterPos3d(*position)     
    glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

def draw():
    global rquad
    global counter
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	
    
    glLoadIdentity()
    glTranslatef(0,0.0,-7.0)

    osd_text = "pitch: " + str("{0:.2f}".format(ax)) + ", roll: " + str("{0:.2f}".format(az)) + ", yaw: " + str("{0:.2f}".format(ay))
    drawText((-2,-2, 2), osd_text)

    glRotatef(az, 0.0, 1.0, 0.0)      # Yaw,   rotate around y-axis
    glRotatef(ay ,1.0,0.0,0.0)        # Pitch, rotate around x-axis
    glRotatef(-1*ax ,0.0,0.0,1.0)     # Roll,  rotate around z-axis

    glBegin(GL_QUADS)	
    glColor3f(0.0,1.0,0.0)
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f(-1.0, 0.2, 1.0)		
    glVertex3f( 1.0, 0.2, 1.0)		

    glColor3f(1.0,0.5,0.0)	
    glVertex3f( 1.0,-0.2, 1.0)
    glVertex3f(-1.0,-0.2, 1.0)		
    glVertex3f(-1.0,-0.2,-1.0)		
    glVertex3f( 1.0,-0.2,-1.0)		

    glColor3f(1.0,0.0,0.0)		
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2, 1.0)		
    glVertex3f(-1.0,-0.2, 1.0)		
    glVertex3f( 1.0,-0.2, 1.0)		

    glColor3f(1.0,1.0,0.0)	
    glVertex3f( 1.0,-0.2,-1.0)
    glVertex3f(-1.0,-0.2,-1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f( 1.0, 0.2,-1.0)		

    glColor3f(0.0,0.0,1.0)	
    glVertex3f(-1.0, 0.2, 1.0)
    glVertex3f(-1.0, 0.2,-1.0)		
    glVertex3f(-1.0,-0.2,-1.0)		
    glVertex3f(-1.0,-0.2, 1.0)		

    glColor3f(1.0,0.0,1.0)	
    glVertex3f( 1.0, 0.2,-1.0)
    glVertex3f( 1.0, 0.2, 1.0)
    glVertex3f( 1.0,-0.2, 1.0)		
    glVertex3f( 1.0,-0.2,-1.0)		
    glEnd()

def rad2deg(rad):
    return rad / np.pi * 180

def deg2rad(deg):
    return deg / 180 * np.pi

def getEulerAngles(q):
    global ax, ay, az
    quaternion = np.array(q)
    ea = sp.Q2EA(quaternion, EulerOrder="zyx", ignoreAllChk=True)[0]

    yaw = rad2deg(ea[0])
    pitch = rad2deg(ea[1])
    roll = rad2deg(ea[2])
    ax = roll
    ay = pitch
    az = yaw

       
def read_data():
    global ax, ay, az
    f = open("../log_asc.txt", 'r', encoding="utf-8", errors='ignore');
    file_content = f.read().splitlines()
    f.close()
    last_line = file_content[-2]
    angles = last_line.split(',')
    if (len(angles) == 6 and angles[0] == '&' and angles[5] == '&'):
        try:
            quat_w = float(angles[1])
            quat_x = float(angles[2])
            quat_y = float(angles[3])
            quat_z = float(angles[4])
        except ValueError:
            pass
    q = [quat_w,quat_x, quat_y, quat_z];
    getEulerAngles(q)

def main():
    global yaw_mode

    video_flags = OPENGL|DOUBLEBUF
    
    pygame.init()
    screen = pygame.display.set_mode((640,480), video_flags)
    pygame.display.set_caption("Press Esc to quit, z toggles yaw mode")
    resize(640,480)
    init()
    frames = 0
    ticks = pygame.time.get_ticks()
    while 1:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()  #* quit pygame properly
            break
        read_data()
        draw()
        pygame.display.flip()
        frames = frames+1
        time.sleep(0.1)
    print ("fps:  %d" % ((frames*1000)/(pygame.time.get_ticks()-ticks)))

if __name__ == '__main__': main()





