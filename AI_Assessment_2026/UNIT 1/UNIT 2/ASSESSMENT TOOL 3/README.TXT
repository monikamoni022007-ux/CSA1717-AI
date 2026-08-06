# Artificial Intelligence Lab Programs

## Dry Run Test 

Implementation of A* Search Algorithm and Minimax Algorithm with Alpha-Beta Pruning using Python.

## Objective

To implement and understand two fundamental Artificial Intelligence algorithms:

* A* Search Algorithm for finding the shortest path.
* Minimax Algorithm with Alpha-Beta Pruning for game decision making.

## Programs Included

1. A* Search Algorithm
2. Minimax with Alpha-Beta Pruning

## Software Requirements

* Python 3.x
* Visual Studio Code / IDLE / PyCharm (or any Python IDE)

## Files

* `astar.py` - Implementation of the A* Search Algorithm.
* `minimax_alpha_beta.py` - Implementation of the Minimax Algorithm with Alpha-Beta Pruning.
* `README.txt` - Project description and execution details.

## Algorithms Used

### A* Search Algorithm

The A* Search Algorithm is an informed search algorithm that finds the shortest path between a start node and a goal node. It evaluates each node using:

**f(n) = g(n) + h(n)**

where:

* **g(n)** = Actual path cost from the start node.
* **h(n)** = Estimated cost (heuristic) to the goal.
* **f(n)** = Total estimated cost.

### Minimax with Alpha-Beta Pruning

The Minimax Algorithm is used in two-player games to determine the best possible move. Alpha-Beta Pruning improves efficiency by eliminating branches that cannot affect the final decision, thereby reducing the number of nodes evaluated.

## How to Run

### A* Search

```bash
python astar.py
```

### Minimax with Alpha-Beta Pruning

```bash
python minimax_alpha_beta.py
```

## Sample Input

### A* Search

Graph edges, heuristic values, start node, and goal node.

### Minimax

Enter three leaf values for the Left MIN node and three leaf values for the Right MIN node.

## Sample Output

### A* Search

* Optimal Path
* Total Path Cost

### Minimax

* Best Move for MAX
* Final Minimax Value
* Pruned Nodes (if any)

## Applications

* Robot Navigation
* GPS Route Planning
* Network Routing
* Game Playing AI
* Decision Support Systems

## Author

Monika M

## Language

Python

## License

This project is developed for educational and laboratory purposes.

