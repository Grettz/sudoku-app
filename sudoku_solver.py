
class SudokuSolver():
    COLUMNS = [1,2,3,4,5,6,7,8,9]
    ROWS = ['A','B','C','D','E','F','G','H','I']

    def __init__(self, sudoku):
        self.sudoku = sudoku

    def solve(self):
        #print('Solving sudoku...\n')

        # Fill each empty cell with a list of valid numbers for that cell
        self.add_possible_values()
        #self.pprint()

        num_added = 0 # Number of cells filled in with numbers
        while True:
            # Fill cells that have only one valid solution i.e. list length of 1
            counter = self.fill_single_value_cells()

            # Fills cells that are the only place a number can go in a given row, column, or block
            counter += self.find_numbers()

            if counter < 1:
                break
            num_added += counter

        if self.is_solved():
            #print('\nSudoku Solved.')
            pass
        else:
            #print('\nCould not solve sudoku..')
            pass

        #print('Filled {0} cells.'.format(num_added))
       # self.pprint()

        return self.sudoku


    def add_possible_values(self):
        # Adds an array of all possible values to each empty cell
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0 or self.sudoku[i][j] == None: # If cell is empty
                    row_numbers = self.get_numbers_in_row(i)
                    col_numbers = self.get_numbers_in_column(j)
                    block_numbers = self.get_numbers_in_block(i, j)

                    # Create list of valid numbers to fill the cell
                    used_numbers = list(dict.fromkeys(row_numbers + col_numbers + block_numbers)) # Numbers that cant go in the cell
                    possible_numbers = self.COLUMNS.copy()
                    for num in used_numbers:
                        possible_numbers.remove(num)

                    # Add the array of possible numbers to the sudoku board
                    self.sudoku[i][j] = possible_numbers

    def fill_single_value_cells(self):
        # Function to find arrays (possible values) of length 1 and insert that single value into the cell
        counter = 0
        for i in range(9):
            for j in range(9):
                cell = self.sudoku[i][j]
                if type(cell) == list and len(cell) == 1:
                    self.sudoku[i][j] = cell[0]
                    # Remove the inserted number from possible values in this cells row, column, and block
                    self.update_cell_values(i, j)
                    counter += 1

        #print('Filled {0} cells that have a single possible value'.format(counter))

        return counter

    def find_numbers(self):
        # This function searches each row, column, block to find possible numbers that only show up once in that row, column, block and insert it into the cell
        counter = 0

        # Search rows
        for i in range(9):
            num_freq = [0] * 9

            for j in range(9):
                cell = self.sudoku[i][j]

                if type(cell) == list:
                    for val in cell:
                        num_freq[val-1] += 1

            # Check for rows that have a number that only shows up once
            for k in range(9):
                freq = num_freq[k]
                
                if freq == 1:
                    for j in range(9):
                        cell = self.sudoku[i][j]

                        if type(cell) == list:
                            if (k+1) in cell:
                                self.sudoku[i][j] = k + 1
                                self.update_cell_values(i, j)
                                #print('Filled {} in row {}, column {}'.format(k+1, i, j))
                                counter += 1
                
        # Search columns
        for j in range(9):
            num_freq = [0] * 9

            for i in range(9):
                cell = self.sudoku[i][j]

                if type(cell) == list:
                    for val in cell:
                        num_freq[val-1] += 1

            # Check for columns that have a number that only shows up once
            for k in range(9):
                freq = num_freq[k]

                if freq == 1:
                    for i in range(9):
                        cell = self.sudoku[i][j]

                        if type(cell) == list:
                            if (k+1) in cell:
                                self.sudoku[i][j] = k + 1
                                self.update_cell_values(i, j)
                                #print('Filled {} in column {}, row {}'.format(k+1, j, i))
                                counter += 1

        # Search blocks
        for block in range(9):
            b_i = int(block / 3) * 3
            b_j = (block % 3) * 3

            # Track how often each possible value for empty cells shows up in the block
            num_freq = [0] * 9
            for i in range(3):
                for j in range(3):
                    _i = b_i + i
                    _j = b_j + j
                    cell = self.sudoku[_i][_j]

                    if type(cell) == list:
                        for val in cell:
                            num_freq[val-1] += 1

            for k in range(9):
                freq = num_freq[k]
                
                if freq == 1:
                    for i in range(3):
                        for j in range(3):
                            _i = b_i + i
                            _j = b_j + j
                            cell = self.sudoku[_i][_j]
                            if type(cell) == list:
                                if (k+1) in cell:
                                    self.sudoku[_i][_j] = k + 1
                                    self.update_cell_values(_i, _j)
                                    #print('Filled {} in row {}, column {} from block'.format(k+1, _i, _j))



        return counter


    def update_cell_values(self, i, j):
        # This function updates the cells row, column, and block to remove the cells value
        num = self.sudoku[i][j]
        # Update row
        for cell in self.sudoku[i]:
            if type(cell) == list:
                if num in cell:
                    #print('removed', num, 'from row', i, ',', cell)
                    cell.remove(num)
        # Update column
        for k in range(9):
            cell = self.sudoku[k][j]
            if type(cell) == list:
                if num in cell:
                    #print('removed', num, 'from column', k, j, ',', cell)
                    cell.remove(num)
        # Update block
        idx_i, idx_j = get_block_index(i, j) # i and j index for the 3x3 block
        for k in range(idx_i, idx_i + 3):
            for l in range(idx_j, idx_j + 3):
                cell = self.sudoku[k][l]
                if type(cell) == list:
                    if num in cell:
                        #print('removed', num, 'from block', idx_i, idx_j, cell)
                        cell.remove(num)


    def get_numbers_in_row(self, i):
        # Returns array of numbers in row i
        numbers = []
        for num in self.sudoku[i]:
            if type(num) == int and num > 0:
                numbers.append(num)
        return numbers

    def get_numbers_in_column(self, j):
        # Returns an array of numbers in column j
        numbers = []
        for i in range(9):
            num = self.sudoku[i][j]
            if type(num) == int and num > 0:
                numbers.append(num)
        # Remove duplicate values
        numbers = list(dict.fromkeys(numbers))
        return numbers

    def get_numbers_in_block(self, i, j):
        # Returns an array of numbers in that 3x3 block
        idx_i, idx_j = get_block_index(i, j)

        numbers = []
        for i in range(idx_i, idx_i + 3):
            for j in range(idx_j, idx_j + 3):
                num = self.sudoku[i][j]
                if type(num) == int and num > 0:
                    numbers.append(num)
        return numbers


    def is_solved(self):
        # Check rows
        for i in range(9):
            numbers = self.COLUMNS.copy()

            for j in range(9):
                cell = self.sudoku[i][j]

                if cell not in numbers:
                    return False

                numbers.remove(cell)

        # Check columns
        for j in range(9):
            numbers = self.COLUMNS.copy()

            for i in range(9):
                cell = self.sudoku[i][j]

                if cell not in numbers:
                    return False

                numbers.remove(cell)

        # Check blocks
        for k in range(9):
            # Block index
            b_i = int(k / 3) * 3
            b_j = (k % 3) * 3
        
            numbers = self.COLUMNS.copy()

            for _i in range(3):
                for _j in range(3):
                    # Cell index
                    i = b_i + _i
                    j = b_j + _j
                    cell = self.sudoku[i][j]

                    if cell not in numbers:
                        return False

                    numbers.remove(cell)
        return True

    def pprint(self):
        for i in range(9):
            # This second loop replaces the list of posible numbers with empty cells for printing. comment it out to keep lists for debugging etc.
            # for j in range(9):
            #     if type(sudoku[i][j]) == list:
            #         sudoku[i][j] = 0

            # Format the sudoku for printing
            line = str(self.sudoku[i]).replace('0', '-').replace(',', '')
            line_f = ' ' + line[1:6] + ' ' + line[6:12] + ' ' + line[12:-1]

            if i % 3 == 0:
                print()
            print(line_f)
        return


def get_block_index(i, j):
    # Get the i and j indexes for the 3x3 block containing cell i, j
    idx_i = 3 * int(i / 3)
    idx_j = 3 * int(j / 3)
    return idx_i, idx_j


sudoku = [
    [0,0,0,2,0,0,7,0,8],
    [0,3,0,8,0,0,4,0,5],
    [9,0,6,0,0,0,0,0,0],
    [6,0,2,0,4,8,5,7,0],
    [5,0,8,7,0,3,6,0,9],
    [0,7,9,6,1,0,2,0,4],
    [0,0,0,0,0,0,3,0,6],
    [1,0,3,0,0,6,0,2,0],
    [7,0,5,0,0,2,0,0,0]
]

sudoku2 = [
    [1,6,9,0,0,0,0,0,0],
    [0,7,0,6,9,0,3,0,0],
    [0,0,4,0,5,1,0,6,0],
    [8,0,0,0,0,0,0,0,1],
    [0,0,0,3,7,0,5,0,0],
    [0,0,0,0,6,5,0,0,0],
    [0,9,0,0,0,0,0,0,7],
    [0,8,0,0,0,0,0,5,2],
    [0,5,2,0,0,7,0,0,0]
]

sudoku3 = [
    [9,7,0,0,0,5,3,0,0],
    [0,0,0,2,3,0,8,7,0],
    [1,2,0,8,0,0,0,6,0],
    [2,0,7,0,0,0,6,0,0],
    [0,5,0,7,8,6,0,2,0],
    [0,0,0,0,1,0,0,0,0],
    [0,0,2,0,0,4,1,9,0],
    [3,1,0,0,0,0,0,0,6],
    [0,4,0,0,6,0,0,0,0]
]

sudoku4 = [
    [6,3,0,0,0,0,0,8,1],
    [0,2,0,0,0,3,0,0,0],
    [0,0,0,0,1,7,4,3,0],
    [0,9,6,4,0,0,5,7,0],
    [0,0,0,7,6,2,0,0,0],
    [0,8,0,0,0,0,6,0,0],
    [0,6,0,0,2,0,0,0,0],
    [3,0,9,0,0,0,0,6,0],
    [0,0,0,0,0,0,0,0,9]
]


if __name__ == "__main__":
    # Attempt to solve all sudokus from each difficulty
    difficulty = ['Very Easy', 'Easy', 'Moderate', 'Hard', 'Very Hard']

    for lvl in range(5):
        with open('sudoku_9x9_lvl_' + str(lvl+1) + '.txt') as file:
            ran = 0
            solved = 0

            # Get each sudoku from line
            for line in file:
                if line[-1] == ']':
                    sudoku = line[2:-2].split('], [')
                else:
                    sudoku = line[2:-3].split('], [')

                for i, row in enumerate(sudoku):
                    sudoku[i] = row.split(', ')
                    for j in range(9):
                        try:
                            sudoku[i][j] = int(sudoku[i][j])
                        except:
                            pass
                    
                s = SudokuSolver(sudoku)
                s.solve()

                if s.is_solved() is True:
                    solved += 1
                ran += 1

            percent = (solved / ran) * 100

            print('{0} - {1:2.2f}% - {2}/{3}'.format(difficulty[lvl], percent, solved, ran))



    # s = SudokuSolver(sudoku)
    # s.pprint()
    # s.solve()