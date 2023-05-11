'''
Sudoku solver using a genetic algorithm.
'''
import sys
from copy import deepcopy

from .given import Given
from .organism import Organism
from .population import Population


class Sudoku:
    '''
    Sudoku class represents a sudoku puzzle.
    '''
    def __init__(self, file_name: str,
                population_size: int = 1000,
                elites_multiplier: float = 0.5,
                number_of_generations: int = 1500,
                mutation_rate: float = 0.1,
                reseed_after_stale: bool = False) -> None:
        '''
        Initializes the sudoku puzzle with a given file name.
        Input:
            file_name: str - name of the file containing the sudoku puzzle
        '''
        self.population: Population = Population()
        with open(file_name, 'r', encoding='utf-8') as file:
            values: list[list[int]] = []
            for line in file:
                values.append(list(map(int,line.split())))
            self.given: Given = Given(values)
        self.population_size: int = population_size
        self.number_of_elites: int = int(elites_multiplier*population_size)
        self.number_of_generations: int = number_of_generations
        self.mutation_rate: float = mutation_rate
        self.reseed_after_stale: bool = reseed_after_stale

    def solve(self) -> Organism | None:
        '''
        Solves the sudoku puzzle using a genetic algorithm.
        Output:
            Organism | None - solution to the sudoku puzzle
        '''
        mutation_rate: float = self.mutation_rate
        self.population.seed(self.population_size, self.given)
        stale: int = 0
        for generation in range(self.number_of_generations):
            max_fitness: Organism = max(self.population.people, key=lambda x: x.fitness)
            if max_fitness.fitness == 1:
                print(f'Solution found at generation {generation}!')
                print(max_fitness.values)
                return max_fitness
            print(f'Generation {generation}: {format(max_fitness.fitness*100, ".2f")}%')
            next_population: Population = Population()
            self.population.sort()
            elites: list[Organism] = []
            for i in range(self.number_of_elites):
                elite: Organism = Organism()
                elite.values = deepcopy(self.population.people[i].values)
                elites.append(elite)
            for _ in range(self.number_of_elites, self.population_size, 2):
                parent1: Organism = self.population.compete()
                parent2: Organism = self.population.compete()
                child1, child2 = self.population.crossover(parent1, parent2)
                child1.mutate(mutation_rate, self.given)
                child2.mutate(mutation_rate, self.given)
                next_population.people.append(child1)
                next_population.people.append(child2)
            next_population.people += elites
            self.population = next_population
            self.population.update_fitness()
            self.population.sort()
            if self.population.people[0].fitness != self.population.people[1].fitness:
                stale = 0
            else:
                stale += 1
            if stale > 30:
                print('Population has gone stale')
                if self.reseed_after_stale:
                    self.population.seed(self.population_size, self.given)
                stale = 0
                mutation_rate *= 1.1
        print('No solution found')
        return None


s: Sudoku = Sudoku(sys.argv[1])
s.solve()
