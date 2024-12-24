def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    # Check the row
    for c in range(9):
        if board[row][c] == num:
            return False

    # Check the column
    for r in range(9):
        if board[r][col] == num:
            return False

    # Check the 3x3 subgrid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve_sudoku(board):
    """Solve the 9x9 Sudoku puzzle using backtracking."""
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:  # Find an empty cell
                for num in range(1, 10):  # Try numbers 1 to 9
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # Place the number

                        if solve_sudoku(board):
                            return True

                        board[row][col] = 0  # Backtrack

                return False  # No valid number found

    return True  # Solved

def print_board(board):
    """Print the 9x9 Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# Example 9x9 Sudoku puzzle (0 represents an empty cell)
puzzle = [
    [0, 9, 7, 8, 0, 0, 0, 4, 0],
    [5, 8, 0, 9, 1, 0, 0, 0, 0],
    [0, 0, 0, 2, 7, 6, 0, 5, 9],
    [3, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 5, 9, 1, 4, 0, 0, 6, 8],
    [4, 1, 6, 0, 0, 2, 9, 3, 0],
    [8, 0, 5, 0, 2, 0, 0, 9, 0],
    [0, 0, 0, 4, 5, 9, 7, 0, 3],
    [9, 3, 4, 0, 6, 8, 5, 2, 0]
]

print("Original Sudoku:")
print_board(puzzle)

if solve_sudoku(puzzle):
    print("\nSolved Sudoku:")
    print_board(puzzle)
else:
    print("\nNo solution exists!")
