import random as rnd
import pygame as pg
from pygame.locals import *
from Genotype import *

def move(pos, direction):
    return (pos[0]+direction[0],pos[1]+direction[1])
def scale(pos, factor):
    return (pos[0]*factor, pos[1]*factor)
def rotate(direction, radians):
    c = np.cos(radians)
    s = np.sin(radians)
    return (c*direction[0] + s*direction[1],
            -s*direction[0]+ c*direction[1])

def flatten(lst):
    if len(lst)==0:
        return lst
    elif isinstance(lst[0],list):
        return flatten(lst[0])+flatten(lst[1:])
    else:
        return [lst[0]]+flatten(lst[1:])

class Organism(object):
    def __init__(self,**args):
        self.center = (int(rnd.uniform(0,800)), int(rnd.uniform(0,600)))
        self.orientation = 0
        self.speed = 20
        self.angSpeed = 0
        self.hunger = 100
        self.age = 0.

        self.radius     = 6
        self.noseLength = 6
        self.tailLength = 18
        self.color      = (255,255,0)

        self.genome = args.get('genome', Genotype(3,2,0))
        self.brain = self.genome.makeNet()
    def getColor(self):
        return map(lambda x: x*(1./50*self.hunger-1./10000*self.hunger*self.hunger),
            self.color)
    def getForward(self):
        return (np.cos(self.orientation), np.sin(self.orientation))
    def getLeftNostril(self):
        noseDir = rotate(self.getForward(), -np.pi/4)
        return move(self.center,scale(noseDir,self.radius+self.noseLength))
    def getRightNostril(self):
        noseDir = rotate(self.getForward(), np.pi/4)
        return move(self.center,scale(noseDir,self.radius+self.noseLength))
    def getGenome(self):
        return self.genome
    def draw(self, screen):
        Black = (0,0,0)
        #Draw main body
        pg.draw.circle(screen, self.getColor(), map(int,self.center), self.radius)
        #Draw tail
        tailStart = move(self.center,scale(self.getForward(),-self.radius))
        tailEnd = move(tailStart,scale(self.getForward(),-self.tailLength))
        pg.draw.line(screen, Black, tailStart, tailEnd)
        #Draw right nostril
        noseDir = rotate(self.getForward(),np.pi/4)
        noseStart = move(self.center,scale(noseDir,self.radius))
        noseEnd = move(noseStart,scale(noseDir,self.noseLength))
        pg.draw.line(screen, Black, noseStart, noseEnd)
        #Draw left nostril
        noseDir = rotate(self.getForward(),-np.pi/4)
        noseStart = move(self.center,scale(noseDir,self.radius))
        noseEnd = move(noseStart,scale(noseDir,self.noseLength))
        pg.draw.line(screen, Black, noseStart, noseEnd)
    def update(self, smells, dt):
        output = self.brain.fire(smells+[self.hunger/100-1])
        self.orientation += output[0]*dt
        self.center = move(self.center, scale(self.getForward(), (output[1]+1)*15*dt))
        #self.center = (self.center[0]%800,self.center[1]%600)
        self.age += dt
        self.hunger = max(self.hunger-dt,0)
    # Returns a string represeing a graphviz graph of the organism's brain
    def toGraph(self):
        res = 'digraph {\n'
        res += '\tNode0[label="left smell (input)"];\n'
        res += '\tNode1[label="right smell (input)"];\n'
        res += '\tNode2[label="hunger (input)"];\n'
        res += '\tNode3[label="angular speed (output)"];\n'
        res += '\tNode4[label="speed (output)"];\n'

        b = self.brain
        for x in xrange(b.hidSize):
            res += '\tNode'+str(x+b.inSize+b.outSize)+'[label="hidden '+str(x)+'"];\n'
        res += '\n'
        for s in b.synapses:
            res += '\tNode'+str(s.fro)+'->Node'+str(s.to)+'[label="'+str(s.w)+'"];\n'
        res += '}'
        return res
                               
