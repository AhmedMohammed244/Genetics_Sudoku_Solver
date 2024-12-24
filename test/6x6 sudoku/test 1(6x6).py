def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    # Check the row
    for c in range(6):
        if board[row][c] == num:
            return False

    # Check the column
    for r in range(6):
        if board[r][col] == num:
            return False

    # Check the 2x3 subgrid
    start_row, start_col = 2 * (row // 2), 3 * (col // 3)
    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 3):
            if board[r][c] == num:
                return False

    return True

def solve_sudoku(board):
    """Solve the 6x6 Sudoku puzzle using backtracking."""
    for row in range(6):
        for col in range(6):
            if board[row][col] == 0:  # Find an empty cell
                for num in range(1, 7):  # Try numbers 1 to 6
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # Place the number

                        if solve_sudoku(board):
                            return True

                        board[row][col] = 0  # Backtrack

                return False  # No valid number found

    return True  # Solved

def print_board(board):
    """Print the 6x6 Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# Example 6x6 Sudoku puzzle (0 represents an empty cell)
puzzle = [
    [0, 0, 3, 0, 1, 0],
    [5, 6, 0, 3, 2, 0],
    [0, 5, 4, 2, 0, 3],
    [2, 0, 6, 4, 5, 0],
    [0, 1, 2, 0, 4, 5],
    [0, 4, 0, 1, 0, 0]
]

print("Original Sudoku:")
print_board(puzzle)

if solve_sudoku(puzzle):
    print("\nSolved Sudoku:")
    print_board(puzzle)
else:
    print("\nNo solution exists!")
