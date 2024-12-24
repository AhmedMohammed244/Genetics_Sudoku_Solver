import random
import math

class SudokuPuzzleGenerator:
    def __init__(self, size):
        self.n = size 
        
        # Handle the subgrid size
        if self.n == 6:
            self.subgrid_rows, self.subgrid_cols = 2, 3 
        elif self.n == 12:
            self.subgrid_rows, self.subgrid_cols = 3, 4 
        elif self.n == 20:
            self.subgrid_rows, self.subgrid_cols = 4, 5 
        else:
            # for squre sudoku
            self.subgrid_rows = self.subgrid_cols = int(math.sqrt(self.n))

    def is_valid(self, board, row, col, num):
        # Check row
        if num in board[row]:
            return False
        # Check column
        if num in [board[r][col] for r in range(self.n)]:
            return False
        # Check subgrid
        start_row = (row // self.subgrid_rows) * self.subgrid_rows
        start_col = (col // self.subgrid_cols) * self.subgrid_cols
        for r in range(start_row, start_row + self.subgrid_rows):
            for c in range(start_col, start_col + self.subgrid_cols):
                if board[r][c] == num:
                    return False
        return True

    def generate_full_solution(self):
        def fill_board(board):
            for r in range(self.n):
                for c in range(self.n):
                    if board[r][c] == 0:
                        for num in random.sample(range(1, self.n + 1), self.n):
                            if self.is_valid(board, r, c, num):
                                board[r][c] = num
                                if fill_board(board):
                                    return True
                                board[r][c] = 0
                        return False
            return True

        # Initialize empty board
        board = [[0] * self.n for _ in range(self.n)]
        fill_board(board)
        return board

    def remove_values_to_create_puzzle(self, board, clues=20):
        puzzle = [row[:] for row in board]
        cells = [(r, c) for r in range(len(board)) for c in range(len(board))]
        random.shuffle(cells)

        for r, c in cells:
            if sum(row.count(0) for row in puzzle) >= (len(board) * len(board) - clues):
                break
            # Temporarily remove a value
            backup = puzzle[r][c]
            puzzle[r][c] = 0

        return puzzle



