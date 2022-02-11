from timeit import default_timer
from copy import deepcopy
from exceptions import *


class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.solve_info = {}

    def possibilities_for_cell(self, row, col, board):
        # return a list of possible values for a cell
        # if the cell is already solved, return an empty list
        if self.puzzle.get_cell(row, col, board) != self.puzzle.empty_char:
            raise CellSolvedException
        # if the cell is not solved, return a list of possible values
        return [
            x
            for x in self.puzzle.nums
            if not self.puzzle.num_in_row(row, x, board)
            and not self.puzzle.num_in_col(col, x, board)
            and not self.puzzle.num_in_square(row, col, x, board)
        ]

    def solve(self):
        raise NotImplementedError

    def run(self):
        self.solve_info["start_time"] = default_timer()
        solution = self.solve()
        self.solve_info["end_time"] = default_timer()

        try:
            elapsed = self.solve_info["end_time"] - self.solve_info["start_time"]
            print(f"Time taken: {round(elapsed, 3)}")
        except KeyError:
            pass

        if solution:
            print("Solution found:")
            self.puzzle.from_list(solution)
            print(self.puzzle)
            self.puzzle.check_board_solved()
        else:
            print("No solution found.\n")


class RecursiveNaiveSolver(Solver):
    def __init__(self, puzzle, verbose=True):
        super().__init__(puzzle)
        self.verbose = verbose
        self.guesses = [None] * self.puzzle.size**2

    def get_guesses(self, row, col):
        return self.guesses[row * self.puzzle.size + col]

    def set_guesses(self, row, col, guesses):
        self.guesses[row * self.puzzle.size + col] = guesses

    def find_all_guesses(self, board):
        for r in range(self.puzzle.size):
            for c in range(self.puzzle.size):
                try:
                    guesses = self.possibilities_for_cell(r, c, board)
                except CellSolvedException:
                    self.set_guesses(r, c, None)
                    continue
                if len(guesses) == 0:
                    raise BadSolutionException
                self.set_guesses(r, c, guesses)

    def solve_recursive(self, board):
        try:
            self.find_all_guesses(board)
        except BadSolutionException:
            return False

        new_board = deepcopy(board)
        min_guess_loc, min_guess_len = None, self.puzzle.size

        for r in range(self.puzzle.size):
            for c in range(self.puzzle.size):
                guesses = self.get_guesses(r, c)
                if guesses is None:
                    continue  # cell already solved
                n_guesses = len(guesses)
                if n_guesses == 1:
                    self.puzzle.set_cell(r, c, guesses[0], new_board)
                elif n_guesses < min_guess_len:
                    min_guess_loc = r, c
                    min_guess_len = n_guesses

        if min_guess_loc is None:
            return new_board  # solved the board
        else:
            r, c = min_guess_loc
            guess = self.get_guesses(r, c)[0]
            self.puzzle.set_cell(r, c, guess, new_board)
            if self.verbose:
                print(self.puzzle.as_string(new_board))
            return self.solve_recursive(new_board)

    def solve(self):
        return self.solve_recursive(self.puzzle.board)
