"""Bisimulation: when two worlds cannot be told apart by any modal formula.

Two worlds are bisimilar when they carry the same atoms and every step from one
can be matched by a step from the other, in both directions, forever. The point
of the definition is a theorem: bisimilar worlds satisfy exactly the same modal
formulas.

That theorem is what makes modal logic useful for transition systems. It says
the logic can only see behaviour, never the identity or the number of states,
so a system and its minimisation are indistinguishable, and so are a loop and
its infinite unwinding.
"""

from __future__ import annotations

import os
import sys

_here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_here, "..", "kripke-structures"))
sys.path.insert(0, os.path.join(_here, "..", "modal-satisfiability"))
import kripke_structures as ks


def bisimilar(first, first_world, second, second_world):
    """Whether two worlds of two structures are bisimilar.

    Computed as a greatest fixed point: start by assuming every pair with equal
    labels is related, then repeatedly remove pairs whose steps cannot be
    matched, until nothing changes. Starting from everything and shrinking is
    what makes it the **greatest** bisimulation; starting from nothing and
    growing would give the empty relation, which satisfies the definition
    vacuously and relates nothing.
    """
    relation = {(left, right)
                for left in first.worlds for right in second.worlds
                if first.labels[left] == second.labels[right]}

    changed = True
    while changed:
        changed = False
        for pair in list(relation):
            left, right = pair
            if not _matches(first, left, second, right, relation) \
                    or not _matches(second, right, first, left,
                                    {(b, a) for a, b in relation}):
                relation.discard(pair)
                changed = True

    return (first_world, second_world) in relation


def _matches(first, left, second, right, relation):
    """Whether every step from one world is matched by a step from the other."""
    for target in first.successors(left):
        if not any((target, other) in relation for other in second.successors(right)):
            return False
    return True


def unwind(structure, world, depth):
    """The tree obtained by unrolling a structure from a world.

    Every path of the original becomes its own branch, so the result is a tree
    and typically much larger. It is bisimilar to the original by construction,
    which is the point: modal logic cannot tell a cycle from its unwinding, and
    that is why the finite model property does not conflict with formulas that
    describe infinite behaviour.
    """
    worlds = []
    accessible = {}
    labels = {}

    def build(current, remaining, path):
        """Create a node for one path and recurse into its successors."""
        name = path
        worlds.append(name)
        labels[name] = set(structure.labels[current])
        accessible[name] = []

        if remaining == 0:
            return

        for index, target in enumerate(structure.successors(current)):
            child = f"{path}.{index}"
            accessible[name].append(child)
            build(target, remaining - 1, child)

    build(world, depth, "r")
    return ks.Kripke(worlds, accessible, labels)


def is_tree(structure):
    """Whether every world has at most one predecessor and there is no cycle."""
    incoming = {world: 0 for world in structure.worlds}

    for world in structure.worlds:
        for target in structure.successors(world):
            incoming[target] += 1

    if any(count > 1 for count in incoming.values()):
        return False

    roots = [world for world, count in incoming.items() if count == 0]
    return len(roots) == 1


def quotient(structure):
    """Merge bisimilar worlds, which is the smallest equivalent structure.

    The modal analogue of minimising an automaton, and the reason bisimulation
    is computed in practice: a transition system with a million states may have
    a quotient with ten, and every modal property of the first holds of the
    second.
    """
    classes = []

    for world in structure.worlds:
        for group in classes:
            if bisimilar(structure, world, structure, group[0]):
                group.append(world)
                break
        else:
            classes.append([world])

    names = {world: index for index, group in enumerate(classes) for world in group}
    accessible = {index: [] for index in range(len(classes))}
    labels = {index: set(structure.labels[group[0]]) for index, group in enumerate(classes)}

    for index, group in enumerate(classes):
        targets = set()
        for world in group:
            for target in structure.successors(world):
                targets.add(names[target])
        accessible[index] = sorted(targets)

    return ks.Kripke(list(range(len(classes))), accessible, labels)
