# sudoku-solver

A basic implementation of a generic 9x9 Sudoku puzzle, with helper functions and support for a variety of solvers.

## Testing

Specify a solver to use with `-s` and pass in any number of unsolved puzzle files through standard input. Puzzle files can take a variety of formats, but must have consistent and distinct row delimiters (specified with `--rd`), column delimiters (specified with `--cd`), and puzzle delimiters (specified with `--pd`).

Default input file is of the following format (one puzzle, 81 characters, per line, with numbers for given cells and any other character, like `.`, for empty cells).

```
4...3.......6..8..........1....5..9..8....6...7.2........1.27..5.3....4.9........
7.8...3.....2.1...5.........4.....263...8.......1...9..9.6....4....7.5...........
3.7.4...........918........4.....7.....16.......25..........38..9....5...2.6.....
```

## Known Issues

- `RecursiveNaiveSolver` occasionally makes a mistake on one of the `topn87` puzzles.
