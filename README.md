#Sudoku Solver
This is a simple sudoku solver written in python. It uses a genetic algorithm to solve the sudoku puzzle. The algorithm is as follows:
1. Generate a random population of sudoku boards
2. Calculate the fitness of each board
3. Select the top organisms the population
4. Breed the top organisms to create a new population
5. Mutate the new population
6. Repeat steps 2-5 until a solution is found
To run the program, simply run the following command:
```
python3 solver.py <sudoku board>.txt
```
The program will then print outthe final board, and the number of generations it took to solve the puzzle.
