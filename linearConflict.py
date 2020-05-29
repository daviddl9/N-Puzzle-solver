# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from collections import deque
import copy
import heapq

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt
class Node(object):
    def __init__(self, curr_state, parent, action, pos):
        self.state = curr_state
        self.parent = parent
        self.action = action
        self.pos = pos
        self.path_cost = parent.path_cost + 1 if parent != None else 0
        self.manhattanDistance = self.getManhattanDistance(curr_state) if parent is None else self.computeManhattanDistanceDifference()
        self.linearConflict = self.getLinearConflict(curr_state)

    def computeManhattanDistanceDifference(self):
        cell = self.getCorrectCellFor(self.parent.state[self.pos[0]][self.pos[1]], len(self.state))
        dist = abs(cell[0] - self.pos[0]) + abs(cell[1] - self.pos[1])
        curr_cell = self.getCorrectCellFor(self.state[self.parent.pos[0]][self.parent.pos[1]], len(self.state))
        toAdd = abs(curr_cell[0] - self.parent.pos[0]) + abs(curr_cell[1] - self.parent.pos[1])
        return self.parent.manhattanDistance - dist + toAdd

    def __lt__(self, other):
      # it's straightforward to see why this heuristic dominates manhattan distance, because for all n where n represents a state, 
      # manhattanDistance(n) <= manhattanDistance(n) + linearConflict(n), where linearConflict(n) is an integer >= 0.  
      return self.path_cost + self.manhattanDistance + self.linearConflict < other.path_cost + other.manhattanDistance + other.linearConflict
    
    def getManhattanDistance(self, curr_state):
      distance = 0
      for i in range(len(self.state)):
          for j in range(len(self.state[0])):
              if self.state[i][j] != 0:
                  x, y = divmod(self.state[i][j]-1, len(self.state[0]))
                  distance += abs(x - i) + abs(y - j)
      return distance

    def getCorrectCellFor(self, number, dimension):
        return (number - 1) / dimension, dimension - 1 if number % dimension == 0 else (number % dimension) - 1
    
    def getLinearConflict(self, x):
        linConflict = 0
        for i in range(len(x)):
            for j in range(len(x[0])):
                if x[i][j] == 0: continue
                number = x[i][j]
                cell = self.getCorrectCellFor(number, len(x))
                if (i, j) == cell: continue  # if Correct Cell
                if i == cell[0]:  # if correct row
                    for fromCol in range(j+1,len(x)):
                        if number > x[i][fromCol] and self.getCorrectCellFor(x[i][fromCol], len(x))[0] == i:
                            linConflict += 1
                elif j == cell[1]:  # if correct column
                    for fromRow in range(i+1,len(x)):
                        if number > x[fromRow][j] and self.getCorrectCellFor(x[fromRow][j], len(x))[1] == j:
                            linConflict += 1

        return 2 * linConflict

class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = deque()
        for i, v in enumerate(self.init_state):
            for j, k in enumerate(v):
                if k == 0:
                    self.start_pos = (i, j)
                    break
        self.start_node = Node(self.init_state, None, None, self.start_pos)

    def swap(self, curr_state, pos, direction):
        temp = curr_state[pos[0]][pos[1]]
        curr_state[pos[0]][pos[1]] = curr_state[pos[0]+direction[0]][pos[1] + direction[1]]
        curr_state[pos[0]+direction[0]][pos[1]+direction[1]] = temp
        return curr_state
    
    def move(self, curr_state, pos, visited, direction):
        if pos[0] + direction[0] >= len(curr_state) or pos[0] + direction[0] < 0 or pos[1] + direction[1] >= len(curr_state[0]) or pos[1] + direction[1] < 0:
            return None, pos
        if str(self.swap(curr_state, pos, direction)) in visited:
            curr_state = self.swap(curr_state, pos, direction)
            return None, pos
        
        next_state = copy.deepcopy(curr_state)
        curr_state = self.swap(curr_state, pos, direction)
        return next_state, (pos[0]+direction[0], pos[1]+direction[1])

    def isSolvable(self):
        flattened_list = [i for sublist in self.init_state for i in sublist]
        inv_count = 0
        for i in range(len(flattened_list) - 1):
            for j in range(i+1, len(flattened_list)):
                if flattened_list[i] and flattened_list[j] and flattened_list[i] > flattened_list[j]:
                    inv_count += 1
        
        if len(self.init_state[0]) % 2:
            return inv_count % 2 == 0
        else:
            x = len(self.init_state) - self.start_pos[0]
            return inv_count % 2 == 0 if x % 2 else inv_count % 2

    def solve(self):
        if not self.isSolvable():
            return ['UNSOLVABLE']
        move_directions = {
            (0,1): 'LEFT',
            (1,0): 'UP',
            (-1, 0): 'DOWN',
            (0, -1): 'RIGHT'
        }
        visited = set()
        pq = []
        heapq.heappush(pq, self.start_node)

        while pq:
            curr_node = heapq.heappop(pq)
            if curr_node.state == self.goal_state:
              break
            if str(curr_node.state) in visited:
              continue
            visited.add(str(curr_node.state))
           
            for direction in move_directions.keys():
                next_state, next_pos = self.move(curr_node.state, curr_node.pos, visited, direction)
                if next_state:
                  heapq.heappush(pq, Node(next_state, curr_node, move_directions[direction], next_pos))

        while curr_node:
            if curr_node.action:
                self.actions.appendleft(curr_node.action)
            curr_node = curr_node.parent
        
        return self.actions

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
            f.write(answer + '\n')
