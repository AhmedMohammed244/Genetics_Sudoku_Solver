def is_valid(board, row, col, num):
    """Check if placing num in board[row][col] is valid."""
    # Check the row
    for c in range(4):
        if board[row][c] == num:
            return False

    # Check the column
    for r in range(4):
        if board[r][col] == num:
            return False

    # Check the 2x2 subgrid
    start_row, start_col = 2 * (row // 2), 2 * (col // 2)
    for r in range(start_row, start_row + 2):
        for c in range(start_col, start_col + 2):
            if board[r][c] == num:
                return False

    return True

def solve_sudoku(board):
    """Solve the 4x4 Sudoku puzzle using backtracking."""
    for row in range(4):
        for col in range(4):
            if board[row][col] == 0:  # Find an empty cell
                for num in range(1, 5):  # Try numbers 1 to 4
                    if is_valid(board, row, col, num):
                        board[row][col] = num  # Place the number

                        if solve_sudoku(board):
                            return True

                        board[row][col] = 0  # Backtrack

                return False  # No valid number found

    return True  # Solved

def print_board(board):
    """Print the 4x4 Sudoku board."""
    for row in board:
        print(" ".join(str(num) if num != 0 else "." for num in row))

# Example 4x4 Sudoku puzzle (0 represents an empty cell)
puzzle = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3],
    [0, 0, 0, 0]
]

print("Original Sudoku:")
print_board(puzzle)

if solve_sudoku(puzzle):
    print("\nSolved Sudoku:")
    print_board(puzzle)
else:
    print("\nNo solution exists!")
