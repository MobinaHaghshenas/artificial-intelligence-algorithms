# Predator–Prey Ordering Optimization

This project explores two metaheuristic algorithms for finding an ordering of vertices in a directed graph under predator–prey precedence constraints:

- **Genetic Algorithm (GA)**
- **Simulated Annealing (SA)**

The implementations optimize the same objective function so that their solution scores can be compared on the same input.

## Problem Definition

The input represents a directed graph. The first line contains the number of vertices, and each subsequent line contains a pair of vertex IDs.

The code interprets each edge `a b` as a constraint that vertex `a` (the predator) must appear **before** vertex `b` (the prey) in the ordering.

The goal is to find a permutation of all vertices that satisfies as many edge constraints as possible. A perfect ordering satisfies every edge. If the graph contains directed cycles, a perfect ordering may not exist.

## Project Files

| File | Purpose |
|---|---|
| `input.txt` | Input graph: vertex count followed by directed edges. |
| `genetic_algorithm.py` | Genetic Algorithm implementation. |
| `simulated_annealing.py` | Simulated Annealing implementation. |

## Input Format

The first line specifies the number of vertices. Every remaining line contains two integers:

```text
20
1 5
1 10
2 5
...
```

For this sample, vertices are numbered from `1` to `20`. Each edge line is interpreted as `predator prey`, meaning the predator should appear earlier than the prey.

## Algorithms

### Genetic Algorithm

The Genetic Algorithm represents each candidate ordering as a permutation of the vertices. It uses:

- Random permutation-based initial population
- Fitness evaluation by counting satisfied edge constraints
- Tournament selection
- Order Crossover (OX)
- Swap mutation
- Elitism to retain top individuals
- A fixed generation limit

### Simulated Annealing

Simulated Annealing starts from a random permutation and iteratively explores neighboring orderings. A neighbor is produced by swapping two positions. Better solutions are accepted; worse solutions may be accepted according to the temperature-dependent probability. The temperature decreases over time, and the implementation uses multiple restarts.

## Objective Function

For an ordering, the fitness score is the number of input edges whose source vertex appears before their destination vertex.

```text
Fitness = satisfied edge constraints / total edge constraints
```

The scripts report the fitness count, percentage, whether all constraints are satisfied, and whether the result is a valid permutation. A valid permutation contains every vertex exactly once; it does not necessarily satisfy every graph edge.


## Running the Scripts


Run each algorithm separately from this directory:

```bash
python genetic_algorithm.py
python simulated_annealing.py
```

The scripts use only Python's standard library, so no third-party packages need to be installed.

## Observed Results

In the reported runs on the provided input, both algorithms obtained a score of **53/54 (98.15%)**:

| Metric | Genetic Algorithm | Simulated Annealing |
|---|---:|---:|
| Best reported fitness | 53/54 | 53/54 |
| Fitness percentage | 98.15% | 98.15% |
| Valid permutation | Yes | Yes |
| All edge constraints satisfied | No | No |
| Generations / iterations reported | 500 generations | 11,485 iterations |

These are the results reported for the current parameter settings and runs.


