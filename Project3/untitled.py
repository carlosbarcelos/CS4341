'''
CS 4341: Assignment 3
Feburary 17, 2017
Carlos Barcelos
Connor Smith
Justin Myerso
Ryan Walsh
'''

''' Page 533 Text book
function REJECTION-SAMPLING(X,e,bn,N) returns an estimate of P(X|e)
  inputs: X, the query variable
          e, observedvalues forvariables E
          bn, a Bayesian network
          N, the total numberof samples to be generated
  local variables: M, a vector of counts for each value of X, initially zero
  
  for j = 1 to N do
    x←PRIOR-SAMPLE(bn)
    if x is consistent with e then
      M[x]←M[x]+1 where x is the value of X in x
  return NORMALIZE(M)
  
  
function PRIOR-SAMPLE(bn) returns an event sampled from the prior speciﬁed by bn
    inputs: bn, a Bayesian network specifyingjoint distribution P(X1,...,Xn)
  
  x←an event with n elements
  foreach variable Xi in X1,...,Xn do
    x[i]←a random sample from P(Xi | parents(Xi))
  return x
  
function NORMALIZE(a,b)
    return a/(a+b), b/(a+b)

'''

''' ===== Definitions ===== '''
import sys
import math
import random
import time
import copy

TRUE = 1
FALSE = 0

# "!" denotes that the node has no affecting parent
hum_cpt = [
    ("!", "low", 0.2),
    ("!", "medium", 0.5),
    ("!", "high", 0.3)
  ]
tmp_cpt = [
    ("!" , "warm", 0.1),
    ("!" , "mild", 0.4),
    ("!" , "cold", 0.5)  
  ]
ice_cpt = [
    ("humidity", "low", "temperature", "warm", 0.001),
    ("humidity","low", "temperature", "mild", 0.01),
    ("humidity","low", "temperature", "cold", 0.05),
    ("humidity", "medium", "temperature", "warm", 0.001),
    ("humidity", "medium", "temperature", "mild", 0.03),
    ("humidity", "medium", "temperature", "cold", 0.2),
    ("humidity", "high", "temperature", "warm", 0.005),
    ("humidity", "high", "temperature", "mild", 0.01),
    ("humidity", "high", "temperature", "cold", 0.35)
  ]
snw_cpt = [
    ("humidity" , "low", "temperature" , "warm", 0.0001),
    ("humidity" , "low", "temperature" , "mild", 0.001),
    ("humidity" , "low", "temperature" , "cold", 0.1),
    ("humidity" , "medium", "temperature" , "warm", 0.0001),
    ("humidity" , "medium", "temperature" , "mild", 0.0001),
    ("humidity" , "medium", "temperature" , "cold", 0.25),
    ("humidity" , "high", "temperature" , "warm", 0.0001),
    ("humidity" , "high", "temperature" , "mild", 0.001),
    ("humidity" , "high", "temperature" , "cold", 0.4)
  ]
cld_cpt = [
    ("snow" , "false", 0.3),
    ("snow" , "true", 0.9)
  ]
day_cpt = [
    ("!" , "weekend", 0.2),
    ("!" , "weekday", 0.8)
  ]
exm_cpt = [
    ("snow" , "false", "day" , "weekend", 0.001),
    ("snow" , "false", "day" , "weekday", 0.1),
    ("snow" , "true", "day" , "weekend", 0.0001),
    ("snow" , "true", "day" , "weekday", 0.3)
  ]
str_cpt = [
    ("snow" , "false", "exam" , "false", 0.01),
    ("snow" , "false", "exam" , "true", 0.2),
    ("snow" , "true", "exam" , "false", 0.1),
    ("snow" , "true", "exam" , "true", 0.5)
  ]

''' ===== Classes ===== '''

class node:
# Node class to fill Bayseian Network
  def __init__(self, name, cpt, bool, value=-1):
    self.name = name
    self.cpt = cpt
    self.bool = bool
    self.value = value
  
  def hasParent(self, bool):
     return self.bool

class network:
# Bayseian Network class
  def __init__(self, graph={}):
    self.graph = graph
    
  def add_edge(self, from_node, to_node):
    if(from_node in self.graph):
      self.graph[from_node].append(to_node)
    else:
      self.graph[from_node] = [to_node]



# Convert the query string into the node and state in question
# node: The node in question
# value: THe cooresponding, observed state
def parse_query(query):
  node, value = query.split("=",2)
  return node, value

# Convert the array of observation strings into two lists
# nodes: The observed node
# values: The cooresponding, observed states
def parse_observations(observations):
  nodes = []
  values = []
  # Iterate through the observations
  for i in range(0,len(observations)):
    halves = observations[i].lower()
    half1, half2 = halves.split("=")
    nodes.append(half1)  # Put the nodes in one list
    values.append(half2) # Put observations in another list
  return nodes, values
        
''' ===== Algorithm ===== '''
# Returns an estimate of P(X|e)
def rej_sample(query, observations, bn, iterations):
  #parse input:
  q_node, q_value = parse_query(query)
  #both are lists: list of nodes, list of values, <- should correspond
  o_nodes, o_values = parse_observations(observations)
  
  successes = 0
  validSamples = 0
  SD = 0
  
  confidence = []
  
  original_bn = copy.copy(bn)
  for i in range(0,iterations):
    bn = copy.copy(original_bn) # Use the original, uninstantiated bn
    
    bn, result, query_result = instantiate(bn, q_node, q_value, o_nodes, o_values)
    if not result:
      continue # Reject this network configuration
    
    validSamples += 1
    if query_result:
      successes += 1
      
  if validSamples == 0:
    print("ERROR - no valid samples in the configuration")
    return 0, 0, 0, 0, 0
  
  prob = round((float(successes) / validSamples), 5)

  # Finally, calculate the standard deviation and 95% confidence
  
  SD = math.sqrt(prob * (1-prob))
  confidence.append(round(prob - 2 * (SD/math.sqrt(validSamples)), 5))
  confidence.append(round(prob + 2 * (SD/math.sqrt(validSamples)), 5))
  
  return successes, validSamples, prob, round(SD,5), confidence
  
# Create the sample enviornment
def instantiate(bn, q_node, q_value, o_nodes, o_values):
  result = FALSE
  query_result = FALSE
  # Initalize all the things
  
  num = random.uniform(0, 1) # Returns random number between 0 and 1
  humid = no_parent_prob("hum_cpt", num) 
  if "humidity" in o_nodes:
    o_node_index = o_nodes.index("humidity")
    if o_values[o_node_index] != humid:
      return bn, result, query_result
  if "humidity" == q_node:
    if q_value == humid:
      query_result = TRUE
      
  num = random.uniform(0, 1)
  temp = no_parent_prob("tmp_cpt", num)
  if "temperature" in o_nodes:
    o_node_index = o_nodes.index("temperature")
    if o_values[o_node_index] != temp:
      return bn, result, query_result
  if "temperature" == q_node:
    if q_value == temp:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  day = no_parent_prob("day_cpt", num)
  if "day" in o_nodes:
    o_node_index = o_nodes.index("day")
    if o_values[o_node_index] != day:
      return bn, result, query_result
  if "day" == q_node:
    if q_value == day:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  icy = two_parent_prob("ice_cpt", humid, temp, num)
  if "icy" in o_nodes:
    o_node_index = o_nodes.index("icy")
    if o_values[o_node_index] != icy:
      return bn, result, query_result
  if "icy" == q_node:
    if q_value == icy:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  snow = two_parent_prob("snw_cpt", humid, temp, num)
  if "snow" in o_nodes:
    o_node_index = o_nodes.index("snow")
    if o_values[o_node_index] != snow:
      return bn, result, query_result
  if "snow" == q_node:
    if q_value == snow:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  cloudy = one_parent_prob(snow, num)
  if "cloudy" in o_nodes:
    o_node_index = o_nodes.index("cloudy")
    if o_values[o_node_index] != cloudy:
      return bn, result, query_result
  if "cloudy" == q_node:
    if q_value == cloudy:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  exam = two_parent_prob("exm_cpt", snow, day, num)
  if "exams" in o_nodes:
    o_node_index = o_nodes.index("exams")
    if o_values[o_node_index] != exam:
      return bn, result, query_result
  if "exams" == q_node:
    if q_value == exam:
      query_result = TRUE
  
  num = random.uniform(0, 1)
  stress = two_parent_prob("str_cpt", snow, exam, num)
  if "stress" in o_nodes:
    o_node_index = o_nodes.index("stress")
    if o_values[o_node_index] != stress:
      return bn, result, query_result
  if "stress" == q_node:
    if q_value == stress:
      query_result = TRUE
  
  result = TRUE
  return bn, result, query_result
  
  '''
  list_of_nodes = []
  list_of_nodes.append(query)
  # Add all of the observations to a list
  for i in observations:
    list_of_nodes.append(i)
  
  # Iterate over the list
  for i in range (0, iterations):
    dummy_list = copy.copy(list_of_nodes)
    while dummy_list:
    '''

''' ===== Helper Functions ===== '''
#function for getting probabilities from our hardcoded probability tables
def query_table(table, param1, param2):
    if table == "ice_cpt":
        for i in ice_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "hum_cpt":
      for i in hum_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "tmp_cpt":
      for i in tmp_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "snw_cpt":
      for i in snw_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "cld_cpt":
      for i in cld_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "day_cpt":
      for i in day_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "exm_cpt":
      for i in exm_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "str_cpt":
      for i in str_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    else:
                print("major error - table not found")
        
#function to compute str-> which quality value to choose   -- on no-parent 
#use probab as bounds
def no_parent_prob(table, rand):
  if table == "hum_cpt":
    if rand >= 0 and rand <= 0.2:
      return "low"
    elif rand > 0.2 and rand <= 0.7:
      return "medium"
    elif rand > 0.7 and rand <= 1:
      return "high"
    else:
      print("error - no parent prob")
  
  #tmp_cpt
  elif table == "tmp_cpt":
    if rand >= 0 and rand <= 0.1:
      return "warm"
    elif rand > 0.1 and rand <= 0.5:
      return "mild"
    elif rand > 0.5 and rand <= 1:
      return "cold"
    else:
      print("error - no parent prob")
      
  #day_cpt
  elif table == "day_cpt":
    if rand >= 0 and rand <= 0.2:
      return "weekend"
    elif rand > 0.2 and rand <= 1:
      return "weekday"
    else:
      print("error - no parent prob")
      
  #safety guard
  else:
    print("major error - table not found")

def one_parent_prob(param1, rand):
  if param1 == "false":
    if rand <= .3:
      return "true"
    else:
      return "false"
  else:
    if rand <= .9:
      return "true"
    else:
      return "false"
  
def two_parent_prob(table, param1, param2, rand):
  # ice snw exm str
  if table == "ice_cpt":
    if param1 == "low":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.001:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.01:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.05:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    if param1 == "medium":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.001:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.03:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.2:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    if param1 == "high":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.005:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.01:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.35:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
  elif table == "snw_cpt":
    if param1 == "low":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.0001:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.001:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.1:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    if param1 == "medium":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.0001:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.0001:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.25:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    if param1 == "high":
      if param2 == "warm":
        if rand >= 0 and rand <= 0.0001:
          return "true"
        else:
          return "false"
      elif param2 == "mild":
        if rand >= 0 and rand <= 0.001:
          return "true"
        else:
          return "false"
      elif param2 == "cold":
        if rand >= 0 and rand <= 0.4:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    
  elif table == "exm_cpt":
    if param1 == "false":
      if param2 == "weekend":
        if rand >= 0 and rand <= 0.001:
          return "true"
        else:
          return "false"
      elif param2 == "weekday":
        if rand >= 0 and rand <= 0.1:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    if param1 == "true":
      if param2 == "weekend":
        if rand >= 0 and rand <= 0.0001:
          return "true"
        else:
          return "false"
      elif param2 == "weekday":
        if rand >= 0 and rand <= 0.3:
          return "true"
        else:
          return "false"
      else:
        print("You messed up.")
    
  elif table == "str_cpt":
    if param1 == "false":
      if param2 == "false":
        if rand >= 0 and rand <= 0.01:
          return "high"
        else:
          return "low"
      elif param2 == "true":
        if rand >= 0 and rand <= 0.2:
          return "high"
        else:
          return "low"
      else:
        print("You messed up.")
    if param1 == "true":
      if param2 == "false":
        if rand >= 0 and rand <= 0.1:
          return "high"
        else:
          return "low"
      elif param2 == "true":
        if rand >= 0 and rand <= 0.5:
          return "high"
        else:
          return "low"
      else:
        print("You messed up.")
  else:
    print("You messed up.")
          
''' ===== Main function ===== '''
# Initialize the Bayesian network
def init():
  hum_node = node("humidity", hum_cpt, FALSE)
  tmp_node = node("temperature", tmp_cpt, FALSE)
  ice_node = node("icy", ice_cpt, TRUE)
  snw_node = node("snow", snw_cpt, TRUE)
  cld_node = node("cloudy", cld_cpt, TRUE)
  day_node = node("day", day_cpt, FALSE)
  exm_node = node("exams", exm_cpt, TRUE)
  str_node = node("stress", str_cpt, TRUE)
  
  bn = network()
  bn.add_edge(hum_node, ice_node)
  bn.add_edge(hum_node, snw_node)
  bn.add_edge(tmp_node, ice_node)
  bn.add_edge(tmp_node, snw_node)
  bn.add_edge(snw_node, cld_node)
  bn.add_edge(snw_node, exm_node)
  bn.add_edge(snw_node, str_node)
  bn.add_edge(day_node, exm_node)
  bn.add_edge(exm_node, str_node)
  
  return bn

def query_table(table, param1, param2):
    if table == "ice_cpt":
        for i in ice_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "hum_cpt":
      for i in hum_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "tmp_cpt":
      for i in tmp_cpt:
            if i[1] == param1:
                print("FOUND")
                return (i[len(i) -1])
    elif table == "snw_cpt":
      for i in snw_cpt:
            if i[1] == param1 and i[3] == param2:
                print("FOUND")
                return (i[len(i) -1])
    else:
                print("major error - table not found")

def main(argv):
    initial_time = time.time()
    bn = init()
    if(len(argv) < 3): # {1:}
        print("Please reconsider your command line input for running this program:")
        print("  $> sample <query node> #iterations <observed nodes>")
        print("  Please do not add spaces for <query node> or <observed nodes>")
        return 0 # Failure
    
    # Parse the CLI
    query = argv[1].lower() # Get the query
    iterations = argv[2] # Get number of iterations
    if(len(argv) > 3): # (If any) parse the observations
        observations = argv[3:] # Make sure to make these .lower() after
    else:
        observations = []
    suc, smp, prb, SD, con = rej_sample(query, observations, bn, int(iterations))

    if smp != 0:
      print("After " + iterations + " iterations, there were " + str(smp) + " non-rejected samples, and there were " + str(suc) + " successful samples.")
      print("  P(" + query + "|" + str(observations) + ") = " + str(prb))
      print("  Standard deviation = " + str(SD))
      print("  Confidence Interval = " + str(con))
      print("    delta(Confidence) = " + str(round(con[1] - con[0],5)))
    else:
      print("You have no valid samples, all calculations are 0.")
#     print("\n")
#     print ("query table")
#     stri = query_table("ice_cpt", "high", "mild")
#     print (stri)

#     prob2 = query_table("hum_cpt", "high", None)
#     print (prob2)
    finish_time = time.time()
    total_time = round((finish_time - initial_time), 4)
    print("Total time to run trial: " + str(total_time))

    return 1 # Succses
    

if __name__ == "__main__":
    main(sys.argv)