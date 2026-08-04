#Question 1: Dry Run of A Search Algorithm -SOURCE CODE

import heapq

# Graph
graph = {
    'A': [('B', 2), ('C', 4)],
    'B': [('C', 3), ('D', 7), ('E', 2)],
    'C': [('E', 3)],
    'D': [('E', 2)],
    'E': [('G', 2)],
    'G': []
}

# Heuristic values
heuristic = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 3,
    'E': 2,
    'G': 0
}

def astar(start, goal):
    open_list = []
    heapq.heappush(open_list, (heuristic[start], 0, start, [start]))
    visited = set()

    while open_list:
        f, g, node, path = heapq.heappop(open_list)

        if node in visited:
            continue

        visited.add(node)

        print("\nCurrent Node:", node)
        print("g(n):", g)
        print("h(n):", heuristic[node])
        print("f(n):", f)

        if node == goal:
            print("\nOptimal Path:", " -> ".join(path))
            print("Total Cost:", g)
            return

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(open_list, (new_f, new_g, neighbor, path + [neighbor]))

astar('A', 'G')


#Question 2: Dry Run of Minimax with Alpha-Beta Pruning - SOURCE CODE 


import math

# Get input for left MIN node
left = list(map(int, input("Enter 3 leaf values for Left MIN (space separated): ").split()))

# Get input for right MIN node
right = list(map(int, input("Enter 3 leaf values for Right MIN (space separated): ").split()))

alpha = -math.inf
beta = math.inf

print("\n----- Left MIN Node -----")
left_value = math.inf

for value in left:
    print("Evaluating:", value)
    left_value = min(left_value, value)
    beta = min(beta, left_value)
    print("Alpha =", alpha, " Beta =", beta)

print("Selected Value of Left MIN =", left_value)

alpha = max(alpha, left_value)

print("\n----- Right MIN Node -----")
beta = math.inf
right_value = math.inf
pruned = []

for i, value in enumerate(right):
    print("Evaluating:", value)
    right_value = min(right_value, value)
    beta = min(beta, right_value)
    print("Alpha =", alpha, " Beta =", beta)

    if beta <= alpha:
        pruned = right[i+1:]
        break

print("Selected Value of Right MIN =", right_value)

print("\n----- Final Result -----")
final = max(left_value, right_value)

print("Final Minimax Value =", final)

if final == left_value:
    print("Best Move for MAX = Left Subtree")
else:
    print("Best Move for MAX = Right Subtree")

if pruned:
    print("Pruned Node(s):", pruned)
else:
    print("No Nodes Pruned")