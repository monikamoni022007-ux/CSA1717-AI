

# QUESTION 1 - WATER JUG PROBLEM USING BFS


from collections import deque

def water_jug():
    visited = set()
    queue = deque([((0, 0), [])])

    while queue:
        (a, b), path = queue.popleft()

        if a == 2:
            print("\nGoal Reached!\n")
            for state in path + [(a, b)]:
                print(state)
            return

        if (a, b) in visited:
            continue

        visited.add((a, b))

        next_states = [

            (4, b),                     # Fill 4L

            (a, 3),                     # Fill 3L

            (0, b),                     # Empty 4L

            (a, 0),                     # Empty 3L

            (a - min(a, 3 - b), b + min(a, 3 - b)),   # 4 -> 3

            (a + min(b, 4 - a), b - min(b, 4 - a))    # 3 -> 4

        ]

        for state in next_states:

            if state not in visited:
                queue.append((state, path + [(a, b)]))

water_jug()

print("\n")


# QUESTION 2 - MARS ROVER AGENT




class MarsRover:

    def move(self):
        print("Moving Forward")

    def turn(self):
        print("Turning Left")

    def capture(self):
        print("Capturing Image")

    def collect(self):
        print("Collecting Rock Sample")

    def analyse(self):
        print("Analyzing Sample")

    def transmit(self):
        print("Sending Data to Earth")


rover = MarsRover()

rover.move()
rover.turn()
rover.capture()
rover.collect()
rover.analyse()
rover.transmit()

print("\n")



# QUESTION 3 - 8 QUEENS USING BACKTRACKING


N = 8

board = [[0 for i in range(N)] for j in range(N)]

def safe(row, col):

    for i in range(col):
        if board[row][i]:
            return False

    i = row
    j = col

    while i >= 0 and j >= 0:

        if board[i][j]:
            return False

        i -= 1
        j -= 1

    i = row
    j = col

    while i < N and j >= 0:

        if board[i][j]:
            return False

        i += 1
        j -= 1

    return True


def solve(col):

    if col >= N:
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
    print(row)

print("\n")



# QUESTION 4 - OLA CAB BOOKING=




pickup = input("Enter Pickup Location : ")
destination = input("Enter Destination : ")

cabs = {

    "Mini":150,

    "Micro":120,

    "Sedan":250,

    "Shared":100,

    "Prime":300

}

print("\nAvailable Cabs\n")

for cab in cabs:
    print(cab, " - ₹", cabs[cab])

choice = input("\nSelect Cab : ")

print("\nBooking Confirmed")
print("-------------------------")
print("Pickup :", pickup)
print("Destination :", destination)
print("Cab :", choice)
print("Fare : ₹", cabs[choice])

print("\n")


# QUESTION 5 - UNIFORM COST SEARCH




import heapq

graph = {

'S':[('A',1),('G',12)],

'A':[('B',3),('C',1)],

'B':[('D',3)],

'C':[('D',1),('G',2)],

'D':[('G',3)],

'G':[]

}


def ucs(start, goal):

    pq = [(0, start, [start])]

    visited = set()

    while pq:

        cost, node, path = heapq.heappop(pq)

        if node == goal:
            return cost, path

        if node in visited:
            continue

        visited.add(node)

        for neighbour, weight in graph[node]:

            if neighbour not in visited:

                heapq.heappush(

                    pq,

                    (cost + weight, neighbour, path + [neighbour])

                )

cost, path = ucs('S', 'G')

print("\nLeast Cost Path")

print(" -> ".join(path))

print("Minimum Cost =", cost)

print("\n")
print("=" * 60)
print("ALL PROGRAMS EXECUTED SUCCESSFULLY")
print("=" * 60)