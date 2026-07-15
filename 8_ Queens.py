N = 8

board = [[0] * N for _ in range(N)]

def safe(row, col):
    for i in range(col):
        if board[row][i] == 1:
            return False

    i, j = row, col
    while i >= 0 and j >= 0:
        if board[i][j] == 1:
            return False
        i -= 1
        j -= 1

    i, j = row, col
    while i < N and j >= 0:
        if board[i][j] == 1:
            return False
        i += 1
        j -= 1

    return True

def solve(col):
    if col == N:
        return True

    for row in range(N):
        if safe(row, col):
            board[row][col] = 1

            if solve(col + 1):
                return True

            board[row][col] = 0

    return False

solve(0)

for row in board:
    for cell in row:
        if cell == 1:
            print("Q", end=" ")
        else:
            print(".", end=" ")
    print()