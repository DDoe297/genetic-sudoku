'''
Organism represents a single solution to the sudoku puzzle.
'''
import random

from .given import Given


class Organism:
    '''
    Organism class represents a single solution to the sudoku puzzle.
    It contains a 9x9 matrix of integers, each representing a value in the sudoku puzzle.
    It also contains a fitness value, which is a float between 0 and 1,
    representing how close the solution is to the actual solution.
    '''

    def __init__(self) -> None:
        '''
        Initializes the organism with a 9x9 matrix of 0s and a fitness of 0.
        '''
        self.values: list[list[int]] = \
            [[0 for _ in range(9)] for _ in range(9)]
        self.fitness: float = 0

    def update_fitness(self) -> None:
        '''
        Updates the fitness of the organism.
        The fitness is calculated by taking the average of the fitness of the columns and blocks.
        The fitness of a column or block is calculated by taking the number of
        unique values in the column or block and dividing it by 9.
        '''
        column_fitness: float = 0
        block_fitness: float = 0
        for i in range(9):
            column_fitness += len({self.values[j][i] for j in range(9)})/9
        column_fitness /= 9
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block: list[int] = \
                    [self.values[i][j], self.values[i][j+1], self.values[i][j+2],
                     self.values[i+1][j], self.values[i +
                                                      1][j+1], self.values[i+1][j+2],
                     self.values[i+2][j], self.values[i+2][j+1], self.values[i+2][j+2]]
                block_fitness += len(set(block))/9
        block_fitness /= 9
        self.fitness = column_fitness * block_fitness

    def mutate(self, mutation_rate: float, given: Given) -> None:
        '''
        Mutates the organism by swapping two values in the same row.
        Input:
            mutation_rate: float - probability of mutation
            given: Given - given sudoku puzzle
        '''
        chance: float = random.uniform(0, 1)
        if chance > mutation_rate:
            for _ in range(5):
                while True:
                    from_row: int = random.randint(0, 8)
                    from_column, to_column = random.sample(range(9), 2)
                    if given.values[from_row][from_column] == 0 \
                    and given.values[from_row][to_column] == 0:
                        if (
                        not given.is_column_duplicate(to_column, self.values[from_row][from_column])
                        and not given.is_column_duplicate(from_column, self.values[from_row][to_column])
                        and not given.is_block_duplicate(from_row, to_column, self.values[from_row][from_column])
                        and not given.is_block_duplicate(from_row, from_column, self.values[from_row][to_column])):
                            self.values[from_row][to_column], self.values[from_row][from_column] =\
                            self.values[from_row][from_column], self.values[from_row][to_column]
                            break

    def randomize(self, given: Given) -> None:
        '''
        Randomizes the organism by filling in the empty spaces with random values.
        Input:
            given: Given - given sudoku puzzle
        '''
        for i in range(9):
            for j in range(9):
                if given.values[i][j] != 0:
                    self.values[i][j] = given.values[i][j]
            while len(set(self.values[i])) != 9:
                for j in range(9):
                    if given.values[i][j] == 0:
                        choice: int = random.choice(given.helper_values[i][j])
                        self.values[i][j] = choice
