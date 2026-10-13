
"""
Simulated Annealing for Predator-Prey Ordering Optimization.

Input format:
    First line: number of vertices
    Remaining lines: predator prey

Assumption:
    An edge (a, b) means predator a must appear before prey b.

Objective:
    Maximize the number of edges satisfying this ordering constraint.
"""

from pathlib import Path
import math
import random

INPUT_FILE = "/content/input.txt"

INITIAL_TEMPERATURE = 10.0
COOLING_RATE = 0.995
MIN_TEMPERATURE = 1e-4
MAX_ITERATIONS = 200_000
RESTARTS = 5
RANDOM_SEED = 42


def read_graph(path=INPUT_FILE):
    """Read the number of vertices and directed edges."""
    with open(path, "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]

    if not lines:
        raise ValueError("input.txt is empty.")

    try:
        n = int(lines[0])
    except ValueError as exc:
        raise ValueError("The first line must contain the vertex count.") from exc

    if n < 1:
        raise ValueError("The number of vertices must be positive.")

    edges = []
    for line_number, line in enumerate(lines[1:], start=2):
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid edge on line {line_number}: {line}")

        try:
            predator, prey = map(int, parts)
        except ValueError as exc:
            raise ValueError(
                f"Invalid vertex number on line {line_number}: {line}"
            ) from exc

        if not (1 <= predator <= n and 1 <= prey <= n):
            raise ValueError(
                f"Vertex number out of range on line {line_number}: {line}"
            )

        edges.append((predator, prey))

    return n, edges


def fitness(order, edges):
    """Count the edges whose predator appears before its prey."""
    position = {vertex: index for index, vertex in enumerate(order)}
    return sum(
        position[predator] < position[prey]
        for predator, prey in edges
    )


def is_valid_permutation(order, n):
    """Check that every vertex appears exactly once."""
    return len(order) == n and set(order) == set(range(1, n + 1))


def simulated_annealing(n, edges):
    """Run Simulated Annealing and return the best solution found."""
    best_order = random.sample(range(1, n + 1), n)
    best_score = fitness(best_order, edges)
    iterations_completed = 0

    iterations_per_restart = max(1, MAX_ITERATIONS // RESTARTS)

    for _ in range(RESTARTS):
        current = random.sample(range(1, n + 1), n)
        current_score = fitness(current, edges)
        temperature = INITIAL_TEMPERATURE

        if current_score > best_score:
            best_order = current[:]
            best_score = current_score

        for _ in range(iterations_per_restart):
            if temperature < MIN_TEMPERATURE:
                break

            if best_score == len(edges):
                break

            iterations_completed += 1

            # Create a neighboring permutation by swapping two vertices.
            neighbor = current[:]
            if n >= 2:
                i, j = random.sample(range(n), 2)
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]

            neighbor_score = fitness(neighbor, edges)
            delta = neighbor_score - current_score

            # Always accept improvements; sometimes accept worse solutions.
            if delta >= 0:
                current = neighbor
                current_score = neighbor_score
            elif random.random() < math.exp(delta / temperature):
                current = neighbor
                current_score = neighbor_score

            if current_score > best_score:
                best_order = current[:]
                best_score = current_score

            temperature *= COOLING_RATE

        if best_score == len(edges):
            break

    return best_order, best_score, iterations_completed


def main():
    random.seed(RANDOM_SEED)
    n, edges = read_graph()

    best_order, best_score, iterations = simulated_annealing(n, edges)

    print("\nSimulated Annealing Results")
    print("Best ordering:", best_order)
    print(f"Fitness: {best_score}/{len(edges)}")
    print(f"Fitness percentage: {100 * best_score / len(edges):.2f}%"
          if edges else "Fitness percentage: N/A (no edges)")
    print("All constraints satisfied:", best_score == len(edges))
    print("Valid permutation:", is_valid_permutation(best_order, n))
    print("Iterations completed:", iterations)


if __name__ == "__main__":
    main()
