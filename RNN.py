import numpy as np

class RNN(object):
    def __init__(self, inSize, hidSize, outSize):
        self.W_hx = np.random.normal(0,1,[hidSize,inSize])
        self.W_hh = np.random.normal(0,1,[hidSize,hidSize])
        self.W_ah = np.random.normal(0,1,[outSize,hidSize])
        self.h    = np.array([0]*hidSize)
        self.b_h  = np.random.normal(0,1,hidSize)
        self.b_a  = np.random.normal(0,1,outSize)
    def step(self, x):
        self.h = np.tanh(np.dot(self.W_hx,x)+np.dot(self.W_hh,self.h)+self.b_h)
        return np.tanh(np.dot(self.W_ah,self.h)+self.b_a)
