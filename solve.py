import glob
import argparse
from puzzle import Puzzle
import solvers


if __name__ == "__main__":
    # list of available solvers
    solver_names = [x for x in dir(solvers) if "Solver" in x and x != "Solver"]

    parser = argparse.ArgumentParser(description="Solve a Sudoku puzzle")
    parser.add_argument(
        "input_files",
        nargs="+",
        help="The puzzle to solve (default format: one puzzle (81 characters) per "
        "line, with numbers for given cells and any other character for empty cells)",
    )
    parser.add_argument(
        "-s",
        default="RecursiveNaiveSolver",
        help="The solver to use",
        choices=solver_names,
    )
    parser.add_argument(
        "--pd", default="\n", help="Puzzle delimiter (default: newline)"
    )
    parser.add_argument(
        "--rd", default="", help="Row delimiter (default: empty string)"
    )
    parser.add_argument(
        "--cd", default="", help="Column delimiter (default: empty string)"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Print each step of the solution"
    )

    a = parser.parse_args()

    for path in a.input_files:
        with open(path, "r") as f:
            contents = f.read()
        puzzles = contents.split(a.pd)
        for i, puzzle_str in enumerate(puzzles):
            print(f"Testing file {path} [puzzle {i}]...")
            puzzle = Puzzle()
            puzzle.from_string(puzzle_str, row_delim=a.rd, col_delim=a.cd)
            solver_args = "puzzle, verbose=a.verbose"
            solver = eval("solvers." + a.s + f"({solver_args})")  # unsafe but who cares
            solver.run()
