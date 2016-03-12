import numpy as np

class Synapse(object):
        def __init__(self, fromIndex, toIndex, weight):
                self.fro = fromIndex
                self.to = toIndex
                self.w = weight
        def  __repr__(self):
                return str(self.fro) + ' --(' + str(self.w) + ')--> ' + str(self.to)

class NeuralNet(object):
        def __init__(self, numInput, numOutput, numHidden = 0):
                self.inSize = numInput
                self.outSize = numOutput
                self.hidSize = numHidden
                self.synapses = []
                # self.biasVector = np.array([0]*(numOutput+numHidden), dtype='float64')
                self.activations = np.array([0]*(numOutput+numInput+numHidden), dtype='float64')

        def size(self):
                return self.inSize + self.hidSize + self.outSize

        def fire(self, x):
                assert(len(x) == self.inSize)
                
                newState = [0]*self.size()
                self.activations[:self.inSize] = x
                
                for s in self.synapses:
                        # newState[s.to] += self.activations[s.fro]*s.w + self.biasVector[s.to-self.inSize]
                        newState[s.to] += self.activations[s.fro]*s.w
                        
                self.activations[self.inSize:] = np.tanh(newState[self.inSize:])
                return self.activations[self.inSize:self.inSize+self.outSize]

        def addNeuron(self):
                # self.biasVector = np.append(self.biasVector, [bias])
                self.activations = np.append(self.activations, [0])
                self.hidSize += 1

        def addSynapse(self, fro, to, w):
                self.synapses += [Synapse(fro, to, w)]
