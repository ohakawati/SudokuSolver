# SudokuSolver

# Sudoku Solver leverages 3 algortihm techniques in order to provide a valid solution to any given incomplete sudoku puzzle.

-Algorithm 1 is the Brute Force method where each empty cell of the puzzle is examined and the numbers 1-9 are checked in that cell. Following that would be the next empty cell placing valid numbers and this goes on until the puzzle is filled in and verified. If there is a constraint violated the algorithm backtracks to the previous cell to attempt another digit until a valid puzzle is found.

-Algorithm 2 is the CSP Backtracking method where each empty cell is filled with a valid digit and checked, if there are any violations at a cell the algorithm backtracks to the previous cell to eliminate any contradiction.

-Algorithm 3 is the CSP Forward Checking method that includes a minimum remaining value heuristic. The algorithm starts by examining each empty cell in the Sudoku grid and uses the MRV heuristic to select the cell with the fewest possible values in its domain. That cell is assigned a value and forward checking is used to update the domains of other cells in the same row, column, and 3x3 box. If the forward checking results in any empty domain, the algorithm backtracks to the previous cell and tries the next possible value until a valid solution is found. The process continues until either a solution is found or all possibilities have been exhausted.

-Nodes Generated and Time to Complete are measured within each algorithm

# Given an Incomplete Sudoku
![unkownpuzz](https://user-images.githubusercontent.com/89810188/236750271-a22724d1-e119-4f6a-b5e2-11588d677158.PNG)


# Using the CSP FC Algorithm(3) and input puzzle(testcase4.csv) we are given a solution
![cpmpleyt](https://user-images.githubusercontent.com/89810188/236750792-7554120f-7ef5-4030-8cff-a57475ddaf39.PNG)


# Testcase4.csv Solution Key
![Solvedsol](https://user-images.githubusercontent.com/89810188/236750854-3080f33d-fed1-4552-a0e9-58d3f4e18f77.PNG)



