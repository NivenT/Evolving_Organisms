from organism import *
from time import clock, sleep

def distSquared(pos1, pos2):
    return (pos1[0]-pos2[0])*(pos1[0]-pos2[0])+(pos1[1]-pos2[1])*(pos1[1]-pos2[1])

def partition(lst, size):
    return [lst[i:i+size] for i in xrange(0,len(lst),size)]

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
        self.orgs = [Organism() for x in xrange(30)]
        self.food = [Food() for x in xrange(25)]
        self.lastFoodUpdate = 0
        self.start = clock()

    def draw(self, screen):
        for org in self.orgs:
            if abs(org.hunger-100) < 100:
                org.draw(screen)
        for food in self.food:
            food.draw(screen)

    def update(self, dt):
        allDead = True
        #if rnd.uniform(0,1/dt) <= 1/(50-len(self.orgs)) and len(self.orgs) > 1:
        #    self.orgs += [self.crossover(rnd.choice(self.orgs),rnd.choice(self.orgs))]
        for food in self.food:
            food.update(dt)
            if 0 > food.lifespan:
                self.food.remove(food)
        if clock() - self.lastFoodUpdate >= 10:
            self.food += [Food() for x in xrange(rnd.randint(1,5))]
            self.lastFoodUpdate = clock()
        for org in self.orgs:
            if abs(org.hunger-100) < 100:
                allDead = False
                leftSmells = [0]*3
                rightSmells = [0]*3
                for food in self.food:
                    if distSquared(food.center,org.center) < (food.radius+org.radius)*(food.radius+org.radius):
                        org.hunger += {0: -10, 1: 5, 2: 15}[food.type]
                        self.food.remove(food)
                    else:
                        leftSmells[food.type] += np.exp(-distSquared(food.center,org.getLeftNostril())/(10**4))
                        rightSmells[food.type] += np.exp(-distSquared(food.center,org.getRightNostril())/(10**4))
                org.update(leftSmells+rightSmells, dt)
        if allDead:
            sleep(3)
            durr = int(round(clock()-self.start))
            print "Population survived for", durr/60, "minutes and", durr%60, "seconds"
            self.stepPopulation()

    def stepPopulation(self):
        minimumAge = min([org.age for org in self.orgs])
        totalFitness = sum([org.age-minimumAge for org in self.orgs])
        newPop = []
        while len(newPop) < len(self.orgs):
            rand = rnd.uniform(0,totalFitness)
            for org in self.orgs:
                if org.age-minimumAge > rand:
                    dad = org
                    break
                rand -= org.age-minimumAge
            rand = rnd.uniform(0,totalFitness)
            for org in self.orgs:
                if org.age-minimumAge > rand:
                    mom = org
                    break
                rand -= org.age-minimumAge
            newPop.append(self.crossover(mom,dad))
        self.orgs = newPop
        self.food = [Food() for x in xrange(25)]
        self.lastFoodUpdate = clock()
        self.start = clock()

    def crossover(self, mom, dad):
        pivot = rnd.choice([80,180,200,210])
        genome = mom.getGenome()[:pivot] + dad.getGenome()[pivot:]

        q = 1.-(1.-.1)**(1/212.)
        for i in xrange(212):
            if rnd.uniform(0,1) <= q:
                genome[i] += rnd.uniform(-2,2)
                
        rnn = RNN(8,10,2)
        rnn.W_hx = np.array(partition(genome[:80],8))
        rnn.W_hh = np.array(partition(genome[80:180],10))
        rnn.W_ah = np.array(partition(genome[180:200],10))
        rnn.b_h  = np.array(genome[200:210])
        rnn.b_a  = np.array(genome[210:212])
        return Organism(brain=rnn)
        
