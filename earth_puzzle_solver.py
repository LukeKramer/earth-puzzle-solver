import time
from ortools.sat.python import cp_model
from concurrent.futures import ThreadPoolExecutor
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EarthPuzzleSolver:
    def __init__(self, letter_ranges):
        self.letter_ranges = letter_ranges
        self.model = cp_model.CpModel()
        self.variables = self._create_variables()
        self.word_positions = self._define_word_positions()

    def _create_variables(self):
        """Create variables for each unique letter in the puzzle."""
        letters = "NORTH EAST SOUTH WEST EARTH"
        unique_letters = sorted(set(letters.replace(" ", "")))
        return {letter: self.model.NewIntVar(0, 9, letter) for letter in unique_letters}

    def _define_word_positions(self):
        """Define the positional multipliers for each word in the puzzle."""
        return {
            "NORTH": [10000, 1000, 100, 10, 1],
            "EAST": [1000, 100, 10, 1],
            "SOUTH": [10000, 1000, 100, 10, 1],
            "WEST": [1000, 100, 10, 1],
            "EARTH": [10000, 1000, 100, 10, 1],
        }

    def _word_value(self, word):
        """Calculate the word's value based on its letter positions."""
        return sum(self.variables[letter] * pos for letter, pos in zip(word, self.word_positions[word]))

    def _add_constraints(self):
        """Add all the constraints to the model."""
        # Add AllDifferent constraint
        self.model.AddAllDifferent(self.variables.values())
        
        # Prevent leading zeros
        self.model.Add(self.variables["N"] > 0)
        self.model.Add(self.variables["E"] > 0)
        self.model.Add(self.variables["S"] > 0)

        # Add the main equation constraint
        self.model.Add(self._word_value("NORTH") + self._word_value("EAST") + self._word_value("SOUTH") + self._word_value("WEST") == self._word_value("EARTH"))
        self.model.Add(self._word_value("EARTH") >= 10000)
        self.model.Add(self._word_value("EARTH") < 100000)

        # Apply letter range constraints
        for letter, (low, high) in self.letter_ranges.items():
            self.model.Add(self.variables[letter] >= low)
            self.model.Add(self.variables[letter] <= high)

    def solve(self):
        """Solve the puzzle and return the solutions."""
        solver = cp_model.CpSolver()
        solutions = []

        class SolutionPrinter(cp_model.CpSolverSolutionCallback):
            def __init__(self, variables, word_positions):
                cp_model.CpSolverSolutionCallback.__init__(self)
                self.variables = variables
                self.word_positions = word_positions

            def OnSolutionCallback(self):
                solution = {letter: self.Value(var) for letter, var in self.variables.items()}
                n_value = sum(solution[letter] * pos for letter, pos in zip("NORTH", self.word_positions["NORTH"]))
                e_value = sum(solution[letter] * pos for letter, pos in zip("EAST", self.word_positions["EAST"]))
                s_value = sum(solution[letter] * pos for letter, pos in zip("SOUTH", self.word_positions["SOUTH"]))
                w_value = sum(solution[letter] * pos for letter, pos in zip("WEST", self.word_positions["WEST"]))
                ea_value = sum(solution[letter] * pos for letter, pos in zip("EARTH", self.word_positions["EARTH"]))

                logger.info(f"NORTH: {n_value}, EAST: {e_value}, SOUTH: {s_value}, WEST: {w_value}, EARTH: {ea_value}")
                solutions.append((n_value, e_value, s_value, w_value, ea_value))

        self._add_constraints()
        solver.SearchForAllSolutions(self.model, SolutionPrinter(self.variables, self.word_positions))
        return solutions


def solve_earth_puzzle():
    """Solve the Earth puzzle using parallelization."""
    # Define letter ranges for partitioning the search space
    ranges = [
        {"N": (1, 3)},  # Example partition
        {"N": (4, 6)},
        {"N": (7, 9)},
    ]

    all_solutions = []

    # Use ThreadPoolExecutor to parallelize the solving process
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda r: EarthPuzzleSolver(r).solve(), ranges)

    # Combine results from all subproblems
    for result in results:
        all_solutions.extend(result)

    logger.info(f"Total solutions: {len(all_solutions)}")
    return all_solutions


if __name__ == "__main__":
    start_time = time.time()
    solve_earth_puzzle()
    logger.info(f"Execution Time: {(time.time() - start_time) * 1000:.3f} ms")
