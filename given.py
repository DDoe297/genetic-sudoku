'''
Given represents the given sudoku puzzle.
'''
class Given:
    '''
    Given class represents the given sudoku puzzle.
    It contains a 9x9 matrix of integers, each representing a value in the sudoku puzzle.
    It also contains a 9x9x9 matrix of integers, each representing a possible value for a given cell
    in the sudoku puzzle.
    '''
    def __init__(self, values: list[list[int]]) -> None:
        '''
        Initializes the given with a 9x9 matrix of integers and a 9x9x9 matrix of integers.
        The 9x9 matrix of integers is the given sudoku puzzle.
        The 9x9x9 matrix of integers is a helper matrix that contains all the possible values for
        each cell in the sudoku puzzle.
        Input:
            values: list[list[int]] - 9x9 matrix of integers
        '''
        super().__init__()
        self.values: list[list[int]] = values
        self.helper_values: list[list[list[int]]] = \
            [[[] for _ in range(9)] for _ in range(9)]
        for row in range(9):
            for column in range(9):
                for value in range(1, 10):
                    if (
                        self.values[row][column] == 0) and \
                        not (self.is_column_duplicate(column, value) or \
                            self.is_block_duplicate(row, column, value) or \
                            self.is_row_duplicate(row, value)):
                        self.helper_values[row][column].append(value)
                    elif self.values[row][column] != 0:
                        self.helper_values[row][column].append(
                            self.values[row][column])
                        break

    def is_row_duplicate(self, row: int, value: int) -> bool:
        '''
        Checks if the given value is already in the given row.
        Input:
            row: int - row index
            value: int - value to check
        Output:
            bool - True if the value is already in the row, False otherwise
        '''
        return value in self.values[row]

    def is_column_duplicate(self, column: int, value: int) -> bool:
        '''
        Checks if the given value is already in the given column.
        Input:
            column: int - column index
            value: int - value to check
        Output:
            bool - True if the value is already in the column, False otherwise
        '''
        for row in range(9):
            if self.values[row][column] == value:
                return True
        return False

    def is_block_duplicate(self, row: int, column: int, value: int) -> bool:
        '''
        Checks if the given value is already in the given block.
        Input:
            row: int - row index
            column: int - column index
            value: int - value to check
        Output:
            bool - True if the value is already in the block, False otherwise
        '''
        i: int = row - (row % 3)
        j: int = column - (column % 3)
        values: list[int] = [self.values[i][j], self.values[i][j+1], self.values[i][j+2],
                self.values[i+1][j], self.values[i+1][j+1], self.values[i+1][j+2],
                self.values[i+2][j], self.values[i+2][j+1], self.values[i+2][j+2]]
        return value in values
    