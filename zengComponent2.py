# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import copy

from collections import deque
from heapq import heappush, heappop

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Node(object):
  def __init__(self, state, empty_coords, parent, actual_cost):
    self.state = state
    self.parent = parent
    self.empty_coords = empty_coords
    self.actual_cost = actual_cost

class Puzzle(object):
  def __init__(self, init_state, goal_state):
    # you may add more attributes if you think is useful
    self.init_state = init_state
    self.goal_state = goal_state
    self.visited = set()

    k = 3 # grid size
    self.valToCoord = {}
    for val in range(1, int(math.pow(k, 2))):
      x = math.floor((val - 1)/k)
      y = (val - 1) % k
      self.valToCoord[val] = (x, y)


  def solve(self):
    heap = []
    startNode = Node(self.init_state, self.getEmptyCoordinates(self.init_state), None, 0)
    heappush(heap, (0, startNode)) # initial cost is 0

    while heap:
      currNode = heappop(heap)
      if (currNode.state == self.goal_state):
        path = []
        while (currNode.parent != None):
          # TODO: populate path by appending to front of list
        return path
      else:
        for newNode in self.getNextNodes(currNode):
          heappush(heap, (self.getEvaluation(node), node))
    # while queue:
    #   currNode = queue.popleft()
    #   if (self.isGoalState(currNode.state, self.goal_state)):
    #     return currNode.path
    #   for newNode in self.getNextNodes(currNode):
    #     queue.append(newNode);
    return ['UNSOLVABLE']

  # Returns f(n) = g(n) + h(n)
  def getEvaluation(self, node):
    return self.actual_cost + self.getManhattanDistSum(node)

  # |x1 – x2| + |y1 – y2|
  def getManhattanDistSum(self, node):
    sum = 0;
    for i in range(len(node.state)):
      for j in range(len(node.state[0])):
        val = node.state[i][j]
        coord = self.valToCoord[val] # supposed coordinates
        sum += (abs(coord[0] - i) + abs(coord[1] - j))
    return sum



  def getEmptyCoordinates(self, state):
    for i in range(len(state)):
      for j in range(len(state[0])):
        if (state[i][j] == 0): return (i,j)

  def getNextNodes(self, currNode):
    validNodes = []
    # enum to keep track of the four directions
    moveDirections = {
      (1, 0): 'UP',
      (-1, 0): 'DOWN',
      (0, -1): 'LEFT',
      (0, 1): 'RIGHT'
    }
    # for each direction, try to swee if can swap
    for move in moveDirections.keys():
      validNode = self.getNextValidNode(currNode, move, moveDirections)
      if (validNode != None): validNodes.append(validNode)
    return validNodes

  # checks if row, col within bounds + not visited
  def getNextValidNode(self, currNode, move, moveDirections):
    state = currNode.state
    emptyCoords = currNode.empty_coords
    newPath = copy.deepcopy(currNode.path)

    rowToSwap = emptyCoords[0] + move[0]
    colToSwap = emptyCoords[1] + move[1]

    # check for bounds
    if (rowToSwap >= len(state) or colToSwap >= len(state[0])): return None
    newState = self.swap(state, emptyCoords, (rowToSwap, colToSwap))
    serializedState = str(newState)

    # check for prior visitation
    if (serializedState in self.visited): return None
    self.visited.add(serializedState)
    newPath.append(moveDirections.get(move))
    print(newPath)
    return Node(newState, (rowToSwap, colToSwap), newPath)

  def swap(self, state, coord1, coord2):
    newState = copy.deepcopy(state)
    temp1 = newState[coord1[0]] 
    temp2 = newState[coord1[1]]
    newState[coord1[0]] = newState[coord2[0]]
    newState[coord1[1]] = newState[coord2[1]]
    newState[coord2[0]] = temp1
    newState[coord2[1]] = temp2
    return newState

  def isGoalState(self, state1, state2):
    for i in range(len(state1)):
      for j in range(len(state1[0])):
        if (state1[i][j] != state2[i][j]):
          return False;
    return True;

# driver methods
if __name__ == "__main__":
    # do NOT modify below

    # argv[0] represents the name of the file that is being executed
    # argv[1] represents name of input file
    # argv[2] represents name of destination output file
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    lines = f.readlines()
    
    # n = num rows in input file
    n = len(lines)
    # max_num = n to the power of 2 - 1
    max_num = n ** 2 - 1

    # Instantiate a 2D list of size n x n
    init_state = [[0 for i in range(n)] for j in range(n)]
    goal_state = [[0 for i in range(n)] for j in range(n)]
    

    i,j = 0, 0
    for line in lines:
        for number in line.split(" "):
            if number == '':
                continue
            value = int(number , base = 10)
            if  0 <= value <= max_num:
                init_state[i][j] = value
                j += 1
                if j == n:
                    i += 1
                    j = 0

    for i in range(1, max_num + 1):
        goal_state[(i-1)//n][(i-1)%n] = i
    goal_state[n - 1][n - 1] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')
