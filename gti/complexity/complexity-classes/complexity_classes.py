"""P, NP, verifiers, and the difference between deciding and optimising.

    P    decidable by a deterministic machine in polynomial time
    NP   decidable by a nondeterministic machine in polynomial time,
         equivalently: a proposed solution can be **checked** in polynomial time

The second phrasing is the useful one. A problem is in NP when a certificate
exists that makes the answer easy to check, and the whole of
[np-problems](../np-problems/) is written in that shape: a fast verifier and a
slow search, kept apart on purpose.

P is contained in NP, because a decider is a verifier that ignores the
certificate. Whether the containment is strict is the open question, and
nothing here settles it.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from itertools import product


@dataclass
class Problem:
    """A decision problem given by a verifier, a certificate space and a solver.

    ``certificates`` produces the possible certificates for an instance, which
    is what a nondeterministic machine would guess. Its size is what makes the
    brute force search exponential while each single check stays cheap.
    """

    name: str
    verify: object
    certificates: object
    solver: object = None

    def in_np_by_search(self, instance):
        """Decide by trying every certificate, which is the definition run slowly."""
        for certificate in self.certificates(instance):
            if self.verify(instance, certificate):
                return certificate
        return None

    def check_certificate(self, instance, certificate):
        """Run the verifier once, which is the only polynomial part."""
        return self.verify(instance, certificate)

    def measure(self, instance):
        """Time the search and one verification, to show the gap.

        The verification time is essentially independent of the instance size;
        the search time is not. Printing both next to each other is the most
        direct way to see what NP is about.
        """
        started = time.perf_counter()
        certificate = self.in_np_by_search(instance)
        search = time.perf_counter() - started

        started = time.perf_counter()
        if certificate is not None:
            self.verify(instance, certificate)
        check = time.perf_counter() - started

        return {"certificate": certificate,
                "search seconds": round(search, 6),
                "verify seconds": round(check, 8),
                "certificates tried": sum(1 for _ in self.certificates(instance))}


def growth_table(problem, instances):
    """Search time against instance size, for a family of growing instances."""
    rows = []
    for label, instance in instances:
        measurement = problem.measure(instance)
        rows.append({"instance": label,
                     "certificates": measurement["certificates tried"],
                     "search seconds": measurement["search seconds"],
                     "verify seconds": measurement["verify seconds"]})
    return rows


def decision_from_optimisation(optimise, threshold_name="at least"):
    """Turn an optimisation problem into a decision problem.

    NP-completeness is defined for decision problems, and every optimisation
    problem has a decision twin: instead of "what is the best value", ask "is a
    value of at least k reachable".

    The two are equally hard up to a polynomial factor, because binary search
    over k turns a decider into an optimiser with a logarithmic number of
    calls. That is what exercise 11.4 asks to explain, and it is the reason the
    theory can talk about decision problems without losing anything.
    """
    def decide(instance, threshold):
        """The decision version: whether the optimum reaches the threshold."""
        best = optimise(instance)
        return best is not None and best >= threshold
    decide.threshold_name = threshold_name
    return decide


def optimise_by_binary_search(decide, instance, low, high):
    """Recover the optimum from a decision procedure, in a logarithmic number of calls.

    The other direction of the equivalence, and the reason "just solve the
    decision version" is not a loss of generality.
    """
    calls = 0
    best = None

    while low <= high:
        middle = (low + high) // 2
        calls += 1
        if decide(instance, middle):
            best = middle
            low = middle + 1
        else:
            high = middle - 1

    return best, calls


def polynomial_example(size):
    """Sorting: polynomial, and the contrast for everything below."""
    data = [(size - index) % (size + 1) for index in range(size)]
    started = time.perf_counter()
    sorted(data)
    return time.perf_counter() - started


def classes():
    """A summary table of what the course puts where."""
    return [
        {"class": "P", "means": "decidable in polynomial time",
         "examples": "reachability, sorting, matching, linear programming"},
        {"class": "NP", "means": "certificates checkable in polynomial time",
         "examples": "SAT, clique, vertex cover, Hamiltonian cycle, subset sum"},
        {"class": "NP-hard", "means": "every NP problem reduces to it",
         "examples": "SAT, and everything reachable from it by reduction"},
        {"class": "NP-complete", "means": "in NP and NP-hard",
         "examples": "SAT, 3SAT, clique, vertex cover, subset sum, TSP"},
        {"class": "co-NP", "means": "the complements of NP problems",
         "examples": "unsatisfiability, tautology"},
    ]
