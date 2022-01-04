# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame
import random
import time

pygame.init()
WHITE = (255, 255, 255)
RED = (255,0,0)
BLACK = (0,0,0)
# Classes
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.molecule = None
class Molecule:
    def __init__(self):
        self.list = []

# Creates a set of particles in random locations
# returns a list of the particles
def particleGenerator(n, width, height):
    retValue = []

    while len(retValue) < n:
        x = random.randint(0,width-1)
        y = random.randint(0,height-1)
        repeat = False
        for p in retValue:
            if p.x == x and p.y == y:
                repeat = True
                break
        while repeat:
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            repeat = False
            for p in retValue:
                if p.x == x and p.y == y:
                    repeat = True
                    break
        p = Particle(x,y)
        retValue.append(p)
    return retValue

def move(p,width,height,board):
    moveList = [1,2,3,4]
    # 1 = vX = 1, 2 = vY = 1, 3 = vX = -1, 4 = vY = -1
    if(p.x ==0):
        moveList.remove(3)
    if(p.y==0):
        moveList.remove(4)
    if(p.x == width-1):
        moveList.remove(1)
    if(p.y == height -1):
        moveList.remove(2)
    board[p.x][p.y] = 0
    temp = random.choice(moveList)
    if(temp == 1):
        p.x = p.x + 1
    elif(temp==2):
        p.y = p.y + 1
    elif(temp ==3):
        p.x = p.x -1
    else:
        p.y = p.y -1
    board[p.x][p.y] = p

def moveMolecule(m, width, height, board):
    moveList = [1,2,3,4]
    # 1 = vX = 1, 2 = vY = 1, 3 = vX = -1, 4 = vY = -1, 5 = NO MOVE AVAILAIBLE NOT POSSIBLE
    preX = 0
    preY = 0
    for p in m.list:
        if (p.x <= 0 and 3 in moveList):
            moveList.remove(3)
        if (p.y <= 0 and 4 in moveList):
            moveList.remove(4)
        if (p.x >= width - 1 and (1 in moveList)):
            moveList.remove(1)
        if (p.y >= height - 1 and (2 in moveList)):
            moveList.remove(2)
        if ((p.x >= 799 or p.y >= 799 or p.x <= 0 or p.y <= 0) and len(moveList) == 4):
            print()
        if p.x > preX:
            preX = p.x
        if p.y > preY:
            preY = p.y

    bbb = len(moveList)

    temp = random.choice(moveList)
    vX = 0
    vY = 0

    if (temp == 1):
        vX = 1
    elif (temp == 2):
        vY = 1
    elif (temp == 3):
        vX = -1
    else:
        vY = -1
    for p in m.list:
        board[p.x][p.y] = 0
        p.x = p.x + vX
        p.y = p.y + vY
        board[p.x][p.y] = p

def checkMoleculeCollision(m, board, width, height):
    for p in m.list:
        temp = getNeighbour(p,board, width, height)
        for k in temp:
            if (k not in m.list):
                if k.molecule == None:
                    m.list.append(k)
                    k.molecule = m
                else:
                    mergeMolecule(m, k.molecule)

def mergeMolecule(m, mer):
    for k in mer.list:
        k.molecule = m
        if k not in m.list:
            m.list.append(k)
    del mer


def getNeighbour(p, board, width, height):
    retValue = []
    if isinstance(p.x != width-1 and board[p.x+1][p.y], Particle):
        retValue.append(board[p.x+1][p.y])
    if isinstance(p.x != 0 and board[p.x-1][p.y], Particle):
        retValue.append(board[p.x-1][p.y])
    if isinstance(p.y != height-1 and board[p.x][p.y+1], Particle):
        retValue.append(board[p.x][p.y+1])
    if isinstance(p.y != 0 and board[p.x][p.y-1], Particle):
        retValue.append(board[p.x][p.y-1])
    return retValue

def unpaint(p):
    pygame.draw.rect(screen, BLACK, pygame.Rect(p.x, p.y, rectSize, rectSize))

def paint(p):
    pygame.draw.rect(screen, WHITE, pygame.Rect(p.x, p.y, rectSize, rectSize))

def unPaintMolecule(m):
    for p in m.list:
        unpaint(p)
def paintMolecule(m):
    for p in m.list:
        paint(p)

clock = pygame.time.Clock()
(width, height) = (600,600)
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Fractal Simulation")

board = []
for i in range(0,width):
    temp = []
    for j in range(0,height):
        temp.append(0)
    board.append(temp)

pSet = particleGenerator(1000, width, height)



for i in range(0,len(pSet)):
    board[pSet[i].x][pSet[i].y] = pSet[i]

mSet = []
rectSize = 1
screen.fill((0, 0, 0))


for p in pSet:
    paint(p)
while True:
    # prints free particles
    for p in pSet:
    #neighbours = getNeighbour(p,board, width, height)
        if(p.molecule == None):
            neighbours = getNeighbour(p,board, width, height)
            if(len(neighbours) == 0):
                unpaint(p)
                move(p, width, height, board)
                paint(p)
            else:
                m = Molecule()
                mSet.append(m)
                m.list = neighbours
                m.list.append(p)
                p.molecule = m
                for k in neighbours:
                    k.molecule = m
                unPaintMolecule(m)
                moveMolecule(m, width, height, board)
                paintMolecule(m)
        else:
            # check for collision

            checkMoleculeCollision(m,board, width, height)
            unPaintMolecule(m)
            moveMolecule(m,width,height,board)
            paintMolecule(m)

    pygame.display.flip()