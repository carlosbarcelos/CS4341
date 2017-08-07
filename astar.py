# -*- coding: utf-8 -*-

'''
A* Link: https://codeshare.io/alobxj

a* ref: http://web.mit.edu/eranki/www/tutorials/search/
a* tutorial: http://www.policyalmanac.org/games/aStarTutorial.htm

steps:
1) Begin at the starting point A and add it to an “open list” of squares to be considered. The open list is kind of like a shopping list.
    Right now there is just one item on the list, but we will have more later. It contains squares that might fall along the path you want to take, but maybe not.
    Basically, this is a list of squares that need to be checked out.

2) Look at all the reachable or walkable squares adjacent to the starting point, ignoring squares with walls, water, or other illegal terrain.
    Add them to the open list, too. For each of these squares, save point A as its “parent square”. This parent square stuff is important when we want to trace our path.
    It will be explained more later.

3) Drop the starting square A from your open list, and add it to a “closed list” of squares that you don’t need to look at again for now

4) Drop it from the open list and add it to the closed list.

5) Check all of the adjacent squares. Ignoring those that are on the closed list or unwalkable (terrain with walls, water, or other illegal terrain),
    add squares to the open list if they are not on the open list already. Make the selected square the “parent” of the new squares.

6) If an adjacent square is already on the open list, check to see if this path to that square is a better one. In other words, check to see if the G score for that square is lower
    if we use the current square to get there. If not, don’t do anything. On the other hand, if the G cost of the new path is lower, change the parent of the
    adjacent square to the selected square (in the diagram above, change the direction of the pointer to point at the selected square).
    Finally, recalculate both the F and G scores of that square.

Summary:
1) Add the starting square (or node) to the open list.

2) Repeat the following:

    a) Look for the lowest F cost square on the open list. We refer to this as the current square.

    b) Switch it to the closed list.

    c) For each of the 8 squares adjacent to this current square …

        If it is not walkable or if it is on the closed list, ignore it. Otherwise do the following.

        If it isn’t on the open list, add it to the open list. Make the current square the parent of this square. Record the F, G, and H costs of the square.

        If it is on the open list already, check to see if this path to that square is better, using G cost as the measure. A lower G cost means that this is a better path. If so, change the parent of the square to the current square, and recalculate the G and F scores of the square. If you are keeping your open list sorted by F score, you may need to resort the list to account for the change.

    d) Stop when you:

        Add the target square to the closed list, in which case the path has been found (see note below), or
        Fail to find the target square, and the open list is empty. In this case, there is no path.
3) Save the path. Working backwards from the target square, go from each square to its parent square until you reach the starting square. That is your path.


CS 4341: Assignment 1

Carlos Barcelos
Justin Myerson
Connor Smith
Ryan Walsh

January 28, 2017
'''
import math
#import queue
import sys

NORTH = 'N'
EAST = 'E'
SOUTH = 'S'
WEST = 'W'

RIGHT = "right"
LEFT = "left"

TRUE = 1
FALSE = 0

UNNAV = 1
START = 2
GOAL  = 3



# reference:
# [y][x]

points = 0

# Returns whether or not the next move is a valid move or not
def isValid(field, x, y):
  # Will forward progress lead off of the field
  #print("isvalid check:" + str(x) + " " + str(y))
  if(x < 0 or x > X_SIZE-1):
    return FALSE
  elif(y < 0 or y > Y_SIZE-1):
    return FALSE
  else: # There are no out of bounds errors
    return TRUE

  '''
  try:
    node = field[x][y]
    # Will forward progress lead to unnavigable terrain?
    if(node.flag == UNNAV):
        return FALSE
    else:
        return TRUE
  except (IndexError):
    print("  isValid(): Safely caught IndexError")
    return FALSE
  '''

class agent:
# Agent class represents a robot navigating a field
    def __init__(self, x, y, dir=NORTH, cost=0, a_leap=0,a_forward=0,a_turn=0):
        self.x = x
        self.y = y
        self.dir = dir
        self.cost = cost
        self.a_leap = a_turn
        self.a_forward = a_forward
        self.a_turn = a_turn

    def forward(self, field):
        #Make the move (or try to)
        if self.dir == NORTH :
            if(isValid(field, self.x, self.y - 1)):
                self.cost = self.cost + field.field[self.y - 1][self.x]
                self.y = self.y - 1
            else:
                return
        elif self.dir == EAST :
            if(isValid(field, self.x + 1, self.y)):
                self.cost = self.cost + field.field[self.y][self.x + 1]
                self.x = self.x + 1
            else:
                return
        elif self.dir == SOUTH :
            if(isValid(field, self.x, self.y + 1)):
                self.cost = self.cost + field.field[self.y + 1][self.x]
                self.y = self.y + 1
            else:
                return
        elif self.dir == WEST :
            if(isValid(field, self.x - 1, self.y)):
                self.cost = self.cost + field.field[self.y][self.x - 1]
                self.x = self.x - 1
            else:
                return
        else:
            print ("ERROR: agent.forward()")
            return

        #Report move and increment move counter
        print ("Forward")
        self.a_forward += 1
        return

    def leap(self, field):
        #Make the move (or try to)
        if self.dir == NORTH :
            if(isValid(field, self.x, self.y - 3)):
                self.cost = 20
                self.y = self.y - 3
            else:
               return
        elif self.dir == EAST :
            if(isValid(field, self.x + 3, self.y)):
                self.cost = 20
                self.x = self.x + 3
            else:
               return
        elif self.dir == SOUTH :
            if(isValid(field, self.x, self.y + 3)):
                self.cost = 20
                self.y = self.y + 3
            else:
               return
        elif self.dir == WEST :
            if(isValid(field, self.x - 3, self.y)):
                self.cost = 20
                self.x = self.x - 3
            else:
               return
        else:
            print ("  ERROR: agent.leap()")
            return

        #Report move and increment move counter
        print ("Leap")
        self.a_leap += 1
        return

    def turn(self, direction, field):
        if(direction == RIGHT):
            if(self.dir == NORTH):
                self.dir = EAST
            elif(self.dir == EAST):
                self.dir = SOUTH
            elif(self.dir == SOUTH):
                self.dir = WEST
            else:
                self.dir = NORTH
                print ("Turn right")

        if(direction == LEFT):
            if(self.dir == NORTH):
                self.dir = WEST
            elif(self.dir == EAST):
                self.dir = NORTH
            elif(self.dir == SOUTH):
                self.dir = EAST
            else:
                self.dir = SOUTH
                print ("Turn left")

        #self.cost += field.field[self.x][self.y]
        self.a_turn += 1
        return

class node:
  # Node class represents one tile on the board
  def __init__( self, x, y, cost,  flag, dir=NORTH, parent=None, f=0):
    self.x = x
    self.y = y
    self.cost = cost
    self.dir = dir
    self.flag = flag
    self.parent = parent
    self.f = f

  def __str__(self):
    return "[" + str(self.x) + ", " + str(self.y) + "]"
    '''
  def __cmp__(self, other):
    if self.f < other.f:
      return -1
    elif self.f > other.f:
      return 1
    else: return 0
'''
  def __eq__(self, other):
    return self.f == other.f

  def __lt__(self, other):
    return self.f < other.f

  def __hash__(self):
    return (self.x * 3) + (self.y * 5)

def neighbors(this_node, field):
    neighbors = []
    #print ("valid neighbors:")

    if(isValid(field, this_node.x, this_node.y - 1)):

        #print(str(this_node.x) + " " + str(this_node.y-1))
        neighbors.append(field[this_node.y - 1][this_node.x])

    if(isValid(field, this_node.x + 1, this_node.y)):
        #print(str(this_node.x+1) + " " + str(this_node.y))
        neighbors.append(field[this_node.y][this_node.x + 1])

    if(isValid(field, this_node.x, this_node.y + 1)):
        #print(str(this_node.x) + " " + str(this_node.y + 1))
        neighbors.append(field[this_node.y + 1][this_node.x])

    if(isValid(field, this_node.x - 1, this_node.y)):
        #print(str(this_node.x - 1) + " " + str(this_node.y))
        neighbors.append(field[this_node.y][this_node.x - 1])

    #print("xxxxxxxxxxxxx")

    return neighbors

def neighbors_leap(this_node, field):
    neighbors_leap = []

    #print ("valid leap neighbors:")

    if(isValid(field, this_node.x, this_node.y - 3)):
        #print(str(this_node.x) + " " + str(this_node.y-3))
        neighbors_leap.append(field[this_node.y - 3][this_node.x])
    if(isValid(field, this_node.x + 3, this_node.y)):
        #print(str(this_node.x+3) + " " + str(this_node.y))
        neighbors_leap.append(field[this_node.y][this_node.x + 3])
    if(isValid(field, this_node.x, this_node.y + 3)):
        #print(str(this_node.x) + " " + str(this_node.y + 3))
        neighbors_leap.append(field[this_node.y + 3][this_node.x])
    if(isValid(field, this_node.x - 3, this_node.y)):
        #print(str(this_node.x - 3) + " " + str(this_node.y))
        neighbors_leap.append(field[this_node.y][this_node.x - 3])


    #print("xxxxxxxxxxxxx")

    return neighbors_leap


# Read a file using tab-delimited file
def read_file(inputfile):
    f = open (inputfile , 'r')
    #read the string input
    l = []
    l = [line.split('\t') for line in f]
    f.close()

    global Y_SIZE
    Y_SIZE = len(l)
    global X_SIZE
    X_SIZE = len(l[0])

#this_node.row
#this_node.col
#this_node.cost
    matrix = []
    #convert to integers and return
    for col in range(0, len(l)):
        mtrix = []

        for row in range(0, len(l[col])):
            my_node = node(0,0,0,0)

            if l[col][row].strip() is "#":
                my_node.x = row
                my_node.y = col
                my_node.cost = -1
                my_node.flag = UNNAV
            elif l[col][row].strip() is "S":
                my_node.x = row
                my_node.y = col
                my_node.cost = 1
                my_node.flag = START
                global START_NODE
                START_NODE = my_node
            elif l[col][row].strip() is "G":
                my_node.x = row
                my_node.y = col
                my_node.cost = 1
                my_node.flag = GOAL
                global GOAL_NODE
                GOAL_NODE = my_node
            else:
                my_node.x = row
                my_node.y = col
                my_node.cost = int(l[col][row])
                my_node.flag = 0
            mtrix.append(my_node)
        matrix.append(mtrix)
    return matrix

# Calculate the movement cost of moving from current_node to next_node
def movement(current_node, next_node):
  cost = 0
  # Turn cost
  if(current_node.dir == NORTH):
    if(next_node.y == current_node.y - 1):
      # North to North | No turn action required
      next_node.dir = NORTH
    elif(next_node.y == current_node.y + 1):
      # North to South | Turn twice
      cost += 2 * math.ceil(current_node.cost / 3)
      next_node.dir = SOUTH
    elif(next_node.x == current_node.x - 1):
      # North to West  | Turn left once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = WEST
    elif(next_node.x == current_node.x + 1):
      # North to East  | Turn right once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = EAST
  elif(current_node.dir == SOUTH):
    if(next_node.y == current_node.y - 1):
      # South to North | Turn twice
      cost += 2 * math.ceil(current_node.cost / 3)
      next_node.dir = NORTH
    elif(next_node.y == current_node.y + 1):
      # South to South | No turn action required
      next_node.dir = SOUTH
    elif(next_node.x == current_node.x - 1):
      # South to West  | Turn right once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = WEST
    elif(next_node.x == current_node.x + 1):
      # South to East  | Turn left once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = EAST
  elif(current_node.dir == WEST):
    if(next_node.y == current_node.y - 1):
      # West to North | Turn right once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = NORTH
    elif(next_node.y == current_node.y + 1):
      # West to South | Turn left once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = SOUTH
    elif(next_node.x == current_node.x - 1):
      # West to West  | No turn action required
      next_node.dir = WEST
    elif(next_node.x == current_node.x + 1):
      # West to East  | Turn twice
      cost += 2 * math.ceil(current_node.cost / 3)
      next_node.dir = EAST
  elif(current_node.dir == EAST):
    if(next_node.y == current_node.y - 1):
      # East to North | Turn left once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = NORTH
    elif(next_node.y == current_node.y + 1):
      # East to South | Turn right once
      cost += math.ceil(current_node.cost / 3)
      next_node.dir = SOUTH
    elif(next_node.x == current_node.x - 1):
      # East to West  | Turn twice
      cost += 2 * math.ceil(current_node.cost / 3)
      next_node.dir = WEST
    elif(next_node.x == current_node.x + 1):
      # East to East  | No turn action required
      next_node.dir = EAST

  # Calculate distance
  x = abs(current_node.x - next_node.x)
  y = abs(current_node.y - next_node.y)
  d = max(x,y)
  # isForward
  if(d == 1):
    cost += next_node.cost

  # isLeap
  elif(d == 3):
    cost += 20

  else:
    print("  ERROR: agent.movement() d = " + str(d))
    return

  #print("cost:")
  #print(cost)
  return cost


# node_cost is the cost to reach the next node from this node
def node_cost(field, x_next, y_next):
    return field[y_next][x_next]

''' Heuristic Functions: the cost to get from the next node to the goal '''
# Heuristic of 0: Baseline of how uninformed search would perform
def heuristic1():
    return 0

# Min(vertical,horizontal)
def heuristic2(x_goal, y_goal, x_next, y_next):
    x = abs(x_goal - x_next)
    y = abs(y_goal - y_next)
    return min(x,y)

# Max(vertical,horizontal)
def heuristic3(x_goal, y_goal, x_next, y_next):
    x = abs(x_goal - x_next)
    y = abs(y_goal - y_next)
    return max(x,y)

# Manhattan Distance: vertical + horizontal distance
def heuristic4(x_goal, y_goal, x_next, y_next):
    x = abs(x_goal - x_next)
    y = abs(y_goal - y_next)
    return x + y

# Admissable heuristic
def heuristic5(x_goal, y_goal, x_next, y_next):
    x = abs(x_goal - x_next)
    y = abs(y_goal - y_next)
    return math.ceil(math.sqrt(x**2 + y**2))

# Non-admissable heuristic
def heuristic6(x_goal, y_goal, x_next, y_next):
    return 3 * heuristic5(x_goal, y_goal, x_next, y_next)

#returns appropriate h(n) heuristic value.
def heuristic_selection(version, this_node):
    #print("heuristic debug:")
    #print(version)
    #print(this_node)
    #print("----------")

    goal_node = GOAL_NODE


    if version == 1:
        return heuristic1()
    elif version == 2:
        return heuristic2(goal_node.x, goal_node.y, this_node.x, this_node.y)
    elif version == 3:
        return heuristic3(goal_node.x, goal_node.y, this_node.x, this_node.y)
    elif version == 4:
        return heuristic4(goal_node.x, goal_node.y, this_node.x, this_node.y)
    elif version == 5:
        return heuristic5(goal_node.x, goal_node.y, this_node.x, this_node.y)
    elif version == 6:
        return heuristic6(goal_node.x, goal_node.y, this_node.x, this_node.y)
    else:
        print("  ERROR: heuristic_selection()")
        return -1

#A* Search, modified to take agent as input
'''

def a_star(agent, field, start_node, goal_node, heuristic):
  open_nodes = queue.PriorityQueue()
  closed_nodes = []
  prev_node = {}
  total_cost = 0

  open_nodes.put(start_node, 0)
  print("start_node: " + str(start_node.x) + ", " + str(start_node.y))

  while not open_nodes.empty():
    print("++++++++++++++++++++++++++++++++++++++++++++")
    print("iteration...")


    current_node = open_nodes.get()

    if (current_node.x == GOAL_NODE.x and current_node.y == GOAL_NODE.y):
      print("GOAL found")
      break

    neighbor_leap_nodes = neighbors_leap(current_node, field)
    direct_neighbors = neighbors(current_node, field)

    possible_nodes = neighbors(current_node, field) + neighbors_leap(current_node, field)

    for next_node in possible_nodes:
        print("next possible node...")

        print("current_node info: " + str(current_node.x) + ", " + str(current_node.y))
        print("next_node info: " + str(next_node.x) + ", " + str(next_node.y))

        next_node.parent = current_node
        movement_val = movement(current_node, next_node)

        print("movement_val: " + str(movement_val))

        current_node.cost += movement_val
        g = current_node.cost # Current node cost to get where you are
        h = heuristic_selection(int(heuristic), next_node) # Heuristic cost to get to node

        print("h = " + str(h))
        print("g = "+ str(g))

        f = g + h
        if next_node in possible_nodes:
            print("first if")
            if f <= next_node.cost:
                continue
        elif next_node in closed_nodes:
            print("second if")
            if f <= next_node.cost:
                continue
        else:
            print("else yo")
            open_nodes.put(next_node)
        print("___________________________")
    closed_nodes.append(current_node)
  return
  '''
'''
def a_star(agent, field, start_node, goal_node, heuristic):
  open_nodes = []
  closed_nodes = []
  prev_node = {}
  total_cost = 0

  open_nodes.append(start_node)
  print("start_node: " + str(start_node.x) + ", " + str(start_node.y))

  while open_nodes:
    #print("++++++++++++++++++++++++++++++++++++++++++++")
    #print("iteration...")


    current_node = open_nodes[0]
    open_nodes.remove(open_nodes[0])

    if (current_node.x == GOAL_NODE.x and current_node.y == GOAL_NODE.y):
      print("GOAL found")
      print("" + str(current_node.cost))
      createPath(current_node)
      break

    neighbor_leap_nodes = neighbors_leap(current_node, field)
    direct_neighbors = neighbors(current_node, field)

    possible_nodes = neighbors(current_node, field) + neighbors_leap(current_node, field)

    for next_node in possible_nodes:
        #print("next possible node...")

        #print("current_node info: " + str(current_node.x) + ", " + str(current_node.y))
        #print("next_node info: " + str(next_node.x) + ", " + str(next_node.y))

        next_node.parent = current_node
        movement_val = movement(current_node, next_node)

        #print("movement_val: " + str(movement_val))
    if(current_node.parent is None):
          current_node.cost = movement_val
        else:
          current_node.cost = movement_val + current_node.parent.cost
        g = current_node.cost # Current node cost to get where you are
        h = heuristic_selection(int(heuristic), next_node) # Heuristic cost to get to node

        #print("h = " + str(h))
        print("g = "+ str(g))

        f = g + h
        if next_node in open_nodes:
            print("first if")
            if f <= next_node.cost:
                continue
        elif next_node in closed_nodes:
            print("second if")
            if f <= next_node.cost:
                continue
        else:
            print("else yo")
            open_nodes.append(next_node)
            print("node info: " + str(next_node.x) + ", " + str(next_node.y))
        print("___________________________")

    closed_nodes.append(current_node)
  return

'''

def createPath(goal_node):
  node = goal_node
  while node.parent is not None:
    print("" + str(node.x) + "," + str(node.y))
    node = node.parent
  return

'''
def a_star(agent, field, start_node, goal_node, heuristic):
  open_nodes = queue.PriorityQueue()
  closed_nodes = []
  prev_node = {}
  total_cost = 0

  open_nodes.put(start_node, 0)
  print("start_node: " + str(start_node.x) + ", " + str(start_node.y))

  while not open_nodes.empty():
    #print("++++++++++++++++++++++++++++++++++++++++++++")
    #print("iteration...")


    #current_node_tup = open_nodes.get()
    #current_node = current_node_tup[1]
    current_node = open_nodes.get()

    if (current_node.x == GOAL_NODE.x and current_node.y == GOAL_NODE.y):
      print("GOAL found")
      print("" + str(current_node.cost))
      #createPath(current_node)
      break

    neighbor_leap_nodes = neighbors_leap(current_node, field)
    direct_neighbors = neighbors(current_node, field)

    possible_nodes = neighbors(current_node, field) + neighbors_leap(current_node, field)

    for next_node in possible_nodes:
        #print("next possible node...")

        #print("current_node info: " + str(current_node.x) + ", " + str(current_node.y))
        #print("next_node info: " + str(next_node.x) + ", " + str(next_node.y))

        next_node.parent = current_node
        movement_val = movement(current_node, next_node)

        #print("movement_val: " + str(movement_val))
        if(current_node.parent is None):
          current_node.cost = movement_val
        else:
          current_node.cost = movement_val + current_node.parent.cost
        g = current_node.cost # Current node cost to get where you are
        h = heuristic_selection(int(heuristic), next_node) # Heuristic cost to get to node

        #print("h = " + str(h))
        print("g = "+ str(g))

        f = g + h
        if next_node in open_nodes:
            print("first if")
            if f <= next_node.cost:
                continue
        elif next_node in closed_nodes:
            print("second if")
            if f <= next_node.cost:
                continue
        else:
            print("else yo")
            open_nodes.append(next_node)
            print("node info: " + str(next_node.x) + ", " + str(next_node.y))
        print("___________________________")

    closed_nodes.append(current_node)
  return
'''
def a_star(agent, field, start_node, goal_node, heuristic):
    open_nodes = queue.PriorityQueue()
    start_node.f = 0
    open_nodes.put(start_node)
    closed_nodes = {}
    cost_so_far = {}
    closed_nodes[start_node] = None
    cost_so_far[start_node] = 0

    while not open_nodes.empty():
        current_node = open_nodes.get()

        if current_node.flag == GOAL:
            print("GOAL FOUND")
            createPath(current_node)
            break

        possible_nodes = neighbors(current_node, field) + neighbors_leap(current_node, field)
        for next in possible_nodes:
            print("ITERATION")
            new_cost = cost_so_far[current_node] + field[next.y][next.x].cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                f = new_cost + heuristic_selection(int(heuristic), next)
                next.f = f
                open_nodes.put(next)
                closed_nodes[next] = current_node

    return closed_nodes, cost_so_far, open_nodes


def createPath(goal_node):
  node = goal_node
  while node.parent is not None:
    print("" + str(node.x) + "," + str(node.y))
    node = node.parent
  return


''' Main function. Execution from command line. '''
def main(argv):
    if(len(argv) != 3): # {1:}
      print("Please reconsider your command line input for running this program:")
      print("  $> astar.py <input_field.txt> <heuristic_number(1-6)>")
      return 0
    #Code goes here to run the program
    my_field = read_file(argv[1])
    agent_1 = agent(START_NODE.x, START_NODE.y)
    a_star_return = a_star(agent_1, my_field, START_NODE, GOAL_NODE, argv[2])
    # Have astar return an array of (score, number_actions, number_nodes, branching_factor, series_of_actions)
    print("Closed Nodes:\n" + str(a_star_return[0]))
    print("Final Cost:\n" + str(a_star_return[1]))
    print(str(len(a_star_return[1])))



if __name__ == "__main__":
    main(sys.argv)
