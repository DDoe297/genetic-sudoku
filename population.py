'''
Population represents a population of organisms.
'''
import random
from copy import deepcopy

from .given import Given
from .organism import Organism


class Population:
    '''
    Population class represents a population of organisms.
    It contains a list of organisms.
    '''
    def __init__(self) -> None:
        '''
        Initializes the population with an empty list of organisms.
        '''
        self.people: list[Organism] = []

    def seed(self, size: int, given: Given) -> None:
        '''
        Seeds the population with a given number of organisms.
        Input:
            size: int - size of the population
            given: Given - given sudoku puzzle
        '''
        self.people = []
        for _ in range(size):
            organism: Organism = Organism()
            organism.randomize(given)
            self.people.append(organism)
        self.update_fitness()

    def update_fitness(self) -> None:
        '''
        Updates the fitness of all organisms in the population.
        '''
        for person in self.people:
            person.update_fitness()

    def sort(self) -> None:
        '''
        Sorts the organisms in the population by fitness in descending order.
        '''
        self.people.sort(key=lambda x: x.fitness, reverse=True)

    def crossover(self, parent1: Organism, parent2: Organism) -> tuple[Organism, Organism]:
        '''
        Performs crossover between two parents to produce two children using cycle crossover.
        Input:
            parent1: Organism - first parent
            parent2: Organism - second parent
        Output:
            child1: Organism - first child
            child2: Organism - second child
        '''
        child1: Organism = Organism()
        child2: Organism = Organism()
        child1.values = deepcopy(parent1.values)
        child2.values = deepcopy(parent2.values)
        crossover_point1, crossover_point2 = random.choices(range(9), k=2)
        if crossover_point1 > crossover_point2:
            crossover_point1, crossover_point2 = crossover_point2, crossover_point1
        for i in range(crossover_point1, crossover_point2):
            child1.values[i], child2.values[i] = self.cycle_crossover(
                child1.values[i], child2.values[i])
        return child1, child2

    def cycle_crossover(self, row1: list[int], row2: list[int]) -> tuple[list[int], list[int]]:
        '''
        Performs cycle crossover between two rows.
        Input:
            row1: list[int] - first row
            row2: list[int] - second row
        Output:
            new_row1: list[int] - first row after crossover
            new_row2: list[int] - second row after crossover
        '''
        new_row1: list[int] = [0 for _ in range(9)]
        new_row2: list[int] = [0 for _ in range(9)]
        remaining: list[int] = list(range(9))
        while (0 in new_row1) and (0 in new_row2):
            index: int = remaining[0]
            start: int = index
            next_index: int = -1
            remaining.remove(index)
            while next_index != start:
                new_row1[index] = row1[index]
                new_row2[index] = row2[index]
                next_index = row1.index(row2[index])
                index = next_index
                if index in remaining:
                    remaining.remove(index)
                else:
                    break
        return new_row1, new_row2

    def compete(self, selection_rate: float = 0.85) -> Organism:
        '''
        Selects two organisms from the population and returns one of them
        based on the selection rate.
        Input:
            selection_rate: float - probability of selecting the fittest organism
        Output:
            organism: Organism - selected organism
        '''
        choice_1, choice_2 = random.choices(self.people, k=2)
        fittest, weakest = sorted(
            (choice_1, choice_2), key=lambda p: p.fitness)
        if random.uniform(0, 1) < selection_rate:
            return fittest
        return weakest
