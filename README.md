# N-Puzzle solver
This repository explores the [N-Puzzle](https://en.wikipedia.org/wiki/15_puzzle) solver using the following algorithms (in order of increasing performance): 

1. Breadth-First Search (`BFS.py`)
2. A* Search using Manhattan Distance (`manhattanDistance.py`)
3. A* Search using Manhattan Distance & Linear conflict (`linearConflict.py`)

## Running the code
`python <filename> <inputfile> <outputfile>`

## Input format
The input file should be a 2D array representing the puzzle. Look at the test input for an example.

## Output format
The scripts writes the series of steps to solve the N-puzzle into the output file. If no solution exists, it writes 'UNSOLVABLE'. 


### Other minor performance optimisations

#### Solvability Check
We can compute whether the grid is solvable in one step, by checking the position of the blank tile and the number of inversions in the grid. This improves performance significantly, as it would not have to generate all possible nodes before declaring that the puzzle is not solvable. Read more [here.](https://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/)

#### Computing Manhattan Distance
Instead of computing Manhattan Distance for each grid, we could update the manhattan distance using the parent's manhattan distance, compute the change caused by a particular move. 

#### State generation
Another minor optimisation done was to prevent generation of a new grid each time. By doing a simple swap to check if a particular state has been visited before, we saved on a couple of `deepcopy` operations, which were quite expensive.
