"""The standard NP problems, each with a verifier and a brute force solver.

A problem is in **NP** when a proposed solution can be **checked** quickly,
even if finding one is hard. So every problem here comes in two pieces:

- ``verify(instance, certificate)``: polynomial, and this is what puts the
  problem in NP
- ``solve(instance)``: exponential search, here to produce certificates and to
  check the verifier against something

Keeping the two apart is the whole point of the definition, and it is what the
exercises ask to write down.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product


def satisfiable_verify(clauses, assignment):
    """SAT: is this assignment a model of the formula?

    Linear in the size of the formula: check each clause has a true literal.
    Finding an assignment is the hard part, and no verifier ever has to.
    """
    for clause in clauses:
        if not any(assignment.get(abs(literal), False) == (literal > 0) for literal in clause):
            return False
    return True


def satisfiable_solve(clauses, variables=None):
    """SAT by trying every assignment: 2^n, which is what DPLL exists to avoid."""
    variables = sorted(variables or {abs(literal) for clause in clauses for literal in clause})

    for values in product([False, True], repeat=len(variables)):
        assignment = dict(zip(variables, values))
        if satisfiable_verify(clauses, assignment):
            return assignment

    return None


def satisfiable_dpll(clauses, assignment=None):
    """SAT by unit propagation, pure literals and backtracking.

    The brute force version above is 2^n and exists to define the problem. This
    one is the same algorithm every real solver starts from, and it is here
    because the [Cook-Levin](../cook-levin/) encoding produces formulas with
    hundreds of variables where enumeration is hopeless and structure is
    plentiful.

    Still exponential in the worst case: SAT is NP-complete, and no rule here
    changes that. What the rules change is the typical case, and a tableau
    formula is about as far from the worst case as a formula gets.
    """
    assignment = dict(assignment or {})

    while True:
        unit = None
        for clause in clauses:
            unresolved = []
            satisfied = False

            for literal in clause:
                value = assignment.get(abs(literal))
                if value is None:
                    unresolved.append(literal)
                elif value == (literal > 0):
                    satisfied = True
                    break

            if satisfied:
                continue
            if not unresolved:
                return None
            if len(unresolved) == 1:
                unit = unresolved[0]
                break

        if unit is None:
            break
        assignment[abs(unit)] = unit > 0

    remaining = []
    for clause in clauses:
        if not any(assignment.get(abs(literal)) == (literal > 0) for literal in clause):
            remaining.append([literal for literal in clause
                              if abs(literal) not in assignment])

    if not remaining:
        return assignment
    if any(not clause for clause in remaining):
        return None

    signs = {}
    for clause in remaining:
        for literal in clause:
            signs.setdefault(abs(literal), set()).add(literal > 0)

    for variable, seen in signs.items():
        if len(seen) == 1:
            return satisfiable_dpll(clauses, {**assignment, variable: next(iter(seen))})

    variable = abs(remaining[0][0])
    for value in (True, False):
        found = satisfiable_dpll(clauses, {**assignment, variable: value})
        if found is not None:
            return found

    return None


def three_sat_verify(clauses, assignment):
    """3SAT: SAT with exactly three literals per clause.

    The restriction changes nothing about difficulty, and it changes a lot
    about convenience: reductions target 3SAT because a clause of fixed width
    is easy to encode as a graph gadget.
    """
    if any(len(clause) != 3 for clause in clauses):
        raise ValueError("3SAT wants exactly three literals per clause")
    return satisfiable_verify(clauses, assignment)


@dataclass(frozen=True)
class Graph:
    """An undirected graph as vertices and edges, for the graph problems."""

    vertices: tuple
    edges: frozenset

    @classmethod
    def of(cls, vertices, edges):
        """Build a graph, normalising each edge to a sorted pair."""
        return cls(tuple(vertices),
                   frozenset(frozenset(edge) for edge in edges))

    def adjacent(self, first, second):
        """Whether two vertices share an edge."""
        return frozenset((first, second)) in self.edges

    def neighbours(self, vertex):
        """Every vertex adjacent to this one."""
        return {other for edge in self.edges if vertex in edge
                for other in edge if other != vertex}

    def complement(self):
        """The graph with exactly the missing edges, which swaps clique and independent set."""
        return Graph.of(self.vertices,
                        [(first, second) for first, second in combinations(self.vertices, 2)
                         if not self.adjacent(first, second)])


def clique_verify(graph, size, candidate):
    """CLIQUE: are these k vertices pairwise adjacent?

    Quadratic in the size of the candidate, and independent of the graph, which
    is what makes it a certificate: the checker never searches.
    """
    if len(set(candidate)) != size:
        return False
    return all(graph.adjacent(first, second) for first, second in combinations(candidate, 2))


def clique_solve(graph, size):
    """Every subset of that size, which is exponential in the graph."""
    for candidate in combinations(graph.vertices, size):
        if clique_verify(graph, size, candidate):
            return candidate
    return None


def vertex_cover_verify(graph, size, candidate):
    """VERTEX COVER: do these k vertices touch every edge?"""
    if len(set(candidate)) > size:
        return False
    chosen = set(candidate)
    return all(edge & chosen for edge in graph.edges)


def vertex_cover_solve(graph, size):
    """Every subset of that size."""
    for candidate in combinations(graph.vertices, size):
        if vertex_cover_verify(graph, size, candidate):
            return candidate
    return None


def independent_set_verify(graph, size, candidate):
    """INDEPENDENT SET: are these k vertices pairwise non-adjacent?

    The complement of a vertex cover, and the complement graph's clique. Three
    problems, one structure, which is why the reductions between them are three
    lines each.
    """
    if len(set(candidate)) != size:
        return False
    return not any(graph.adjacent(first, second)
                   for first, second in combinations(candidate, 2))


def independent_set_solve(graph, size):
    """Every subset of that size."""
    for candidate in combinations(graph.vertices, size):
        if independent_set_verify(graph, size, candidate):
            return candidate
    return None


def hamiltonian_verify(graph, path):
    """HAMILTONIAN CYCLE: does this order visit every vertex once and close up?"""
    if sorted(path) != sorted(graph.vertices) or len(path) < 3:
        return False

    for index in range(len(path)):
        if not graph.adjacent(path[index], path[(index + 1) % len(path)]):
            return False
    return True


def hamiltonian_solve(graph):
    """Every permutation, which is n! and the reason this is the classic hard one."""
    if not graph.vertices:
        return None

    first = graph.vertices[0]
    for rest in permutations(graph.vertices[1:]):
        candidate = (first,) + rest
        if hamiltonian_verify(graph, candidate):
            return candidate
    return None


def subset_sum_verify(numbers, target, chosen):
    """SUBSET SUM: do the chosen numbers add up to the target?

    Adding is linear, which is the whole verification. Note the certificate is
    a set of **indices**, not values, because a list may repeat a number.
    """
    if any(index < 0 or index >= len(numbers) for index in chosen):
        return False
    if len(set(chosen)) != len(chosen):
        return False
    return sum(numbers[index] for index in chosen) == target


def subset_sum_solve(numbers, target):
    """Every subset: 2^n. The dynamic programming version is pseudo-polynomial."""
    for size in range(len(numbers) + 1):
        for chosen in combinations(range(len(numbers)), size):
            if subset_sum_verify(numbers, target, chosen):
                return chosen
    return None


def knapsack_verify(items, capacity, value, chosen):
    """KNAPSACK as a decision problem: weight within capacity and value at least v.

    The optimisation version asks for the best value; the decision version asks
    whether a given value is reachable. NP-completeness is stated for decision
    problems, and this is the standard way to turn one into the other.
    """
    if any(index < 0 or index >= len(items) for index in chosen):
        return False
    weight = sum(items[index][0] for index in chosen)
    worth = sum(items[index][1] for index in chosen)
    return weight <= capacity and worth >= value


def knapsack_solve(items, capacity, value):
    """Every subset."""
    for size in range(len(items) + 1):
        for chosen in combinations(range(len(items)), size):
            if knapsack_verify(items, capacity, value, chosen):
                return chosen
    return None


def tsp_verify(distances, budget, tour):
    """TRAVELLING SALESMAN, decision version: is there a tour within the budget?"""
    count = len(distances)
    if sorted(tour) != list(range(count)):
        return False

    total = sum(distances[tour[index]][tour[(index + 1) % count]] for index in range(count))
    return total <= budget


def tsp_solve(distances, budget):
    """Every permutation."""
    count = len(distances)
    if count < 2:
        return None

    for rest in permutations(range(1, count)):
        tour = (0,) + rest
        if tsp_verify(distances, budget, tour):
            return tour
    return None


CATALOGUE = {
    "SAT": (satisfiable_verify, satisfiable_dpll),
    "3SAT": (three_sat_verify, None),
    "CLIQUE": (clique_verify, clique_solve),
    "VERTEX COVER": (vertex_cover_verify, vertex_cover_solve),
    "INDEPENDENT SET": (independent_set_verify, independent_set_solve),
    "HAMILTONIAN CYCLE": (hamiltonian_verify, hamiltonian_solve),
    "SUBSET SUM": (subset_sum_verify, subset_sum_solve),
    "KNAPSACK": (knapsack_verify, knapsack_solve),
    "TSP": (tsp_verify, tsp_solve),
}
"""Every problem here, with its verifier and its brute force solver."""
