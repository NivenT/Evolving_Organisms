import random as rnd
import pygame as pg
from pygame.locals import *
from RNN import *

def move(pos, direction):
    return (pos[0]+direction[0],pos[1]+direction[1])
def scale(pos, factor):
    return (pos[0]*factor, pos[1]*factor)
def rotate(direction, radians):
    return (np.cos(radians)*direction[0]+np.sin(radians)*direction[1],
            -np.sin(radians)*direction[0]+np.cos(radians)*direction[1])

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
        self.radius = 8
        self.brain = args.get('brain',RNN(3,5,1))
        self.hunger = 100
        self.age = 0
    def getColor(self):
        return map(lambda x: x*(1./50*self.hunger-1./10000*self.hunger*self.hunger),
            (255,255,0))
    def getForward(self):
        return (np.cos(self.orientation), np.sin(self.orientation))
    def getLeftNostril(self):
        noseDir = rotate(self.getForward(), -np.pi/4)
        return move(self.center,scale(noseDir,self.radius+8))
    def getRightNostril(self):
        noseDir = rotate(self.getForward(), np.pi/4)
        return move(self.center,scale(noseDir,self.radius+8))
    def getGenome(self):
        return flatten([self.brain.W_hx.tolist(), self.brain.W_hh.tolist(), self.brain.W_ah.tolist(),
                        self.brain.b_h.tolist(), self.brain.b_a.tolist()])
    def draw(self, screen):
        Black = (0,0,0)
        pg.draw.circle(screen, self.getColor(), map(int,self.center), self.radius)
        tailStart = move(self.center,scale(self.getForward(),-self.radius))
        tailEnd = move(tailStart,scale(self.getForward(),-24))
        pg.draw.line(screen, Black, tailStart, tailEnd)
        noseDir = rotate(self.getForward(),np.pi/4)
        noseStart = move(self.center,scale(noseDir,self.radius))
        noseEnd = move(noseStart,scale(noseDir,8))
        pg.draw.line(screen, Black, noseStart, noseEnd)
        noseDir = rotate(self.getForward(),-np.pi/4)
        noseStart = move(self.center,scale(noseDir,self.radius))
        noseEnd = move(noseStart,scale(noseDir,8))
        pg.draw.line(screen, Black, noseStart, noseEnd)
    def update(self, smell, dt):
        output = self.brain.step([smell[0],smell[1],self.hunger/100-1])
        self.orientation += output[0]*dt
        self.center = move(self.center, scale(self.getForward(), 20*dt))
        self.age += dt
        self.hunger = max(self.hunger-dt,0)
        
