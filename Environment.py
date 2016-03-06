from organism import *
from time import clock, sleep

def distSquared(pos1, pos2):
    return (pos1[0]-pos2[0])*(pos1[0]-pos2[0])+(pos1[1]-pos2[1])*(pos1[1]-pos2[1])

def partition(lst, size):
    return [lst[i:i+size] for i in xrange(0,len(lst),size)]

def angBetween(vec1, vec2):
    return np.arccos(np.dot(vec1,vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2)))

class Food(object):
    def __init__(self):
        self.center = (int(rnd.uniform(0,800)), int(rnd.uniform(0,600)))
        self.radius = 5
        self.type = int(round(rnd.uniform(0,2)))
        self.color = {0: (255,0,0), 1: (0,255,0), 2: (0,0,255)}[self.type]
        self.lifespan = rnd.randint(50,200)
    def draw(self, screen):
        pg.draw.circle(screen, self.color, self.center, self.radius)
    def update(self, dt):
        self.lifespan -= dt
        
class Environment(object):
    def __init__(self):
        self.orgs = [Organism() for x in xrange(20)]
        self.food = [Food() for x in xrange(25)]
        self.lastFoodUpdate = 0
        self.start = clock()

        self.generation = 1
        self.nodeMutRate   = .1
        self.connMutRate   = .15
        self.weightMutRate = .2
        self.enableRate    = .25

    def draw(self, screen):
        for org in self.orgs:
            if abs(org.hunger-100) < 100:
                org.draw(screen)
        for food in self.food:
            food.draw(screen)

    def updateFood(self, dt):
        for food in self.food:
            food.update(dt)
            if 0 > food.lifespan:
                self.food.remove(food)
        if clock() - self.lastFoodUpdate >= 8:
            self.food += [Food() for x in xrange(rnd.randint(1,5))]
            self.lastFoodUpdate = clock()

    def updateOrgs(self, dt):
        anyAlive = False
        for org in self.orgs:
            if abs(org.hunger-100) < 100:
                anyAlive = True
                
                leftSmells = rightSmells = [0]*3
                for food in self.food:
                    combinedRadii = food.radius+org.radius
                    if distSquared(food.center,org.center) < combinedRadii*combinedRadii:
                        org.hunger += {0: -10, 1: 5, 2: 15}[food.type]
                        self.food.remove(food)
                    elif distSquared(food.center, org.center) < 15000:
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

    def stepPopulation(self, dt):
        minAge = min([org.age for org in self.orgs])
        totFit = 0
        for org in self.orgs:
            org.genome.fit = org.age-minAge
            totFit += org.genome.fit
            
        newPop = []
        while len(newPop) < len(self.orgs):
            rand, index = rng.uniform(0, totFit), 0
            while self.orgs[index].genome.fit < rand:
                rand -= self.orgs[index].genome.fit
                index += 1
            dad = self.orgs[index]
            rand, index = rng.uniform(0, totFit), 0
            while self.orgs[index].genome.fit < rand:
                rand -= self.orgs[index].genome.fit
                index += 1
            mom = self.orgs[index]

            chld = dad.genome.cross(mom.genome, self.enableRate)
            if rng.random() < self.nodeMutRate:
                chld.mutateAddNode()
            elif rng.random() < self.connMutRate:
                chld.mutateAddConnection()
            elif rng.random() < self.weightMutRate and len(chld.conn) > 0:
                chld.conn[rng.choice(range(len(chld.conn)))].w += rng.random()/8
            newPop += [Organism(genome=chld)]

        print '\tFittest organism alive for', int(max([org.age for org in self.orgs])/dt), 'frames'
        print '\t', ConnectGene.numInnovations, 'total innovations thus far'
        """
        fittest = max(self.orgs, key=lambda x: x.genome.fit)
        print 'Genome of fittest organism:'
        print fittest.genome
        print ''
        """
        self.orgs = newPop
        self.food = [Food() for x in xrange(25)]
        self.lastFoodUpdate = clock()
        self.start = clock()
        self.generation += 1
