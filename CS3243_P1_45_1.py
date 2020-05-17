# CS3243 Introduction to Artificial Intelligence
# Project 1: k-Puzzle

import os
import sys
from collections import deque
import copy

# Running script on your own - given code can be run with the command:
# python file.py, ./path/to/init_state.txt ./output/output.txt

class Node(object):
    def __init__(self, curr_state, parent, action, pos):
        self.state = curr_state
        self.parent = parent
        self.action = action
        self.pos = pos
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
        visited.add(str(next_state))
        return next_state, (pos[0]+direction[0], pos[1]+direction[1])


    def solve(self):
        move_directions = {
            (0,1): 'LEFT',
            (1,0): 'UP',
            (-1, 0): 'DOWN',
            (0, -1): 'RIGHT'
        }
        isFound = False
        visited = set()
        q = deque()

        visited.add(str(self.init_state))
        q.append(self.start_node)

        while q:
            curr_node = q.popleft()
            curr_state, pos = curr_node.state, curr_node.pos
            if curr_state == self.goal_state:
                isFound = True
                break
            
            for direction in move_directions.keys():
                next_state, next_pos = self.move(curr_state, pos, visited, direction)
                if next_state and next_pos:
                    q.append(Node(next_state, curr_node, move_directions[direction], next_pos))
        
        if isFound:
            while curr_node:
                if curr_node.action:
                    self.actions.appendleft(curr_node.action)
                curr_node = curr_node.parent
        else:
            return ['UNSOLVABLE']
        
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
            f.write(answer+'\n')