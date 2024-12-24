import random
# Copy puzzle into board
board = [
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 3],
    [0, 0, 0, 0]
]

# Fill empty cells
for r in range(4):
    empty_cells = [c for c in range(4) if board[r][c] == 0]
    for c in empty_cells:
        possible_values = set(range(1, 5))
        
        # Eliminate values from the same row and column
        for i in range(4):
            print("r= ", r, "c= ", c, "i= ", i)
            possible_values.discard(board[r][i])  # Row values
            print("possible value after row:", possible_values)
            possible_values.discard(board[i][c])  # Column values
            print("possible value after col:", possible_values)
        
        # Eliminate values from the same subgrid
        start_row, start_col = (r // 2) *2, (c // 2) *2
        for rr in range(start_row, start_row + 2):
            for cc in range(start_col, start_col + 2):
                possible_values.discard(board[rr][cc])
                print("possible value after subgrid:", possible_values)
                
        
        # Fill the cell with a random valid value if possible
        if possible_values:
            board[r][c] = random.choice(list(possible_values))
        
        # Print the board state after filling each cell
        print(f"After filling cell ({r}, {c}):")
        for row in board:
            print(" ".join(str(num) if num != 0 else "." for num in row))
        print("-" * 40)
