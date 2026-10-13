
"""
Genetic Algorithm for Predator-Prey Ordering Optimization.

Input format:
    First line: number of vertices
    Remaining lines: predator prey

Assumption:
    An edge (a, b) means predator a must appear before prey b.

Objective:
    Maximize the number of edges satisfying this ordering constraint.
"""

from pathlib import Path
import random

INPUT_FILE = Path(__file__).resolve().with_name("input.txt")

POPULATION_SIZE = 100
MAX_GENERATIONS = 500
CROSSOVER_RATE = 0.8
MUTATION_RATE = 0.2
TOURNAMENT_SIZE = 3
ELITISM = 2
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


def order_crossover(parent1, parent2):
    """Order Crossover (OX), preserving valid permutations."""
    n = len(parent1)

    if n < 2:
        return parent1[:]

    left, right = sorted(random.sample(range(n), 2))
    child = [None] * n

    child[left:right + 1] = parent1[left:right + 1]
    used = set(child[left:right + 1])

    remaining_genes = [gene for gene in parent2 if gene not in used]
    remaining_positions = list(range(right + 1, n)) + list(range(left))

    for position, gene in zip(remaining_positions, remaining_genes):
        child[position] = gene

    return child


def swap_mutation(order):
    """Swap two positions in a permutation."""
    if len(order) >= 2:
        i, j = random.sample(range(len(order)), 2)
        order[i], order[j] = order[j], order[i]


def tournament_selection(population, scores):
    """Select the highest-scoring member of a random tournament."""
    candidates = random.sample(
        range(len(population)),
        min(TOURNAMENT_SIZE, len(population))
    )
    winner = max(candidates, key=lambda index: scores[index])
    return population[winner][:]


def genetic_algorithm(n, edges):
    """Run the genetic algorithm and return the best solution found."""
    population = [
        random.sample(range(1, n + 1), n)
        for _ in range(POPULATION_SIZE)
    ]

    best_order = population[0][:]
    best_score = fitness(best_order, edges)
    generations_completed = 0

    for generation in range(1, MAX_GENERATIONS + 1):
        generations_completed = generation
        scores = [fitness(order, edges) for order in population]

        ranked = sorted(
            zip(scores, population),
            key=lambda item: item[0],
            reverse=True
        )

        if ranked[0][0] > best_score:
            best_score = ranked[0][0]
            best_order = ranked[0][1][:]

        if best_score == len(edges):
            break

        next_population = [
            order[:] for _, order in ranked[:ELITISM]
        ]

        while len(next_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, scores)
            parent2 = tournament_selection(population, scores)

            if random.random() < CROSSOVER_RATE:
                child = order_crossover(parent1, parent2)
            else:
                child = parent1[:]

            if random.random() < MUTATION_RATE:
                swap_mutation(child)

            next_population.append(child)

        population = next_population

    return best_order, best_score, generations_completed


def main():
    random.seed(RANDOM_SEED)
    n, edges = read_graph()

    best_order, best_score, generations = genetic_algorithm(n, edges)

    print("\nGenetic Algorithm Results")
    print("Best ordering:", best_order)
    print(f"Fitness: {best_score}/{len(edges)}")
    print(f"Fitness percentage: {100 * best_score / len(edges):.2f}%"
          if edges else "Fitness percentage: N/A (no edges)")
    print("All constraints satisfied:", best_score == len(edges))
    print("Valid permutation:", is_valid_permutation(best_order, n))
    print("Generations completed:", generations)


if __name__ == "__main__":
    main()
