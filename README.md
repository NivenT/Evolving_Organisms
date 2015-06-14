# Evolving_Organisms
Attempting to "evolve" intelligent behavior using genetic algorithms

## General Details
The program consists of organisms living in an environment. 

The organisms (as of yet unnamed) are simple creatures. They have a simple body and two "noses". Their movement is controlled by a recurrant neural network that takes as input what each of their two noses is smelling and their current hunger, and outputs the angle in radians they should turn. The hunger of an organism is a representation of its health. It starts out at 100 and constantly decreases. When it hits 0 (starved) or 200 (overfed), they die. Hunger can be increased by eating food found in the environment. Organism also have an age (constantly increasing) as this is used to represent their fitness at the end of each generation.

The environment is, more or less, a collection of organisms and food. There are three types of food: red, green, and blue. Red food is bad for the organisms (think poison) and actually decreases their hunger. Green and blue foods are good for the organisms and increases their hunger. I feel the need to note that by increases/decreases their hunger what is meant is that the organisms hunger field rises or falls respectively and not that the organism gets more/less hungry. The blue food increases hunger more than the green food. When all organisms are dead, the environment is updated by replacing all the food and introducing the next generation of organisms.

## Genetic Algorithm Details
### Fitness function
The fitness function used is simply the age of the organism
### Parent selection
Parents are selected using a roulette wheel approach. The parents are chosen in succesion by randomly choosing an organism from the previous generation. The probabily that a given organism is chosen is directly proportional to its fitness
### Crossover
Crossover happens by first flattening all the weights in the RNNs of the parents into to lists. A pivot is then chosen at random, and a new list is created by concatenating the first parent's weights up to the pivot with the second parent's weights from the pivot onwards. This list is then used as the weights for the child's RNN.
### Mutation
The only possible mutation is adding a number from -1 to 1 to one of the weights of the child. For code simplicity this is done during crossover before the child's RNN has been created.

### Notes
* I only recently finished this so I have not had much time to extensively test it.
* Organisms generally move in circles at first. After a few hours, however, some will display more intelligent behaviors. i.e turning towards food that is near them
* There currently is not a fast forward feature. The simulation cannot be sped up.
