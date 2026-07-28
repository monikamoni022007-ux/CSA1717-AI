


# QUESTION 1 - DOCTOR SHIFT ASSIGNMENT

shifts = ["Morning", "Afternoon", "Night"]



def is_valid_assignment(assign):
    
    if assign.get("D1") == "Night":
        return False

    
    if assign.get("D3") == "Morning":
        return False


    values = list(assign.values())
    if len(values) != len(set(values)):
        return False

   
    order = {"Morning": 1, "Afternoon": 2, "Night": 3}
    if "D2" in assign and "D3" in assign:
        if order[assign["D2"]] >= order[assign["D3"]]:
            return False

    return True


solution_found = False
solution = {}

def backtrack(assign):
    global solution_found, solution

    doctors = ["D1", "D2", "D3"]

    if len(assign) == 3:
        if is_valid_assignment(assign):
            solution_found = True
            solution = assign.copy()
        return

    doctor = doctors[len(assign)]

    for shift in shifts:
        assign[doctor] = shift
        if is_valid_assignment(assign):
            backtrack(assign)
        if solution_found:
            return
        del assign[doctor]




backtrack({})
print("Final Valid Schedule:")
print(solution)


# QUESTION 2: BFS in a 5x5 Grid


from collections import deque

grid = [
    [0,0,0,0,0],
    [0,1,1,0,0],
    [0,0,0,1,0],
    [0,1,0,0,0],
    [0,0,0,0,0]
]

start = (0,0)
goal = (4,4)

def bfs_grid(start, goal):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    while queue:
        node = queue.popleft()

        if node == goal:
            break

        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy

            if 0 <= nx < 5 and 0 <= ny < 5:
                if grid[nx][ny] == 0 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    parent[(nx, ny)] = node
                    queue.append((nx, ny))

    # Reconstruct path
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()

    return path




path = bfs_grid(start, goal)
print("Optimal Path:", path)
print("Cost:", len(path)-1)



# QUESTION 3: Online Uniform Cost Search (UCS)


import heapq

# 0 = free, 1 = obstacle, 2 = risky zone
grid2 = [
    [0,0,2,0,0],
    [0,1,1,0,0],
    [0,0,2,1,0],
    [0,1,0,0,2],
    [0,0,0,0,0]
]

start2 = (0,0)
goal2 = (4,4)

def cost(cell):
    if grid2[cell[0]][cell[1]] == 2:
        return 3  # risky zone cost
    return 1

def ucs(start, goal):
    pq = [(0, start)]
    visited = set()
    parent = {start: None}
    dist = {start: 0}

    directions = [(1,0),(-1,0),(0,1),(0,-1)]

    while pq:
        current_cost, node = heapq.heappop(pq)

        if node in visited:
            continue
        visited.add(node)

        if node == goal:
            break

        for dx, dy in directions:
            nx, ny = node[0] + dx, node[1] + dy

            if 0 <= nx < 5 and 0 <= ny < 5:
                if grid2[nx][ny] != 1:  # not obstacle
                    new_cost = current_cost + cost((nx, ny))

                    if (nx, ny) not in dist or new_cost < dist[(nx, ny)]:
                        dist[(nx, ny)] = new_cost
                        parent[(nx, ny)] = node
                        heapq.heappush(pq, (new_cost, (nx, ny)))

    
    path = []
    cur = goal
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    path.reverse()

    return path, dist.get(goal, None)




path3, cost3 = ucs(start2, goal2)
print("Least-Cost Path:", path3)
print("Total Cost:", cost3)