# Earth Puzzle Solver
This Python script solves a cryptarithmetic puzzle where each letter represents a unique digit, and the sum of the values formed by the words "NORTH", "EAST", "SOUTH", "WEST", and "EARTH" must satisfy the equation:

NORTH + EAST + SOUTH + WEST = EARTH

# Features:
Constraint Programming: Uses Google OR-Tools' CP-SAT solver to find solutions.
Parallelization: Utilizes Python's ThreadPoolExecutor to solve subproblems in parallel, improving performance.
Efficient Solution Search: The search space is partitioned by letter ranges to optimize the solving process.
# Installation
To run this script, you need to install the required dependencies. The script uses Google OR-Tools for solving the puzzle, and Python's built-in libraries for parallelization and logging.

Install OR-Tools:

pip install ortools

Clone or Download the Script:

Clone the repository or download the script directly.
# Usage
Run the script directly from the command line or as a Python module.

Run the script:

python earth_puzzle_solver.py

Expected Output: The script will print the solutions to the puzzle in the following format:

NORTH: 48150, EAST: 9325, SOUTH: 28750, WEST: 6925, EARTH: 93150
NORTH: 39150, EAST: 8425, SOUTH: 29750, WEST: 6825, EARTH: 84150
...
It will also print the total number of solutions found and the execution time in milliseconds.

# How It Works
Define Variables: The letters "NORTH", "EAST", "SOUTH", "WEST", and "EARTH" are assigned unique digits from 0 to 9. The script ensures that no two letters share the same digit using the AddAllDifferent constraint.

Add Constraints:

The first constraint ensures that the sum of the values for "NORTH", "EAST", "SOUTH", and "WEST" equals the value for "EARTH".
Leading zeros are disallowed for the first letters of each word (N, E, S).
The value of "EARTH" is constrained to be a 5-digit number.
Parallelization: The search space is divided into subproblems by applying letter range constraints (e.g., the letter "N" can be between 1 and 3 in one subproblem, between 4 and 6 in another, etc.). These subproblems are solved in parallel using ThreadPoolExecutor.

Solutions: Each valid solution is printed in the format: NORTH: <value>, EAST: <value>, SOUTH: <value>, WEST: <value>, EARTH: <value>. The total number of solutions is displayed at the end.

Example Output:

NORTH: 48150, EAST: 9325, SOUTH: 28750, WEST: 6925, EARTH: 93150
NORTH: 39150, EAST: 8425, SOUTH: 29750, WEST: 6825, EARTH: 84150
NORTH: 39650, EAST: 7825, SOUTH: 29450, WEST: 1725, EARTH: 78650
...
Total solutions: 3
Execution Time: 2.123 ms

# Notes
The script uses parallelization to improve the speed of solving the puzzle by dividing the search space into subproblems.
The puzzle is solved using Google OR-Tools' CP-SAT solver, which is a constraint programming solver designed to efficiently handle combinatorial optimization problems.
