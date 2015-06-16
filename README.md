# Evolving_Organisms
Attempting to "evolve" intelligent behavior using genetic algorithms

## Overview of the Program
This program is a simulation of evolution of simple creatures. The user does not interact with the program in any way and simply watches as the creatures move around in their environment. When every creature has died, the program assigns each creature a fitness based on how long it lived. It then repopulates the environment by breeding the creatures from the previous generation in order to make creatures for the next generation. The probabily that a creature is selected for breeding is directly proportional to its fitness.

## General Details
### The Organisms
The organisms (as of yet unnamed) are simple creatures. They have a simple body and two "noses". Their movement is controlled by a recurrent neural network that takes as input what each of their two noses is smelling and their current hunger, and outputs the angle in radians they should turn as well as the speed they should move. The hunger of an organism is a representation of its health. It starts out at 100 and constantly decreases. When it hits 0 (starved) or 200 (overfed), they die. Hunger can be increased by eating food found in the environment. Organism also have an age (constantly increasing) as this is used to represent their fitness at the end of each generation. 
### The Environment
The environment is, more or less, a collection of organisms and food. There are three types of food: red, green, and blue. Red food is bad for the organisms (think poison) and actually decreases their hunger. Green and blue foods are good for the organisms and increases their hunger. The blue food increases hunger more than the green food. Every food is spawned with a random lifespan. When this much time has passed, the food is removed (rotted away). When all organisms are dead, the environment is updated by replacing all the food and introducing the next generation of organisms. Because there are three types of food, the organisms have 6 inputs for smell (3 for each nose). Each food gives off a smell whose intensity varies as a gaussian.

## Genetic Algorithm Details
### Fitness function
The fitness function used is simply the age of the organism minus the minimum age of all the organisms.
### Parent selection
Parents are selected using a roulette wheel approach. The parents are chosen in succesion by randomly choosing an organism from the previous generation. The probabily that a given organism is chosen is directly proportional to its fitness.
### Crossover
Crossover happens by first flattening all the weights in the RNNs of the parents into two lists. A pivot is then chosen at random, and a new list is created by concatenating the first parent's weights up to the pivot with the second parent's weights from the pivot onwards. This list is then used as the weights for the child's RNN.
### Mutation
The only possible mutation is adding a number from -2 to 2 to one of the weights of the child. For code simplicity this is done during crossover before the child's RNN has been created.

## Notes
* There currently is not a fast forward feature. The simulation cannot be sped up.
* Requires Pygame and Numpy
