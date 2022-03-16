"""Hazards in combinational circuits: correct logic with a wrong output.

A two-level circuit can produce a momentary wrong value while its inputs
change, even though every input combination maps to the right output. The cause
is timing: two paths through the circuit have different delays, so during a
transition the circuit sees an input combination that never occurs statically.

A **static hazard** is a brief glitch where the output should have stayed
constant. It happens when two adjacent minterms are covered by different terms
and no term covers both: as the input moves from one to the other, the first
term falls before the second rises.

The fix is the **consensus term**, which covers the boundary and is redundant
in the logic. That is the point worth remembering: minimising a circuit as far
as possible is exactly what introduces hazards, and removing them means adding
back a term a minimiser would delete.
"""

from __future__ import annotations

import itertools


def two_level_cover(terms, variables):
    """A circuit as a list of cubes, each a string over `0`, `1` and `-`."""
    return list(terms)


def covers(term, index, variables):
    """Whether a cube covers a row."""
    pattern = format(index, f"0{variables}b")
    return all(position == "-" or position == bit
               for position, bit in zip(term, pattern))


def evaluate(circuit, index, variables):
    """The static output of the circuit for one input combination."""
    return int(any(covers(term, index, variables) for term in circuit))


def adjacent(first, second, variables):
    """Whether two rows differ in exactly one bit."""
    return bin(first ^ second).count("1") == 1


def has_static_hazard(circuit, variables):
    """Whether some single-bit input change can glitch the output.

    The condition is checkable: find two adjacent rows where the output is one
    at both, and no single cube covers both. During the transition the circuit
    passes through a moment where neither cube holds.
    """
    for first in range(2 ** variables):
        for second in range(2 ** variables):
            if not adjacent(first, second, variables):
                continue
            if not (evaluate(circuit, first, variables)
                    and evaluate(circuit, second, variables)):
                continue
            if not any(covers(term, first, variables) and covers(term, second, variables)
                       for term in circuit):
                return True
    return False


def consensus(first, second):
    """The consensus of two cubes, or `None`.

    Defined when the cubes conflict in exactly one position: the consensus
    keeps the agreement everywhere else and drops the conflicting variable.
    It is implied by the two, so adding it changes no output.
    """
    conflicts = [index for index, (a, b) in enumerate(zip(first, second))
                 if a != "-" and b != "-" and a != b]

    if len(conflicts) != 1:
        return None

    result = []
    for index, (a, b) in enumerate(zip(first, second)):
        if index == conflicts[0]:
            result.append("-")
        elif a == "-":
            result.append(b)
        elif b == "-":
            result.append(a)
        else:
            result.append(a)

    return "".join(result)


def add_consensus(circuit, variables):
    """Add every consensus term, which removes the static hazards.

    The added terms are redundant: they cover only rows the circuit already
    covered. A minimiser removes them and reintroduces the glitch, which is why
    hazard-free design and minimal design are different goals.
    """
    extended = list(circuit)

    for first, second in itertools.combinations(circuit, 2):
        term = consensus(first, second)
        if term is not None and term not in extended:
            extended.append(term)

    return extended


def simulate_transition(circuit, start, end, variables, steps=3):
    """The output while one input bit changes, with unequal path delays.

    Modelled by evaluating each cube with its own delay: the cube losing the
    input reacts immediately and the one gaining it reacts a step later. The
    dip between them is the glitch, and a hazard-free circuit has a cube that
    holds throughout.
    """
    trace = [evaluate(circuit, start, variables)]

    for step in range(1, steps):
        active = []
        for term in circuit:
            held_before = covers(term, start, variables)
            holds_after = covers(term, end, variables)
            if held_before and holds_after:
                active.append(1)
            elif held_before:
                active.append(1 if step < 1 else 0)
            elif holds_after:
                active.append(1 if step >= 2 else 0)
        trace.append(int(any(active)))

    trace.append(evaluate(circuit, end, variables))
    return trace
