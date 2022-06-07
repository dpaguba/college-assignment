"""Polynomial reductions between NP problems, executable and checked.

    A <=p B    when a polynomial f exists with   x in A  <=>  f(x) in B

Cook and Levin proved SAT is NP-complete directly, by encoding a machine's
computation as a formula. Every other completeness proof since then is a chain
of reductions from there, and the chain in this module is the one the course
walks:

    SAT  ->  3SAT  ->  CLIQUE  ->  VERTEX COVER
                   ->  INDEPENDENT SET

Each reduction here does two things: it transforms the instance, and it
transforms a **certificate** in both directions. The second half is what makes
the reduction checkable, and it is also what an exercise means by "explain the
correspondence".
"""

from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "np-problems"))

import np_problems as problems
from np_problems import Graph


def sat_to_three_sat(clauses, fresh_start=None):
    """Turn arbitrary clauses into clauses of exactly three literals.

    Four cases, and each one preserves satisfiability:

    - one literal ``(a)``: pad with two fresh variables in all four sign
      combinations, so they cannot help
    - two literals: pad with one fresh variable both ways
    - three: keep
    - more: chain them through fresh variables, so a long clause becomes a
      sequence of three-literal clauses that can only be satisfied together

    The chaining case is the interesting one. The fresh variables act as a
    carry: a satisfying assignment of the original clause fixes them, and if
    none of the original literals is true, the chain forces a contradiction.
    """
    variables = {abs(literal) for clause in clauses for literal in clause}
    fresh = fresh_start or (max(variables) + 1 if variables else 1)
    result = []

    for clause in clauses:
        literals = list(dict.fromkeys(clause))

        if len(literals) == 1:
            first, second = fresh, fresh + 1
            fresh += 2
            for signs in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
                result.append([literals[0], signs[0] * first, signs[1] * second])

        elif len(literals) == 2:
            helper = fresh
            fresh += 1
            result.append([literals[0], literals[1], helper])
            result.append([literals[0], literals[1], -helper])

        elif len(literals) == 3:
            result.append(list(literals))

        else:
            chain = list(range(fresh, fresh + len(literals) - 3))
            fresh += len(chain)

            result.append([literals[0], literals[1], chain[0]])
            for index in range(len(chain) - 1):
                result.append([-chain[index], literals[index + 2], chain[index + 1]])
            result.append([-chain[-1], literals[-2], literals[-1]])

    return result


def three_sat_to_clique(clauses):
    """Turn a 3SAT formula into a graph with a clique of size k.

    One vertex per literal occurrence, tagged with its clause. Two vertices are
    joined when they are in **different** clauses and **not contradictory**.

    A clique of size k, one per clause, then picks a literal from each clause
    with no contradiction among them, which is exactly a satisfying assignment.
    The size of the clique is the number of clauses, and that is the reduction.
    """
    vertices = []
    for index, clause in enumerate(clauses):
        for literal in clause:
            vertices.append((index, literal))

    edges = []
    for (first_clause, first_literal), (second_clause, second_literal) in combinations(vertices, 2):
        if first_clause == second_clause:
            continue
        if first_literal == -second_literal:
            continue
        edges.append(((first_clause, first_literal), (second_clause, second_literal)))

    return Graph.of(vertices, edges), len(clauses)


def clique_certificate_to_assignment(candidate, clauses):
    """Read a satisfying assignment off a clique.

    Each chosen vertex is a literal that must be true. Variables the clique
    says nothing about are set to False, which is safe: the clique already
    covers every clause.
    """
    assignment = {}
    for _, literal in candidate:
        assignment[abs(literal)] = literal > 0

    for clause in clauses:
        for literal in clause:
            assignment.setdefault(abs(literal), False)

    return assignment


def clique_to_vertex_cover(graph, size):
    """A clique of size k becomes a vertex cover of size n - k in the complement.

    The chain of the argument: a set is a clique in G exactly when it is an
    independent set in the complement, and a set is independent exactly when
    its complement is a vertex cover. Two complements and nothing else.
    """
    return graph.complement(), len(graph.vertices) - size


def cover_certificate_to_clique(cover, graph):
    """The vertices **outside** a cover of the complement form the clique."""
    return tuple(vertex for vertex in graph.vertices if vertex not in set(cover))


def three_sat_to_independent_set(clauses):
    """A 3SAT formula becomes an independent set of size k.

    One vertex per literal occurrence again. Edges join literals **inside** a
    clause, so at most one per clause can be chosen, and join contradictory
    literals across clauses, so the choice is consistent.

    It is the clique reduction with the edges inverted, which is what the
    complement relationship predicts.
    """
    vertices = []
    for index, clause in enumerate(clauses):
        for position, literal in enumerate(clause):
            vertices.append((index, position, literal))

    edges = []
    for first, second in combinations(vertices, 2):
        same_clause = first[0] == second[0]
        contradictory = first[2] == -second[2]
        if same_clause or contradictory:
            edges.append((first, second))

    return Graph.of(vertices, edges), len(clauses)


def independent_certificate_to_assignment(candidate, clauses):
    """Read a satisfying assignment off an independent set."""
    assignment = {}
    for _, _, literal in candidate:
        assignment[abs(literal)] = literal > 0

    for clause in clauses:
        for literal in clause:
            assignment.setdefault(abs(literal), False)

    return assignment


def hamiltonian_to_tsp(graph):
    """A Hamiltonian cycle becomes a travelling salesman tour within budget n.

    Distance one along an existing edge, two where there is none, and the
    budget is the number of vertices. A tour of that cost can only use real
    edges, so it is a Hamiltonian cycle, and the reduction is one table.

    This is also where the approximation story starts: TSP with the triangle
    inequality has a 3/2 approximation, and general TSP has none unless P = NP,
    precisely because of this reduction.
    """
    order = list(graph.vertices)
    index = {vertex: position for position, vertex in enumerate(order)}
    count = len(order)

    distances = [[0 if first == second else (1 if graph.adjacent(order[first], order[second]) else 2)
                  for second in range(count)] for first in range(count)]

    return distances, count, order


def tour_to_cycle(tour, order):
    """Translate a tour of the distance matrix back into a cycle of the graph."""
    return tuple(order[position] for position in tour)


def check(reduction_name, instance_in_a, instance_in_b, samples):
    """Report whether the yes-instances line up on a list of samples."""
    rows = []
    for sample in samples:
        left = instance_in_a(sample)
        right = instance_in_b(sample)
        rows.append({"sample": sample, "in A": left, "f(x) in B": right,
                     "agrees": left == right})

    return all(row["agrees"] for row in rows), rows


CHAIN = [
    ("SAT", "3SAT", "pad or chain clauses to exactly three literals"),
    ("3SAT", "CLIQUE", "a vertex per literal, edges between compatible literals "
                       "of different clauses, clique size = number of clauses"),
    ("CLIQUE", "VERTEX COVER", "complement the graph and the set"),
    ("3SAT", "INDEPENDENT SET", "the clique reduction with the edges inverted"),
    ("HAMILTONIAN CYCLE", "TSP", "distance 1 on edges, 2 elsewhere, budget n"),
]
"""The reductions in this module, in the order the course builds them."""
