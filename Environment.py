from organism import *
from time import clock, sleep
from math import ceil

def distSquared(pos1, pos2):
    return (pos1[0]-pos2[0])*(pos1[0]-pos2[0])+(pos1[1]-pos2[1])*(pos1[1]-pos2[1])

def partition(lst, size):
    return [lst[i:i+size] for i in xrange(0,len(lst),size)]

def angBetween(vec1, vec2):
    return np.arccos(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))

class Food(object):
    def __init__(self):
        self.center = (int(rnd.uniform(0,800)), int(rnd.uniform(0,600)))
        self.radius = 3
        self.type = int(round(rnd.uniform(0,2)))
        self.color = {0: (255,0,0), 1: (0,255,0), 2: (0,0,255)}[self.type]
        self.lifespan = rnd.randint(50,200)
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.center, self.radius)
    def update(self, dt):
        self.lifespan -= dt

class Species(object):
    def __init__(self, representative):
        self.rep = representative
        self.members = [representative]
        self.totFit = 0
        self.numOffsprings = 0

    def size(self):
        return len(self.members)

    def distance(self, genotype1, genotype2, c1, c2, c3):
        if len(genotype1.conn) == 0:
            return c2*len(genotype2.conn)
        elif len(genotype2.conn) == 0:
            return c2*len(genotype1.conn)
        
        a = sorted(genotype1.conn, key=lambda x: x.innov)
        b = sorted(genotype2.conn, key=lambda x: x.innov)

        numExcess = 0
        numDisjoint = 0
        numSame = 0
        totWeightDist = 0

        maxInnov = b[-1].innov
        for i in xrange(len(a)):
            if a[i].innov > maxInnov:
                numExcess += 1
            else:
                for j in xrange(len(b)):
                    if a[i].innov == b[j].innov:
                        totWeightDist += abs(a[i].w-b[j].w)
                        numSame += 1
                        numDisjoint -= 1
                        break
                numDisjoint += 1

        maxInnov = a[-1].innov
        for j in xrange(len(b)):
            if b[j].innov > maxInnov:
                numExcess += 1
            else:
                for i in xrange(len(a)):
                    if b[j].innov == a[i].innov:
                        totWeightDist += abs(b[j].w-a[i].w)
                        numSame += 1
                        numDisjoint -= 1
                        break
                numDisjoint += 1

        n = max(len(a), len(b))
        if numSame == 0:
            res = c1*numExcess/n + c2*numDisjoint/n
        else:
            res = c1*numExcess/n + c2*numDisjoint/n + c3*totWeightDist/numSame
        return res
        
        
class Environment(object):
    def __init__(self):
        self.orgs = [Organism() for x in xrange(30)]
        self.food = [Food() for x in xrange(40)]
        self.foodTimer = 800
        self.start = clock()
        self.selected = -1
        
        self.generation = 1
        self.nodeMutRate   = .4
        self.connMutRate   = .6
        self.weightMutRate = .5
        self.enableRate    = .25

        self.species = []
        self.compatThresh = 3
        self.c1           = 1
        self.c2           = 1
        self.c3           = .4

    def draw(self, screen):
        if self.selected > -1:
            self.orgs[self.selected].color = (0,0,255)
        for org in self.orgs:
            if abs(org.hunger-100) < 100:
                org.draw(screen)
        if self.selected > -1:
            self.orgs[self.selected].color = (255,255,0)
        for food in self.food:
            food.draw(screen)

    def updateFood(self, dt):
        for food in self.food:
            food.update(dt)
            if 0 > food.lifespan:
                self.food.remove(food)
        self.foodTimer -= 1
        if self.foodTimer <= 0:
            # Lower food supplies cause less food to be generated
            self.food += [Food() for x in xrange(rnd.randint(1,min(10, len(self.food))))]
            self.foodTimer = 800

    def updateOrgs(self, dt):
        anyAlive = False
        for org in self.orgs:
            if distSquared((400,300), org.center) > 800*800:
                org.hunger = 0 #Kill organisms that move too far away
            elif abs(org.hunger-100) < 100:
                anyAlive = True
                
                leftSmells = rightSmells = [0]*3
                for food in self.food:
                    combinedRadii = food.radius+org.radius
                    dist = distSquared(food.center,org.center)
                    if dist < combinedRadii*combinedRadii:
                        org.hunger += {0: -10, 1: 5, 2: 15}[food.type]
                        self.food.remove(food)
                    elif dist < 15000:
                        leftSmells[food.type] += np.exp(-distSquared(food.center,org.getLeftNostril())/5000)
                        rightSmells[food.type] += np.exp(-distSquared(food.center,org.getRightNostril())/5000)
                org.update(leftSmells+rightSmells, dt)
                """
                minDist, ang = [50]*3, [0]*3
                for food in self.food:
                    dist2 = distSquared(food.center,org.center)
                    if dist2 < (food.radius+org.radius)*(food.radius+org.radius):
                        org.hunger += {0: -10, 1: 5, 2: 15}[food.type]
                        self.food.remove(food)
                    elif dist2 < minDist[food.type]*minDist[food.type]:
                        minDist[food.type] = np.sqrt(dist2)
                        direction = move(food.center,scale(org.center,-1))
                        ang[food.type] = angBetween(direction,[1,0])
                org.update(minDist+ang, dt)
                """
        return anyAlive

    def update(self, dt):
        self.updateFood(dt)
        if not self.updateOrgs(dt):
            durr = int(round(clock()-self.start))
            sleep(3)
            print 'Generation', self.generation
            print "\tPopulation survived for", durr/60, "minutes and", durr%60, "seconds"
            self.stepPopulation(dt)

    def checkClick(self, pos):
        self.selected = -1
        squaredRadius = self.orgs[0].radius*self.orgs[0].radius
        for x in xrange(len(self.orgs)):
            if distSquared(self.orgs[x].center, pos) < squaredRadius:
                self.selected = x

    def saveSelected(self):
        if self.selected > -1:
            f = open('brain.dot', 'w')
            f.write(self.orgs[self.selected].toGraph())
            f.close()
            print 'Saved brain in "brain.dot"'

    def stepPopulation(self, dt):
        #Update species
        #maxDist = 0
        for org in self.orgs:
            if self.species == []:
                self.species = [Species(org)]
            else:
                foundMatch = False
                for s in self.species:
                    dist = s.distance(org.genome, s.rep.genome, self.c1, self.c2, self.c3)
                    #maxDist = max(dist, maxDist)
                    if dist < self.compatThresh:
                        s.members += [org]
                        foundMatch = True
                        break
                if not foundMatch:
                    self.species += [Species(org)]
                    
        #Determine the fitness of each organism
        totFit = 0
        minAge = min([org.age for org in self.orgs])
        for s in self.species:
            s.totFit = 0.
            for org in s.members:
                org.genome.fit = (org.age-minAge)/float(s.size())
                s.totFit += org.genome.fit
            totFit += s.totFit

        #Breed new population on a species by species basis
        newPop = []
        innovations = []
        for s in self.species:
            s.numOffsprings = int(ceil(len(self.orgs)*s.totFit/totFit))
            for x in xrange(s.numOffsprings):
                rand, index = rng.uniform(0, s.totFit), 0
                while s.members[index].genome.fit < rand:
                    rand -= s.members[index].genome.fit
                    index += 1
                dad = s.members[index]
                
                rand, index = rng.uniform(0, s.totFit), 0
                while s.members[index].genome.fit < rand:
                    rand -= s.members[index].genome.fit
                    index += 1
                mom = s.members[index]

                chld = dad.genome.cross(mom.genome, self.enableRate)
                if rng.random() < self.nodeMutRate:
                    newInnovs = chld.mutateAddNode()
                    if len(newInnovs) > 0:
                        for innov in innovations:
                            if innov.to == newInnovs[0].to and innov.fro == newInnovs[0].fro:
                                chld.conn[-2].innov = innov.innov
                                ConnectGene.numInnovations -= 1
                            elif innov.to == newInnovs[1].to and innov.fro == newInnovs[1].fro:
                                chld.conn[-1].innov = innov.innov
                                ConnectGene.numInnovations -= 1
                        innovations += chld.conn[-2:]
                if rng.random() < self.connMutRate:
                    newInnov = chld.mutateAddConnection()
                    for innov in innovations:
                        if innov.to == newInnov.to and innov.fro == newInnov.fro:
                            chld.conn[-1].innov = innov.innov
                            ConnectGene.numInnovations -= 1
                    innovations += [chld.conn[-1]]
                if rng.random() < self.weightMutRate and len(chld.conn) > 0:
                    chld.conn[rng.choice(range(len(chld.conn)))].w += rng.random()/8
                    
                newPop += [Organism(genome=chld)]
            s = Species(rng.choice(s.members))

        print '\tFittest organism alive for', int(max([org.age for org in self.orgs])/dt), 'frames'
        print '\t', ConnectGene.numInnovations, 'total innovations thus far'
        print '\tNumber of species:', len(self.species)
        #print '\tMaximum distance between organisms:', maxDist
        
        """
        fittest = max(self.orgs, key=lambda x: x.genome.fit)
        print 'Genome of fittest organism:'
        print fittest.genome
        print ''
        """
        rng.shuffle(newPop)
        self.orgs = newPop[:len(self.orgs)]
        self.food = [Food() for x in xrange(40)]
        self.start = clock()
        self.selected = -1
        self.generation += 1
