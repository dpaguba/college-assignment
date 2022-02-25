"""Structural induction, checked by enumerating the structures.

A structural claim is proved by showing it for the base cases and for each
construction step. Enumerating every structure up to a depth does not replace
the proof, and it does something the proof cannot: it produces a
counterexample when the claim is false, which is the usual reason a proof
attempt fails.
"""


def trees(depth):
    """Every binary tree of at most the given depth, as nested tuples."""
    if depth == 0:
        return [None]
    smaller = trees(depth - 1)
    built = [None]
    for left in smaller:
        for right in smaller:
            built.append((left, right))
    return built


def leaves(tree):
    """How many leaves the tree has, counting the empty tree as one."""
    if tree is None:
        return 1
    return leaves(tree[0]) + leaves(tree[1])


def inner_nodes(tree):
    """How many branching nodes it has."""
    if tree is None:
        return 0
    return 1 + inner_nodes(tree[0]) + inner_nodes(tree[1])


def depth_of(tree):
    """The length of the longest path from the root."""
    if tree is None:
        return 0
    return 1 + max(depth_of(tree[0]), depth_of(tree[1]))


def balanced(term):
    """Whether the brackets of a term are balanced."""
    depth = 0
    for symbol in term:
        if symbol == "(":
            depth += 1
        elif symbol == ")":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


def symbol_count(term):
    """How many letters and digits the term contains."""
    return sum(1 for symbol in term if symbol.isalnum())


def check(structures, claim):
    """The first structure violating the claim, or nothing."""
    for structure in structures:
        if not claim(structure):
            return structure
    return None
