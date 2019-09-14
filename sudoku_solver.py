
class SudokuSolver():
    numbers = [1,2,3,4,5,6,7,8,9]

    def __init__(self, sudoku):
        self.sudoku = sudoku
        self.pprint()
        print('Solving sudoku...')
        self.solve()

    def solve(self):
        self.add_possible_values() # Fill each empty square with all possible values

        while True:
            counter = self.fill_numbers()
            if counter < 1:
                break

        self.pprint()
        return self.sudoku

    def add_possible_values(self):
        # Adds an array of all possible values to each empty cell
        for i in range(9):
            for j in range(9):
                if self.sudoku[i][j] == 0 or self.sudoku[i][j] == None: # If cell is empty
                    row_numbers = self.get_numbers_in_row(i)
                    col_numbers = self.get_numbers_in_column(j)
                    block_numbers = self.get_numbers_in_block(i, j)

                    possible_numbers = self.numbers.copy() # Numbers that can go in this cell
                    used_numbers = list(dict.fromkeys(row_numbers + col_numbers + block_numbers)) # Numbers that are in this cells row, column, or block; and cannot go in this sqaure
                    for num in used_numbers:
                        possible_numbers.remove(num)

                    # Add the array of possible numbers to the sudoku board
                    self.sudoku[i][j] = possible_numbers

    def fill_numbers(self):
        # Function to find arrays (possible values) of length 1 and insert that single value into the cell
        counter = 0
        for i in range(9):
            for j in range(9):
                cell = self.sudoku[i][j]
                if type(cell) == list and len(cell) == 1:
                    counter += 1
                    self.sudoku[i][j] = cell[0]
                    # Remove the inserted number from possible values in this cells row, column, and block
                    self.update_cell_values(i, j)

        print('Filled {0} cells that have a single possible value'.format(counter))
        return counter

    def find_numbers(self):
        # This function searches each row, column, block to find possible numbers that only show up once in that row, column, block and insert it into the cell
        # Search rows
        for i in range(9):
            pass

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
        # Returns an array of numbers in that row
        numbers = []
        for num in self.sudoku[i]:
            if type(num) == int and num > 0:
                numbers.append(num)
        # Remove duplicate values
        numbers = list(dict.fromkeys(numbers))
        return numbers

    def get_numbers_in_column(self, j):
        # Returns an array of numbers in that column
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
        # Remove duplicate values
        numbers = list(dict.fromkeys(numbers))
        return numbers

    def is_solved(self):
        pass

    def pprint(self):
        for i in range(9):
            print(str(self.sudoku[i]).replace('0', '_').replace(',', ''))


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


if __name__ == "__main__":
    SudokuSolver(sudoku)
    print('----------------------------------')
    SudokuSolver(sudoku3)