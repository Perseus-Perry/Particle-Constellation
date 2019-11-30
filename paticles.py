import pygame
import pygame.gfxdraw
import numpy as np
import random
import math

windowSize = 500

class Dot:

    def __init__(self,position,velocity=[0,0],radius=1):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.connected = []

    def velocity(self,velocity):
        self.velocity = velocity

    def updatePos(self):
        self.position = [self.position[0]+self.velocity[0],self.position[1]+self.velocity[1]]


    def bounceFromEdge(self):
        if self.position[0] >= windowSize or self.position[0] <= 0:
            self.velocity = [-self.velocity[0],self.velocity[1]]
        if self.position[1] >= windowSize or self.position[1] <= 0:
            self.velocity = [self.velocity[0],-self.velocity[1]]

    def connectTo(self,dot):
        self.connected.append(dot)

    def disconnectAll(self):
        self.connected= []

    def isConnectedTo(self,dot):
        if dot in self.connected:
            return True
        else:
            return False

    def drawOnScreen(self,surface):
        pygame.gfxdraw.filled_circle(surface,int(self.position[0]),int(self.position[1]),self.radius,(255,255,255))

def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)

def calcDist(dot1, dot2):
    dist = np.sqrt(np.power((dot1[0]-dot2[0]),2)+np.power((dot1[1]-dot2[1]),2))
    return dist

def drawLines(surface,dot,dots,maxDist):
    for point in dots:
        dist = calcDist(dot.position, point.position)
        if(dist<maxDist):
            if not dot.isConnectedTo(point):
                color_val = translate(dist, 0, maxDist, 255, 33)
                color = (color_val,color_val,color_val)
                dot.connectTo(point)
                pygame.draw.aaline(surface,color,dot.position,point.position)



WHITE = ( 255, 255, 255)
GREY = (33,33,33)
maxDist = 120

runGame = True

pygame.init()
clock = pygame.time.Clock()

# Open a new window
size = (windowSize,windowSize)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Particle Constellation")

#create Dots
dotCount = 35

dots = []
for dot in range(dotCount):
    position = [random.randint(0,windowSize),random.randint(0,windowSize)]
    velocity = [random.uniform(-1,1),random.uniform(-1,1)]
    dots.append(Dot(position,velocity))

#main loop

while runGame:

    #handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runGame = False

    screen.fill(GREY)
    #game events
    for dot in dots:
        dot.drawOnScreen(screen)
        dot.bounceFromEdge()
        dot.updatePos()
        drawLines(screen, dot, dots, maxDist)

    #clear Connections
    for dot in dots:
        dot.disconnectAll()
    #update
    pygame.display.flip()
    clock.tick(60)


pygame.quit()
