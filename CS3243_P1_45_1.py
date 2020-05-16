# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from collections import deque
import copy
import operator

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Puzzle(object):
    class Node(object):
        def __init__(self, curr_state, parent, action):
                self.state = curr_state
                self.parent = parent
                self.action = action

    def __init__(self, init_state, goal_state):
        # you may add more attributes if you think is useful
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        for i, v in enumerate(self.init_state):
            for j, k in enumerate(v):
                if k == 0:
                    self.start_pos = (i, j)
                    break
    
    
    # def swap(self, curr_state, pos, direction, visited):
    #     if direction == 'UP':
    #         temp = curr_state[pos[0]][pos[1]]
    #         curr_state[pos[0]][pos[1]] = curr_state[pos[0]][pos[1] - 1]
    #         curr_state[pos[0]][pos[1] - 1] = temp
    #     elif direction == 'DOWN':
    #     elif direction == 'LEFT':
    #     elif direction == 'RIGHT':

    # def isNextStateVisited(self, curr_state, pos, action, visited):
    
    def move(self, curr_state, pos, visited, direction):
        if pos[0] + direction[0] >= len(curr_state) or pos[0] + direction[0] < 0 or pos[1] + direction[1] >= len(curr_state[0]) or pos[1] + direction[1] < 0:
            return None, pos
        next_state = copy.deepcopy(curr_state)
        temp = next_state[pos[0]][pos[1]]
        next_state[pos[0]][pos[1]] = next_state[pos[0]+direction[0]][pos[1] + direction[1]]
        next_state[pos[0]+direction[0]][pos[1]+direction[1]] = temp
        if str(next_state) in visited: # can optimise by not deepcopying when next state is already visited
            return None, pos
        visited.add(str(next_state))
        return next_state, (pos[0]+direction[0], pos[1]+direction[1])
        

    def solve(self):
        moves = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        directions = [(0,1), (1, 0), (-1, 0), (0, -1)]
        visited = set()
        q = deque()
        
        def isVisited(curr_state):
            return str(curr_state) in visited

        visited.add(str(self.init_state))
        q.append((self.init_state, self.start_pos))

        while q:
            curr_state, pos = q.popleft()
    #         with open('log.txt', 'a') as f:
    #             f.write('curr state: \n' )
    #             f.write('\n'.join([''.join(['{:4}'.format(item) for item in row]) 
    #   for row in curr_state]))
    #             f.write('\n---------\n')
            if curr_state == self.goal_state:
                return True
            
            for direction in directions:
                next_state, next_pos = self.move(curr_state, pos, visited, direction)
                if next_state and next_pos:
                    q.append((next_state, next_pos))
        
        return False
            
                # think of how to represent the state transition

    # you may add more functions if you think is useful

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
        # for answer in ans:
            f.write(str(ans))







