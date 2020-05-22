# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
import copy
import math

from collections import deque
from heapq import heappush, heappop

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Node(object):
  def __init__(self, state, empty_coords, parent, actual_cost, directionFromParent):
    self.state = state
    self.parent = parent
    self.empty_coords = empty_coords
    self.actual_cost = actual_cost
    self.directionFromParent = directionFromParent

class Puzzle(object):
  def __init__(self, init_state, goal_state):
    # you may add more attributes if you think is useful
    self.init_state = init_state
    self.goal_state = goal_state
    self.visited = set()

    k = 3 # grid size
    self.valToCoord = {}
    # dynamically generate the correct coordinates for each value in a k * k grid
    for val in range(1, int(math.pow(k, 2))):
      x = int(math.floor((val - 1)/k))
      y = (val - 1) % k
      self.valToCoord[val] = (x, y)


  def solve(self):
    heap = []
    startNode = Node(self.init_state, self.getEmptyCoordinates(self.init_state), None, 0, '')
    heappush(heap, (0, startNode))

    while heap:
      currNode = heappop(heap)[1]
      if (currNode.state == self.goal_state):
        path = []
        pointer = currNode
        while (pointer.parent != None):
          if (pointer.directionFromParent != ''): path.insert(0, pointer.directionFromParent)
          pointer = pointer.parent
        print(path)
        return path
      else:
        for newNode in self.getNextNodes(currNode):
          heappush(heap, (self.getEvaluation(newNode), newNode))
    return ['UNSOLVABLE']

  # Returns f(n) = g(n) + h(n)
  def getEvaluation(self, node):
    return node.actual_cost + self.getManhattanDistSum(node)

  def getManhattanDistSum(self, node):
    sum = 0;
    for i in range(len(node.state)):
      for j in range(len(node.state[0])):
        val = node.state[i][j]
        if (val == 0): continue
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
    # node properties
    state = currNode.state
    costToParent = currNode.actual_cost
    emptyCoords = currNode.empty_coords

    rowToSwap = emptyCoords[0] + move[0]
    colToSwap = emptyCoords[1] + move[1]

    # check for bounds
    if (rowToSwap >= len(state) or colToSwap >= len(state[0])): return None
    newState = self.swap(state, emptyCoords, (rowToSwap, colToSwap)) #TODO: minor optimization, don't serialize if path exists
    serializedState = str(newState)

    # check for prior visitation
    if (serializedState in self.visited): return None
    self.visited.add(serializedState)
    return Node(newState, (rowToSwap, colToSwap), currNode, costToParent + 1, moveDirections[move])

  def swap(self, state, coord1, coord2):
    newState = copy.deepcopy(state)
    temp1 = newState[coord1[0]] 
    temp2 = newState[coord1[1]]
    newState[coord1[0]] = newState[coord2[0]]
    newState[coord1[1]] = newState[coord2[1]]
    newState[coord2[0]] = temp1
    newState[coord2[1]] = temp2
    return newState

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
