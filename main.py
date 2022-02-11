import glob
from puzzle import Puzzle
from solvers import RecursiveNaiveSolver


if __name__ == "__main__":
    test_dir = "tests"
    test_files = [
        f for f in glob.glob(f"{test_dir}/*.*") if not f.startswith(f"{test_dir}/.")
    ]
    test_files.sort()

    for f in test_files:
        with open(f, "r") as fp:
            for i, line in enumerate(fp.readlines()):
                # print(f"Testing file {f} [puzzle {i}]...")
                puzzle = Puzzle()
                puzzle.from_string(line)
                solver = RecursiveNaiveSolver(puzzle, verbose=False)
                solver.run()
