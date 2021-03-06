from timeit import default_timer
from copy import deepcopy
from exceptions import *


class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.solve_info = {}

    def possibilities_for_cell(self, row, col, board):
        # return a list of possible values for a cell
        # if the cell is already solved, return None
        if self.puzzle.get_cell(row, col, board) != self.puzzle.empty_char:
            return None
        return [
            x
            for x in self.puzzle.nums
            if not self.puzzle.num_in_row(row, x, board)
            and not self.puzzle.num_in_col(col, x, board)
            and not self.puzzle.num_in_square(row, col, x, board)
        ]

    def presolve(self):
        # make the search problem easier, if possible, by repeatedly filling in
        # any cells we immediately know the answer to
        while True:
            made_changes = False
            for r in range(self.puzzle.size):
                for c in range(self.puzzle.size):
                    guess = self.possibilities_for_cell(r, c, self.puzzle.board)
                    if guess is not None and len(guess) == 1:
                        self.puzzle.set_cell(r, c, guess[0])
                        made_changes = True
            if not made_changes:
                break

    def solve(self):
        raise NotImplementedError

    def run(self):
        self.solve_info["start_time"] = default_timer()
        solution = self.solve()
        self.solve_info["end_time"] = default_timer()

        try:
            elapsed = self.solve_info["end_time"] - self.solve_info["start_time"]
            print(f"Time taken: {round(elapsed, 3)} seconds")
        except KeyError:
            pass

        if solution:
            print("Solution found:")
            self.puzzle.from_list(solution)
            print(self.puzzle)
            self.puzzle.check_board_solved()
        else:
            print("No solution found.")
        print()


class RecursiveNaiveSolver(Solver):
    def __init__(self, puzzle, verbose=True):
        super().__init__(puzzle)
        self.verbose = verbose
        self.guesses = [None] * self.puzzle.size**2

    def get_guess(self, row, col):
        return self.guesses[row * self.puzzle.size + col]

    def set_guess(self, row, col, guesses):
        self.guesses[row * self.puzzle.size + col] = guesses

    def find_all_guesses(self, board):
        for r in range(self.puzzle.size):
            for c in range(self.puzzle.size):
                guess = self.possibilities_for_cell(r, c, board)
                if guess is not None and len(guess) == 0:
                    raise BadSolutionException
                self.set_guess(r, c, guess)

    def solve_recursive(self, board):
        try:
            self.find_all_guesses(board)
        except BadSolutionException:
            return False

        new_board = deepcopy(board)
        best_guess, best_guess_loc, best_guess_len = None, None, self.puzzle.size

        for r in range(self.puzzle.size):
            for c in range(self.puzzle.size):
                guess = self.possibilities_for_cell(r, c, new_board)
                if guess is None:  # cell already solved
                    continue
                n_choices = len(guess)
                if n_choices == 1:  # answer trivial
                    self.puzzle.set_cell(r, c, guess[0], new_board)
                elif n_choices < best_guess_len:
                    best_guess = guess
                    best_guess_loc = r, c
                    best_guess_len = n_choices
                    if best_guess_len == 2:
                        break  # can't improve on this

        if best_guess_loc is None:
            return new_board  # solved the board
        else:
            r, c = best_guess_loc
            for g in best_guess:
                self.puzzle.set_cell(r, c, g, new_board)
                if self.verbose:
                    print(self.puzzle.as_string(new_board))
                solution = self.solve_recursive(new_board)
                if solution:
                    return solution
            return False

    def solve(self):
        self.presolve()
        return self.solve_recursive(self.puzzle.board)
