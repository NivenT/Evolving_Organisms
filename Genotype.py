from NeuralNet import *
import random as rng

class ConnectGene(object):
    numInnovations = 0
    def __init__(self, fromIndex, toIndex, weight, isEnabled):
        self.fro = fromIndex
        self.to = toIndex
        self.w = weight
        self.on = isEnabled
        self.innov = ConnectGene.numInnovations # Innovation number

        ConnectGene.numInnovations += 1

    def __repr__(self):
        return str(self.innov) + ': ' + str(Synapse(self.fro,self.to,self.w)) if self.on else 'DISABLED'

class Genotype(object):
    def __init__(self, numInput, numOutput, numHidden):
        self.inSize = numInput
        self.outSize = numOutput
        self.hidSize = numHidden
        self.conn = []
        self.fit = 0

    def size(self):
        return self.inSize + self.hidSize + self.outSize

    def addConnection(self, fro, to, w, on):
        self.conn += [ConnectGene(fro, to, w, on)]
        return self.conn[-1]

    def makeNet(self):
        net = NeuralNet(self.inSize, self.outSize, self.hidSize)
        [net.addSynapse(s.fro, s.to, s.w) for s in self.conn if s.on]
        return net

    def mutateAddConnection(self):
        fromIndex = rng.randint(0,self.size()-1)
        toIndex = rng.randint(self.inSize, self.size()-1)
        weight = rng.gauss(0, 1)
        return self.addConnection(fromIndex, toIndex, weight, True)

    def mutateAddNode(self):
        onConnections = [i for i in range(0,len(self.conn)) if self.conn[i].on]
        if len(onConnections) == 0:
            return []
        
        connIndex = rng.choice(onConnections)
        self.conn[connIndex].on = False
        c = self.conn[connIndex]

        self.addConnection(c.fro, self.size(), 1, True)
        self.addConnection(self.size(), c.to, c.w, True)
        self.hidSize += 1
        return self.conn[-2:]

    def cross(self, mate, enableRate):
        dad = sorted(self.conn, key=lambda x: x.innov)
        mom = sorted(mate.conn, key=lambda x: x.innov)
        chld = []

        i, j = 0, 0 #The current gene for mom (i) and dad (j)
        while i < len(mom) and j < len(dad):
            if mom[i].innov == dad[j].innov:
                chld += [rng.choice([mom[i], dad[j]])]
                if not chld[-1].on and rng.random() < enableRate:
                    chld[-1].on = True
                i, j = i+1, j+1
            elif mom[i].innov < dad[j].innov and mate.fit >= self.fit:
                chld += [mom[i]]
                i += 1
            else:
                chld += [dad[j]]
                j += 1
        if   i < len(mom) and mate.fit >= self.fit:
            chld += mom[i:]
        elif j < len(dad) and self.fit >= mate.fit:
            chld += dad[j:]

        res = Genotype(self.inSize, self.outSize, max(self.hidSize, mate.hidSize))
        res.conn = chld
        return res

    def __repr__(self):
        return  'inSize -> '  + str(self.inSize)  + ', ' + 'outSize -> ' + str(self.outSize) + ', ' +'hidSize -> ' + str(self.hidSize) + '\n' +str(self.conn)
