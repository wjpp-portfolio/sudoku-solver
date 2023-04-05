# sudoku-solver
Python Sudoku Solver

This program awaits input of an 81 character string representing game data (zero is a blank space) like the below which is an 'evil' Sudoku game from an online website.

    010000370000006082000400000003510000700908003000023900000004000820300000065000010

The solver parses this string then identifies any certain values in the game based on this configuration as well as identifying viable values for every unfilled box. A backtrack is the performed to reach either a solution or identify an impossible puzzle. The solution (or impossible puzzle) is printed to the screen at the end.
