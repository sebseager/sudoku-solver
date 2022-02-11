from copy import deepcopy
from timeit import default_timer
import glob


class BoardError(Exception):
    pass


class CellSolvedException(Exception):
    pass


class BadSolutionException(Exception):
    pass


class Puzzle:
    def __init__(self):
        self.size = 9
        self.square_size = 3
        self.empty_char = "."
        self.board = [self.empty_char] * self.size**2
        self.nums = list(range(1, self.size + 1))
        self.str_nums = [str(n) for n in self.nums]

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])

    def from_string(self, s, delim=""):
        s = s.strip()
        if len(s) != self.size**2:
            raise BoardError(
                f"Line length ({len(s)}) must match board size ({self.size**2})"
            )
        s = s if delim == "" else s.replace(delim, "")
        self.board = [int(x) if x in self.str_nums else self.empty_char for x in s]

    def from_file_oneline(self, path, delim=""):
        with open(path, "r") as f:
            line = f.readline()
            self.from_string(line, delim)

    def from_file_square(self, path, delim=","):
        with open(path, "r") as f:
            csv = f.readlines()
            if len(csv) != self.size:
                raise BoardError(f"CSV height must match board size ({self.size})")
            for r in range(self.size):
                line = line if delim == "" else csv[r].replace(delim, "")
                if len(line) != self.size:
                    raise BoardError(f"CSV width must match board size ({self.size})")
                self.board[r] = [
                    int(x) if x in self.str_nums else self.empty_char for x in line
                ]

    def idx(self, row, col):
        return row * self.size + col

    def get_cell(self, row, col):
        try:
            return self.board[self.idx(row, col)]
        except IndexError:
            raise BoardError(f"Cell at row {row}, column {col} is out of bounds")

    def set_cell(self, row, col, value):
        if value not in self.nums:
            raise BoardError(f"Invalid value {value}")
        if self.get_cell(row, col) != self.empty_char:
            raise CellSolvedException(f"Cell {row}, {col} already solved")
        self.board[self.idx(row, col)] = value

    def get_col(self, col):
        return [self.get_cell(r, col) for r in range(self.size)]

    def get_row(self, row):
        return [self.get_cell(row, c) for c in range(self.size)]

    def get_cols(self):
        return [self.get_col(i) for i in range(self.size)]

    def get_rows(self):
        return [self.get_row(i) for i in range(self.size)]

    def get_square(self, row, col):
        # get the square containing the cell at row, col
        start_row = (row // self.square_size) * self.square_size
        start_col = (col // self.square_size) * self.square_size
        return [
            self.get_cell(r, c)
            for r in range(start_row, start_row + self.square_size)
            for c in range(start_col, start_col + self.square_size)
        ]

    def num_in_col(self, col, num):
        return num in self.get_col(col)

    def num_in_row(self, row, num):
        return num in self.get_row(row)

    def num_in_square(self, row, col, num):
        return num in self.get_square(row, col)

    def is_component_solved(self, component):
        # component should be a list (i.e., from get_col, get_row, or get_square)
        if len(set(component)) != len(component):
            return False
        if any(x not in component for x in self.nums):
            return False
        return True

    def check_board_solved(self):
        print("Solution submitted. Verifying it...")
        # check each row, column, and square
        for i in range(self.size):
            if not self.is_component_solved(self.get_row(i)):
                print("Mistake in row", i)
                return False
            if not self.is_component_solved(self.get_col(i)):
                print("Mistake in column", i)
                return False
            if not self.is_component_solved(self.get_square(i)):
                print("Mistake in square", i)
                return False
        print("Solution is correct!")
        return True


class Solver:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.solve_info = {}

    def possibilities_for_cell(self, puzzle, row, col):
        # return a list of possible values for a cell
        # if the cell is already solved, return an empty list
        if puzzle.get_cell(row, col) != puzzle.empty_char:
            raise CellSolvedException
        # if the cell is not solved, return a list of possible values
        return [
            x
            for x in puzzle.nums
            if not puzzle.num_in_row(row, x)
            and not puzzle.num_in_col(col, x)
            and not puzzle.num_in_square(row, col, x)
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
            print(solution, "\n")
            self.puzzle.check_board_solved()
        else:
            print("No solution found.")


class RecursiveBacktrackingSolver(Solver):
    def __init__(self, puzzle):
        super().__init__(puzzle)
        self.guesses = [None] * self.puzzle.size**2

    def get_guesses(self, row, col):
        return self.guesses[row * self.puzzle.size + col]

    def set_guesses(self, row, col, guesses):
        self.guesses[row * self.puzzle.size + col] = guesses

    def get_row_col(self, i):
        return i // self.puzzle.size, i % self.puzzle.size

    def find_all_guesses(self):
        for r in range(self.puzzle.size):
            for c in range(self.puzzle.size):
                try:
                    guesses = self.possibilities_for_cell(self.puzzle, r, c)
                except CellSolvedException:
                    self.set_guesses(r, c, None)
                    continue
                if len(guesses) == 0:
                    raise BadSolutionException
                self.set_guesses(r, c, guesses)

    def solve_recursive(self, board):
        try:
            self.find_all_guesses()
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
                    new_board[self.puzzle.idx(r, c)] = guesses[0]
                elif n_guesses < min_guess_len:
                    min_guess_loc = r, c
                    min_guess_len = n_guesses

        if min_guess_loc is None:
            return new_board  # solved the board
        else:
            r, c = min_guess_loc
            guess = self.get_guesses(r, c)[0]
            new_board[self.puzzle.idx(r, c)] = guess
            return self.solve_recursive(new_board)

    def solve(self):
        return self.solve_recursive(self.puzzle.board)


if __name__ == "__main__":
    test_dir = "tests"
    test_files = [
        f for f in glob.glob(f"{test_dir}/*.*") if not f.startswith(f"{test_dir}/t")
    ]

    for f in test_files:
        with open(f, "r") as fp:
            for i, line in enumerate(fp.readlines()):
                print(f"Testing file {f} [puzzle {i}]...")
                puzzle = Puzzle()
                puzzle.from_string(line)
                solver = RecursiveBacktrackingSolver(puzzle)
                solver.run()
