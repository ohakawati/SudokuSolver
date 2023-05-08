import csv
import sys
from timeit import default_timer

#Defining a global counter to track nodes generated with the 3 algorithms
global counter
counter = 0

#Readcsv funtion reads the input sudoku puzzle and replaces the X's with 0's to be understood by the algorithms
def readCSV(file):
    with open(file) as f:
        reader = csv.reader(f)
        puzzle = [[0 if cell == 'X' else int(cell) for cell in row] for row in reader]
    return puzzle

#Valid function is used to check if a digit 1-9 is valid in a certain position on the board
def checkValid(puzzle, row, column, digit):
    #Checks the column of the puzzle
    for i in range(9):
        if puzzle[i][column] == digit:
            return False
    #Checks the row of the puzzle
    for i in range(9):
        if puzzle[row][i] == digit:
            return False
    #Checks the 3x3 box of the puzzle
    rowColumn = (column // 3) * 3
    rowBox = (row // 3) * 3
    for i in range(rowBox, rowBox + 3):
        for j in range(rowColumn, rowColumn + 3):
            if puzzle[i][j] == digit:
                return False
    return True

#Empty acts as a utility function that searches for the next empty cell that is represented by 0
def checkEmpty(puzzle):
    for i in range(9):
        for j in range(9):
            if puzzle[i][j] == 0:
                return (i, j)
    return None

#Forward checking function that checks if a digit violates a constraint and returns false if so
def checkForward(puzzle, row, column, digits):
    for digit in digits:
        if not checkValid(puzzle, row, column, digit):
            return False
    return True

#Brute Force Search algorithm uses exhaustion to solve sudoku, that is trying every possible digit until the puzzle is solve
def bruteForceSearch(puzzle):
    #Using recursion to solve sudoku
    def brute(puzzle, i, j):
        #Checks if puzzle is filled, if so it is already solved so the puzzle is returned
        if i == 9:
            return puzzle
        #Searching for next empty cell
        while puzzle[i][j] != 0:
            j += 1
            if j == 9:
                i += 1
                j = 0
            if i == 9:
                return puzzle
        #In the current empty cell, all digits are tried
        for digit in range(1, 10):
            #Using the checkValid method to ensure digit is valid in position
            if checkValid(puzzle, i, j, digit):
                #The checked digit is then assigned to its position 
                puzzle[i][j] = digit
                #Counter is incremented as nodes are generated
                global counter
                counter +=1
                #Use brute to solve remaining sudoku
                sudokuSolved = brute(puzzle, i, j)
                if sudokuSolved:
                    return sudokuSolved
                #If not solution is found, backtrack
                puzzle[i][j] = 0
        return False
    
    #Returns solved puzzle using brute 
    return brute(puzzle, 0, 0)


#BackTrackCSP algorithm relies on constraints between nodes and backtracking to solve sudoku 
def backTrackCSP(puzzle):
    #Using recursion to solve sudoku
    def backTrack(puzzle):
        #emptyCell is set to the next empty cell using the checkEmpty function
        emptyCell = checkEmpty(puzzle)
        #Exception to an already solved sudoku being the input, if not the empty cell is assigned to its position
        if not emptyCell:
            return puzzle
        else:
            row, column = emptyCell
        #Begins to test numbers 1-9
        for digit in range(1, 10):
            #Check if the digit is valid in the empty cell position
            if checkValid(puzzle, row, column, digit):
                #Assigns digit to the empty cell
                puzzle[row][column] = digit
                global counter
                counter +=1
                #Using recursion to solve remaining empty cells
                sudokuSolved = backTrack(puzzle)
                if sudokuSolved:
                    return sudokuSolved
                #If there are no solutions found backtrack
                puzzle[row][column] = 0
        return False

    #Returns solved sudoku using backTrack
    return backTrack(puzzle)


#forwardCheckCSP algorithm solves the sudoku by using MRV heuristic to choose and place numbers within a cell and forward check the sudoku
def forwardCheckCSP(puzzle):
    global counter
    #Using recursion to solve puzzle
    def forwardCheck(puzzle):
        global counter
        #Initializing first empty cell
        emptyCell = checkEmpty(puzzle)
        if not emptyCell:
            return puzzle
        row, column = emptyCell
        #Creating a set of possible digits 1-9 that could be placed in the empty cell
        possibilities = set(range(1, 10))
        #For loop discards digits that are used in the same row or column
        for x in range(9):
            possibilities.discard(puzzle[row][x])
            possibilities.discard(puzzle[x][column])
        #Discards digits used within the same 3x3 box
        boxRow = (row // 3) * 3
        boxColumm = (column // 3) * 3
        for i in range(boxRow, boxRow + 3):
            for j in range(boxColumm, boxColumm + 3):
                possibilities.discard(puzzle[i][j])
        #Displaying MRV heuristic, remaining digits are sorted and checked when assigning positions, sudoku is iterated through
        for digit in sorted(possibilities):
            #Checks validity if digit in position
            if checkValid(puzzle, row, column, digit):
                #Assigns digit to empty cell
                puzzle[row][column] = digit
                #Initializing tracked list to keep track of modifications to the sudoku
                tracked = []
                #Checks if a current cell is empty and valid in its position, if so it is appended to tracked 
                for x in range(9):
                    if puzzle[row][x] == 0:
                        #Check is on same row as digit
                        if checkForward(puzzle, row, x, set([digit])):
                            tracked.append((row, x))
                            if not puzzle[row][x]:
                                break
                    
                    if puzzle[x][column] == 0:
                        #Check is on same column as digit
                        if checkForward(puzzle, x, column, set([digit])):
                            tracked.append((x, column))
                            if not puzzle[x][column]:
                                break
                if not puzzle[row][column]:
                    for i in range(boxRow, boxRow + 3):
                        for j in range(boxColumm, boxColumm + 3):
                            if puzzle[i][j] == 0:
                                #Check is done on the same box as the digit
                                if checkForward(puzzle, i, j, set([digit])):
                                    tracked.append((i, j))
                                    if not puzzle[i][j]:
                                        break
                counter +=1
                if forwardCheck(puzzle):
                    return puzzle
                #Backtrack if no solution is found using forwardCheck
                for i, j in tracked:
                    puzzle[i][j] = 0
                puzzle[row][column] = 0
        return False

    #Returns solved sudoku using forwardCheck and increments counter to track nodes generated
    counter +=1
    return forwardCheck(puzzle)


#Print input function is used to print the inputted sudoku puzzle
def PrintInput(puzzle):
    for i in range(9):
        row = ''
        for j in range(9):
            if puzzle[i][j]:
                row += str(puzzle[i][j])
            else:
                row += 'X'
            if j < 8:
                row += ','
        print(row)

#Print output function is used to print the solved sudoku puzzle
def PrintOutput(puzzle):
    for i in range(len(puzzle)):
        row = ''
        for j in range(len(puzzle[i])):
            if puzzle[i][j] == 0:
                row += '_,'
            elif isinstance(puzzle[i][j], bool):
                row += str(int(puzzle[i][j])) + ','
            else:
                row += str(puzzle[i][j]) + ','
        row = row[:-1]
        print(row)

#Method checks if the inputted sudoku puzzle is valid
def checkValidSudoku(sudoku):
    if len(sudoku) != 9 or any(len(row) != 9 for row in sudoku):
        return False
    #Checks row of sudoku
    for row in sudoku:
        if not set(row) == set(range(1, 10)):
            return False
    #Checks column of sudoku
    for column in range(9):
        if not set(sudoku[row][column] for row in range(9)) == set(range(1, 10)):
            return False
    #Checks 3x3 box of sudoku
    for row_offset in range(0, 9, 3):
        for col_offset in range(0, 9, 3):
            box = [sudoku[row][column] for row in range(row_offset, row_offset + 3) for column in range(col_offset, col_offset + 3)]
            if not set(box) == set(range(1, 10)):
                return False
    return True

#Checks if inputted arguments equals 3 or else error occurs
numArg = len(sys.argv)
if (numArg != 3):
    raise Exception('ERROR: Not enough or too many input arguments.')
print("\nNumber of arguments passed", numArg)

#Prints my name and A#
argumentOne = sys.argv[0]
print("Omar, Hakawati:")

#Prints the input file name
argumentTwo = sys.argv[1]
print("Input file: ", argumentTwo)

#Prints the selected algorithm to solve the sudoku puzzle
argumentThree = sys.argv[2]
print("Selected Algorithm: ", argumentThree)

#Stores the input file and selected algorithm in variables
filename = str(sys.argv[1])
algorithm = int(sys.argv[2])

#Sets the puzzle variable to the unsolved sudoku puzzle located within the inputted csv file
puzzle = readCSV(filename)

#Solves the sudoku puzzle using the specified search algorithm chosen by the user
if algorithm == 1:
    #Prints inputted puzzle to the screen
    print('\nInput Puzzle:')
    PrintInput(puzzle)
    #Tracks runtime of the brute force algorithm
    startTime = default_timer()
    solved = bruteForceSearch(puzzle)
    endTime = default_timer()
    overallTime = endTime - startTime
    method = 'Brute Force Search'
    #Printing the number of nodes generated, search time, and search method using global counter, time variable, and method variable
    print(f'\nNumber of search tree nodes generated: {counter}.')
    print(f'Search time:  {overallTime:.10f} seconds.')
    print(f'\nSolved Puzzle using: {method}.')
    PrintOutput(solved)
elif algorithm == 2:
    #Prints inputted puzzle to the screen
    print('\nInput Puzzle:')
    PrintInput(puzzle)
    #Tracks runtime of the CSP Backtracking algorithm
    startTime1 = default_timer()
    solved = backTrackCSP(puzzle)
    endTime1 = default_timer()
    overallTime1 = endTime1 - startTime1
    method = 'Constraint Satisfaction Backtracking Search'
    #Printing the number of nodes generated, search time, and search method using global counter, time variable, and method variable
    print(f'\nNumber of search tree nodes generated: {counter}')
    print(f'Search time:  {overallTime1:.10f} seconds.')
    print(f'\nSolved Puzzle using: {method}.')
    PrintOutput(solved)
elif algorithm == 3:
    #Prints inputted puzzle to the screen
    print('\nInput Puzzle:')
    PrintInput(puzzle)
    #Tracks runtime of the CSP Backtracking algorithm
    startTime2 = default_timer()
    solved = forwardCheckCSP(puzzle)
    endTime2 = default_timer()
    overallTime2 = endTime2 - startTime2
    method = 'Constraint Satisfaction Forward Checking'
    #Printing the number of nodes generated, search time, and search method using global counter, time variable, and method variable
    print(f"\nNumber of search tree nodes generated: {counter}")
    print(f'Search time:  {overallTime2:.10f} seconds.')
    print(f'\nSolved Puzzle using: {method}.')
    PrintOutput(solved)
elif algorithm == 4:
    if checkValidSudoku(puzzle):
        PrintOutput(puzzle)
        print("\nThis is a valid, solved, sudoku puzzle")
    else:
        print("\nError: This is not a solved sudoku puzzle")
else:
    #Prints error message if there is an invalid algorithm selection
    print('Invalid Selection. Choose 1 for brute force, 2 for CSP backtracking, 3 for CSP forward checking, 4 for Solved??????')
    sys.exit()





