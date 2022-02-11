from exceptions import *


class Puzzle:
    def __init__(self):
        self.size = 9
        self.square_size = 3
        self.empty_char = "."
        self.board = [self.empty_char] * self.size**2
        self.nums = list(range(1, self.size + 1))
        self.str_nums = [str(n) for n in self.nums]

    def __str__(self):
        return self.as_string()

    def from_list(self, l):
        if len(l) != self.size**2:
            raise BoardError(
                f"List length ({len(l)}) must match board size ({self.size**2})"
            )
        self.board = l

    def from_string(self, s, delim=""):
        s = s.strip()
        if len(s) != self.size**2:
            raise BoardError(
                f"Line length ({len(s)}) must match board size ({self.size**2})"
            )
        s = s if delim == "" else s.replace(delim, "")
        self.board = [int(x) if x in self.str_nums else self.empty_char for x in s]

    def from_square_csv(self, path, delim=","):
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

    def as_string(self, board=None, row_delim="", col_delim=""):
        board = self.board if board is None else board
        rows = self.get_rows(board)
        return row_delim.join(col_delim.join(map(str, row)) for row in rows)

    def idx(self, row, col):
        return row * self.size + col

    def get_cell(self, row, col, board=None):
        board = self.board if board is None else board
        try:
            return board[self.idx(row, col)]
        except IndexError:
            raise BoardError(f"Cell at row {row}, column {col} is out of bounds")

    def set_cell(self, row, col, value, board=None):
        if value not in self.nums:
            raise BoardError(f"Invalid value {value}")
        if self.get_cell(row, col) != self.empty_char:
            raise CellSolvedException(f"Cell {row}, {col} already solved")
        board = self.board if board is None else board
        board[self.idx(row, col)] = value

    def get_col(self, col, board=None):
        return [self.get_cell(r, col, board) for r in range(self.size)]

    def get_row(self, row, board=None):
        return [self.get_cell(row, c, board) for c in range(self.size)]

    def get_cols(self, board=None):
        return [self.get_col(i, board) for i in range(self.size)]

    def get_rows(self, board=None):
        return [self.get_row(i, board) for i in range(self.size)]

    def get_square(self, row, col, board=None):
        # get the square containing the cell at row, col
        start_row = (row // self.square_size) * self.square_size
        start_col = (col // self.square_size) * self.square_size
        return [
            self.get_cell(r, c, board)
            for r in range(start_row, start_row + self.square_size)
            for c in range(start_col, start_col + self.square_size)
        ]

    def num_in_col(self, col, num, board=None):
        return num in self.get_col(col, board)

    def num_in_row(self, row, num, board=None):
        return num in self.get_row(row, board)

    def num_in_square(self, row, col, num, board=None):
        return num in self.get_square(row, col, board)

    def is_component_solved(self, component):
        # component should be a list (i.e., from get_col, get_row, or get_square)
        if len(set(component)) != len(component):
            return False
        if any(x not in component for x in self.nums):
            return False
        return True

    def check_board_solved(self):
        print("Checking solution... ", end="")
        # check each row, column, and square
        for i in range(self.size):
            row = self.get_row(i)
            if not self.is_component_solved(row):
                print(f"mistake in row {i}: {row}")
                return False
            col = self.get_col(i)
            if not self.is_component_solved(col):
                print(f"mistake in col {i}: {col}")
                return False
        for r in range(self.square_size):
            for c in range(self.square_size):
                square = self.get_square(r * self.square_size, c * self.square_size)
                if not self.is_component_solved(square):
                    print(f"mistake in sqr {r * self.square_size + c}: {square}")
                    return False
        print("solution is correct!\n")
        return True
