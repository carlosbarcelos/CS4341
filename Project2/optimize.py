# -*- coding: utf-8 -*-

'''
CS 4341: Assignment 2
Feburary 3, 2017
Carlos Barcelos
Connor Smith
Justin Myerson
Ryan Walsh
'''

''' ===== Definitions ===== '''

import sys
import math
import random
import time
import copy
import queue

TRUE = 1
FALSE = 0

HILL_CLIMBING = 1
ANNEALING = 2
GA = 3

#genetic algorithm tuning
START_POP_SIZE = 200
MAX_POP_SIZE = 1000000
CUL_RATE = .1
ELT_RATE = .1
MUT_RATE = .05

BIN1 = None
BIN2 = None
BIN3 = None

''' ===== Classes ===== '''

class bin1:
# Bin1 class definition
  def __init__(self, values, score=0):
    self.values = values
    self.score = score
  
  def __str__(self):
    return str(self.values)
  
# Score = +(n1)-(n2)+(n3)-(n4)... 
  def getScore(self):
    cnt = 0
    score = 0
    for val in self.values:
      if(cnt % 2 == 0):
        score += val
      else:
        score -= val
      cnt += 1
    self.score = score
    return self.score
  
class bin2:
# Bin2 class definition
  def __init__(self, values, score=0):
    self.values = values
    self.score = score
  
  def __str__(self):
    return str(self.values)

# Score is defined as ...
  def getScore(self):
    score = 0
    if len(self.values) == 1:
      score = 0
      self.score = score
      return self.score
    for i in range(0,len(self.values)-1):
      if(self.values[i] < self.values[i+1]):   # ... if (i) < (i+1) -> +3
        score += 3
      elif(self.values[i] > self.values[i+1]): # ... if (i) > (i+1) -> -10
        score -= 10
      elif(self.values[i] == self.values[i+1]): # ... if (i) = (i+1) -> +5
        score += 5
    self.score = score
    return self.score

class bin3:
# Bin3 class definition
  def __init__(self, values, score=0):
    self.score = score
    self.first_half = None
    self.second_half = None
    self.values = values
    self.first_half, self.second_half = separate(values)
  
  def __str__(self):
    return str(self.values)

# Score is defined as ...
  def getScore(self):
    # Calculate first_half_score
    score = 0
    for val in self.first_half:
      if val < 0:        # isNegative -> -2
        score -= 2
      elif isPrime(val): # isPositivePrime -> +4
        score += 4
      else:              # isPositiveComposite -> -val
        score -= val
    # Calculate second_half_score
    for val in self.second_half:
      if val < 0:        # isNegative -> +2
        score += 2
      elif isPrime(val): # isPositivePrime -> -4
        score -= 4
      else:              # isPositiveComposite -> +val
        score += val
    self.score = score
    return self.score
        
class species:
# Species class allows a list to be processed by a priority queue for GA
  def __init__(self, genome):
    self.genome = genome
    self.fitness = fitness_fn(self.genome)

  def __str__(self):
    return str(self.genome)
    
  def __hash__(self):
    return fitness_fn(genome)

  def __lt__(self, other):
    return self.fitness > other.fitness

  def __eq__(self, other):
    return self.fitness == other.fitness

  def __len__(self):
    return len(self.genome)
  
''' ===== Algorithms ===== '''

def hill_climbing(bin1, bin2, bin3):
  bin_hold1 = copy.deepcopy(bin1) #These bin-holds are meant to be able to go to fresh start if time permits
  bin_hold2 = copy.deepcopy(bin2)
  bin_hold3 = copy.deepcopy(bin3)
  bestScore = totalScore(bin1, bin2, bin3)
  counter = 0
  bestAnswer = []
  bestAnswer.append(bin1)
  bestAnswer.append(bin2)
  bestAnswer.append(bin3)
  bestAnswer.append(bestScore)

  initial_time = time.time()
  current_time = time.time()
  while current_time - initial_time < TIME_LIMIT:
    counter = 0
    bin1 = copy.deepcopy(bin_hold1)
    bin2 = copy.deepcopy(bin_hold2)
    bin3 = copy.deepcopy(bin_hold3)
    bestScore = totalScore(bin1, bin2, bin3)
    while counter < 100:
      current_time = time.time()
      if current_time - initial_time > TIME_LIMIT:
        break

      first = random.randint(1, 3)
      second = random.randint(1, 3)
      rand_val1 = random.randint(0, len(bin1.values) - 1)
      rand_val2 = random.randint(0, len(bin1.values) - 1)
      
      if first == 1:
        bin_value1 = bin1.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if internal_bin_score(bin1, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if score_evaluate(bin1, bin2, bin3, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if score_evaluate(bin1, bin3, bin2, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      elif first == 2:
        bin_value1 = bin2.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if score_evaluate(bin2, bin1, bin3, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if internal_bin_score(bin2, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if score_evaluate(bin2, bin3, bin1, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      elif first == 3:
        bin_value1 = bin3.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if score_evaluate(bin3, bin1, bin2, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if score_evaluate(bin3, bin2, bin1, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if internal_bin_score(bin3, bin_value1, bin_value2, rand_val1, rand_val2) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      else:
        print("YOU DONE MESSED UP")
    if bestScore > bestAnswer[3]:
      bestAnswer[0] = bin1
      bestAnswer[1] = bin2
      bestAnswer[2] = bin3
      bestAnswer[3] = bestScore
      print("Current Best Score: " + str(bestAnswer[3]))
    #print("Best Score: " + str(bestScore))
    #print("Total Score: " + str(totalScore(bin1, bin2, bin3)))
  return bestAnswer[0], bestAnswer[1], bestAnswer[2], bestAnswer[3]

#Helper Hill Climbing
def score_evaluate(bin1, bin2, bin3, bin_value1, bin_value2, spot1, spot2):
  bin_holder1 = copy.copy(bin1)
  bin_holder2 = copy.copy(bin2)
  bin_holder3 = copy.copy(bin3)
  bestScore = totalScore(bin_holder1, bin_holder2, bin_holder3)
  #print(str(bestScore))
  bin_holder1.values[spot1] = bin_value2
  bin_holder2.values[spot2] = bin_value1
  #print(str(totalScore(bin_holder1, bin_holder2, bin_holder3)))
  if totalScore(bin_holder1, bin_holder2, bin_holder3) > bestScore:
    return TRUE
  else:
    bin_holder1.values[spot1] = bin_value1
    bin_holder2.values[spot2] = bin_value2
    totalScore(bin_holder1, bin_holder2, bin_holder3)
    return FALSE

#Helper Hill climbing
def internal_bin_score(bin1, bin_value1, bin_value2, spot1, spot2):
  bin_holder = copy.copy(bin1)
  bestScore = bin_holder.getScore()
  #print(str(bestScore))
  bin_holder.values[spot1] = bin_value2
  bin_holder.values[spot2] = bin_value1
  #print(bin_holder.getScore())
  if bin_holder.getScore() > bestScore:
    return TRUE
  else:
    bin_holder.values[spot1] = bin_value1
    bin_holder.values[spot2] = bin_value2
    bin_holder.getScore()
    return FALSE

#Helper annealing
def ann_score_evaluate(bin1, bin2, bin3, bin_value1, bin_value2, spot1, spot2, initial_time):
  bin_holder1 = copy.copy(bin1)
  bin_holder2 = copy.copy(bin2)
  bin_holder3 = copy.copy(bin3)
  bestScore = totalScore(bin_holder1, bin_holder2, bin_holder3)
  #print(str(bestScore))
  bin_holder1.values[spot1] = bin_value2
  bin_holder2.values[spot2] = bin_value1
  #print(str(totalScore(bin_holder1, bin_holder2, bin_holder3)))
  if totalScore(bin_holder1, bin_holder2, bin_holder3) > bestScore:
    return TRUE
  else:
    delta_e = totalScore(bin_holder1, bin_holder2, bin_holder3) - bestScore
    if delta_e == 0:
      delta_e = -0.2
    probability = anneal_prob(delta_e, initial_time)
    rand_val = random.random()
    if rand_val < probability:
      #print("picked worse move with probability = " + str(probability))
      return TRUE
    else:
      bin_holder1.values[spot1] = bin_value1
      bin_holder2.values[spot2] = bin_value2
      totalScore(bin_holder1, bin_holder2, bin_holder3)
      return FALSE
    
#Helper Annealing  
def ann_internal_bin_score(bin1, bin_value1, bin_value2, spot1, spot2, initial_time):
  bin_holder = copy.copy(bin1)
  bestScore = bin_holder.getScore()
  #print(str(bestScore))
  bin_holder.values[spot1] = bin_value2
  bin_holder.values[spot2] = bin_value1
  #print(bin_holder.getScore())
  if bin_holder.getScore() > bestScore:
    return TRUE
  else:
    delta_e = bin_holder.getScore() - bestScore
    if delta_e == 0:
      delta_e = -0.2
    probability = anneal_prob(delta_e, initial_time)
    rand_val = random.random()
    if rand_val < probability:
      #print("picked worse move with probability = " + str(probability))
      return TRUE
    else:
      bin_holder.values[spot1] = bin_value1
      bin_holder.values[spot2] = bin_value2
      bin_holder.getScore()
      return FALSE

# Simulated Annealing
def simulated_annealing(bin1, bin2, bin3):
  bin_hold1 = copy.deepcopy(bin1) #These bin-holds are meant to be able to go to fresh start if time permits
  bin_hold2 = copy.deepcopy(bin2)
  bin_hold3 = copy.deepcopy(bin3)
  bestScore = totalScore(bin1, bin2, bin3)
  counter = 0
  bestAnswer = []
  bestAnswer.append(bin1)
  bestAnswer.append(bin2)
  bestAnswer.append(bin3)
  bestAnswer.append(bestScore)

  initial_time = time.time()
  current_time = time.time()

  while current_time - initial_time < TIME_LIMIT:
    #print("Restart")

    anneal_time = time.time()

    counter = 0
    bin1 = copy.deepcopy(bin_hold1)
    bin2 = copy.deepcopy(bin_hold2)
    bin3 = copy.deepcopy(bin_hold3)
    bestScore = totalScore(bin1, bin2, bin3)
    while counter < 100:
      current_time = time.time()
      if current_time - initial_time > TIME_LIMIT:
        break

      first = random.randint(1, 3)
      second = random.randint(1, 3)
      rand_val1 = random.randint(0, len(bin1.values) - 1)
      rand_val2 = random.randint(0, len(bin1.values) - 1)
      
      if first == 1:
        bin_value1 = bin1.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if ann_internal_bin_score(bin1, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if ann_score_evaluate(bin1, bin2, bin3, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if ann_score_evaluate(bin1, bin3, bin2, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin1.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      elif first == 2:
        bin_value1 = bin2.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if ann_score_evaluate(bin2, bin1, bin3, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if ann_internal_bin_score(bin2, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if ann_score_evaluate(bin2, bin3, bin1, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin2.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      elif first == 3:
        bin_value1 = bin3.values[rand_val1]
        if second == 1:
          bin_value2 = bin1.values[rand_val2]
          if ann_score_evaluate(bin3, bin1, bin2, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin1.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 2:
          bin_value2 = bin2.values[rand_val2]
          if ann_score_evaluate(bin3, bin2, bin1, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin2.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
        elif second == 3:
          bin_value2 = bin3.values[rand_val2]
          if ann_internal_bin_score(bin3, bin_value1, bin_value2, rand_val1, rand_val2, anneal_time) == TRUE:
            bin3.values[rand_val1] = bin_value2
            bin3.values[rand_val2] = bin_value1
            bestScore = totalScore(bin1, bin2, bin3)
            counter = 0
            #print("Change")
          else:
            #print("No Change")
            counter += 1
      else:
        print("YOU DONE MESSED UP")
    if bestScore > bestAnswer[3]:
      bestAnswer[0] = bin1
      bestAnswer[1] = bin2
      bestAnswer[2] = bin3
      bestAnswer[3] = bestScore
      print("Current Best Score: " + str(bestAnswer[3]))
    #print("Best Score: " + str(bestScore))
    #print("Total Score: " + str(totalScore(bin1, bin2, bin3)))
  return bestAnswer[0], bestAnswer[1], bestAnswer[2], bestAnswer[3] 

# Genetic Algorithm - with elitism, mutation and optimal with population size
# The population is the list of all numbers being input
# 
def genetic_algorithm(values, population_size, max_population_size, culling_rate, elitism_rate, mutation_rate):
  # Create randomly generated population
  breeding_population = generate_population(values, population_size)
  population_pq = queue.PriorityQueue()
  
  #Configure the time
  initial_time = time.time()
  elapsed_time = time.time() - initial_time

  while (len(breeding_population) < max_population_size) and (elapsed_time < TIME_LIMIT):
    # Iterate over the population until population full or time is up
    for member in breeding_population: # Do for all member
      population_pq.put(member)
    population_size = population_pq.qsize()
  
      # Preserve the elite
    elite_species = []
    for i in range(0,math.floor(elitism_rate * population_size)): 
      s = population_pq.get()
      elite_species.append(s)
    # Numerate the common
    not_elite_species = []
    for i in range(0, math.floor((1-elitism_rate-culling_rate) * population_size)): 
      s = population_pq.get()
      not_elite_species.append(s)
    # Cull the bottom GA_CULLING
    for i in range(0, math.floor(culling_rate * population_size)):
      g = population_pq.get()
  
    breeding_population = not_elite_species + elite_species
  
    # Reproduce between the elite and the common
    child_population = []
    
    #random.shuffle(breeding_population)
    #if (len(breeding_population) % 2) != 0: # The odd man out will not breed
    #  breeding_population.pop()
    breed_amount = int(len(breeding_population)/2)
    for i in range(0, breed_amount):
      parentA = randomSelection(breeding_population)
      parentB = randomSelection(breeding_population)
      first_child, second_child = reproduce(parentA, parentB)
      if random.randrange(0,int(1/mutation_rate)): # mutation_rate% chance to mutate
        first_child = mutate(first_child)
      if random.randrange(0,int(1/mutation_rate)):
        second_child = mutate(second_child)
        
      child_population.append(first_child) # Add children to their own population
      child_population.append(second_child)
    
    # The next generation is this generations elite plus the children
    breeding_population = child_population + elite_species
    elapsed_time = time.time() - initial_time
    
  # Return the most fit species
  for member in breeding_population: # Do for all member
    population_pq.put(member)
  most_fit = population_pq.get()

  return most_fit

# GA Helper: Randomly chooses a genome (weighted towards higher fitness)
def randomSelection(new_population):
  # Set weights
  my_weights = []
  for i in range(0,len(new_population)):
    fit = new_population[i].fitness
    w = 0.5 + (0.5 * (fit / (abs(fit) + 10)))
    my_weights.append(w)
  p = random.choices(new_population, weights=my_weights)
  pos = new_population.index(p[0])
  return p[0]

# GA Helper: Reproduces some parentA with some parentB
def reproduce(parentA, parentB):
  n = int((len(parentA)/3))
  # Divide the genome of the parents
  A_strand1 = parentA.genome[:n+1]
  A_strand2 = parentA.genome[n+1:]
  B_strand1 = parentB.genome[:n+1]
  B_strand2 = parentB.genome[n+1:]

  # Switch the parts
  first_genome = A_strand1 + B_strand2
  second_genome = B_strand1 + A_strand2
  
  # Make the children
  first_child = species(first_genome)
  second_child = species(second_genome)
  return first_child, second_child

# GA Helper: Mutates a random number within a child genome
def mutate(child):
  genome = child.genome
  mutate_pos1 = random.randint(0, len(genome)-1)
  mutate_pos2 = random.randint(0, len(genome)-1)
  temp = genome[mutate_pos1]
  genome[mutate_pos1] = genome[mutate_pos2]
  genome[mutate_pos2] = temp

  child = species(genome)
  return child

# GA Helper: Returns as many 
def generate_population(values, population_size):
  population = []
  current_population = []
  originalValues = values
  for i in range(0,population_size):
    random.shuffle(values)
    s = species(values)
    population.append(s)
  return population    

''' ===== Helper Functions ===== '''

#Calculates the total score of all three bins
def totalScore(bin1, bin2, bin3):
  bin_holder1 = bin1
  bin_holder2 = bin2
  bin_holder3 = bin3
  totalScore = bin_holder1.getScore() + bin_holder2.getScore() + bin_holder3.getScore()
  return totalScore

#get the probability for the annealing function
def anneal_prob(delta_e, initial_time):
    prob = 0.0
    exp = 0.0
    T = 0.0

    current_time = time.time()
    time_diff = current_time - initial_time
    if (time_diff == 0.0):
        time_diff = 0.001

    #get the T value
    T = 1/time_diff
    # print ("T = " + str(T))
    # print ("Time elapsed = " + str(time_diff))

    exp = delta_e/T
    prob = math.e**exp

    return prob


# Separate the input into a first_half and a second_half
def separate(values):
    half = int(math.ceil(len(values)/2)) # Find midway point
    if len(values) % 2 == 0:        # If even, split as normal
        first_half = values[:half]
        second_half = values[half:]
    else:                           # If odd, ignore middle value
        first_half = values[:half-1]
        second_half = values[half:]
    return first_half, second_half

# Returns (TRUE/FALSE) whether or not a number is prime
def isPrime(n):
    if n==2 or n==3:  # Is a base number?
        return TRUE
    if n%2==0 or n<2: # Is less even or less than 2
        return FALSE
    for i in range(3, int(n**0.5)+1, 2): # Every odd number
        if n%i==0:
          return FALSE
    return TRUE 

# Read a file using space-delimited file
def read_file(inputfile):
    f = open (inputfile , 'r')
    #read the string input
    l = [line.split(' ') for line in f]
    f.close()

    array = []
    #convert to integers and return
    for val in l:
      array.append(val)
    return array

# Calculate the fitness of the memeber
def fitness_fn(member):
  # Parse the input for the three bins
  n = int((len(member)/3))
  in_1 = member[:n]
  in_2 = member[n:2*n]
  in_3 = member[2*n:3*n]
  
  b1 = bin1(in_1)
  b2 = bin2(in_2)
  b3 = bin3(in_3)

  s1 = b1.getScore()
  s2 = b2.getScore()
  s3 = b3.getScore()
  
  return s1 + s2 + s3

''' Main function. Execution from command line. '''
def init(values=[1,2,3]):
    global BIN1
    global BIN2
    global BIN3
    BIN1 = bin1(values)
    BIN2 = bin2(values)
    BIN3 = bin3(values)
    
    global ALGORITHM
    random.seed()

def main(argv):
    '''
    You should submit a program named optimize that takes three command line arguments:
    1.      The type of optimization to use:  hill, annealing, ga
    2.      The name of the input file containing the list of numbers
    3.      The amount of time in seconds – can be floating point.
    '''

    init()
    if(len(argv) != 4): # {1:}
        print("Please reconsider your command line input for running this program:")
        print("  $> optimize <optimization_type> <input_file> <time>")
        print("  Optimization Types:")
        print("    1 = Hill Climbing:")
        print("    2 = Simulated Annealing")
        print("    3 = Genetic Algorithm")
      #return 0

        my_arr = [1,2,3,1,2,3]
        print(my_arr)
        my_arr.remove(1)
        print(my_arr)
        return 0
      
  #determine what algorithm to use:
    if argv[1].strip() == "hill":
        ALGORITHM = HILL_CLIMBING
    elif argv[1].strip() == "annealing":
        ALGORITHM = ANNEALING
    elif argv[1].strip() == "ga":
        ALGORITHM = GA
    elif argv[1].strip() == "test":
        ALGORITHM = TEST
    else:
        print("ERROR - algorithm selection")
        print("second inputs param should be one of the following:")
        print("    'hill'      = Hill Climbing:")
        print("    'annealing' = Simulated Annealing")
        print("    'ga'        = Genetic Algorithm")
        print("argv[1] = " + argv[1])
        return 1

    #open the file and extract the data
    val_list = read_file(argv[2])
    #static length
    len_vals = len(val_list[0])

    #assign the numbers randomly to the bins
    #shuffle the ordering and assign first third, next third, final third
    random.shuffle(val_list[0])

    bin_capacity = int(len_vals/3) #should divide evenly (problem description)

    bin1_holder = []
    bin2_holder = []
    bin3_holder = []

    #sanity check if num values divisible by 3
    if (len_vals % 3 != 0):
        print("ERROR - error in input file. Number of values not divisible by 3")
        print("NOTE: Do not have a 'space' at the end of the input file")
        return 1

    print ("Amount of values in input file: " + str(len_vals))
    
    #sanity check if input is more than 9,999
    if (len_vals > 9999):
        print("ERROR - error in input file. Number of values is too great")
        print("NOTE: The maximum input length is 9999")
        return 1
      
    #global holding integer version of input array
    global INT_INPUT
    INT_INPUT = []
    for val in val_list[0]:
        if int(val) > 9 or int(val) < -9:
            print("ERROR - All values must be between -9 and 9, inclusive")
            return 1
        INT_INPUT.append(int(val))

    #fill each bin
    for i in range(0,3):
        for val in range(0,bin_capacity):
            if i == 0:
                bin1_holder.append(int(val_list[0][0]))
                #print (val_list[0][0])
                val_list[0].remove(val_list[0][0])
            elif i == 1:
                bin2_holder.append(int(val_list[0][0]))
                #print (val_list[0][0])
                val_list[0].remove(val_list[0][0])
            elif i == 2:
                bin3_holder.append(int(val_list[0][0]))
                #print (val_list[0][0])
                val_list[0].remove(val_list[0][0])
            else:
                print("ERROR - error allocating random values to the bins")

    BIN1 = bin1(bin1_holder)
    BIN2 = bin2(bin2_holder)
    BIN3 = bin3(bin3_holder)

    #print("our bins:")
    #print(BIN1)
    #print(BIN2)
    #print(BIN3)

    #determine the amount of time to use (floats)
    global TIME 
    global TIME_LIMIT
    TIME = 0.0
    TIME_LIMIT = 0.0

    TIME_LIMIT = float(argv[3])

    #execute algorithm:
    if ALGORITHM == HILL_CLIMBING:
        print("exec hill climb")
        score = totalScore(BIN1, BIN2, BIN3)
        print("initial score: " + str(score))
        BIN1, BIN2, BIN3, score = hill_climbing(BIN1, BIN2, BIN3)
        print("DONE")
        #print(BIN1)
        #print(BIN2)
        #print(BIN3)
        print("Final Score: " + str(score))
    elif ALGORITHM == ANNEALING:
        print("exec annealing")
        score = totalScore(BIN1, BIN2, BIN3)
        print("initial score = " + str(score))
        BIN1, BIN2, BIN3, score = simulated_annealing(BIN1, BIN2, BIN3)
        print("DONE")
        print("Final Score: " + str(score))
    elif ALGORITHM == GA:
        print("exec genetic algorithm")
        score = totalScore(BIN1, BIN2, BIN3)
        print("initial score: " + str(score))
        most_fit = genetic_algorithm(INT_INPUT, START_POP_SIZE, MAX_POP_SIZE, CUL_RATE, ELT_RATE, MUT_RATE)
        print("DONE")
        print("The most fit species:")
        #print("  Genome: " + str(most_fit.genome))
        print("  Fitness: " + str(most_fit.fitness))
    else:
        print("MAJOR ERROR - UNABLE TO DECIDE WHAT TO RUN")
if __name__ == "__main__":
    main(sys.argv)