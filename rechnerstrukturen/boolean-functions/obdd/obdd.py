"""Ordered binary decision diagrams.

A decision tree over the variables in a fixed order, with two reductions
applied until neither applies:

- **merge** identical subgraphs, so each distinct function appears once
- **remove** a node whose two children are the same node, since the variable
  does not matter there

The result is **canonical**: two functions are equal exactly when their reduced
diagrams are identical, so equivalence checking becomes a pointer comparison.
That property is why OBDDs took over hardware verification.

The cost is the variable order. The same function can have a linear diagram in
one order and an exponential one in another, and finding the best order is
NP-hard.
"""

from __future__ import annotations


class Node:
    """An internal node, testing one variable, or a leaf.

    The node records **which position in the variable order** it tests, not
    only the name. Removing a node whose children are equal shortens the path,
    so the depth of a node in the diagram is no longer its position in the
    order, and a walk that consumes one bit per level reads the wrong bits.
    """

    def __init__(self, variable, low=None, high=None, value=None, level=None):
        """Create a leaf when `value` is given, an internal node otherwise."""
        self.variable = variable
        self.low = low
        self.high = high
        self.value = value
        self.level = level

    def is_leaf(self):
        """Whether the node is a terminal."""
        return self.value is not None


def build(vector, variables):
    """The reduced diagram of a truth vector under a variable order.

    Built bottom up with a table of already-created nodes, so merging and
    removal happen at construction time rather than as a cleanup pass. That is
    how a real package does it, and it is why the diagram is canonical by
    construction rather than by a later normalisation.
    """
    unique = {}

    def make(variable, level, low, high):
        """Create or reuse a node, applying both reduction rules."""
        if low is high:
            return low
        key = (variable, id(low), id(high))
        if key not in unique:
            unique[key] = Node(variable, low, high, level=level)
        return unique[key]

    leaves = {0: Node(None, value=0), 1: Node(None, value=1)}

    def construct(depth, prefix):
        """Build the subdiagram for one prefix of assignments."""
        if depth == len(variables):
            return leaves[1 if vector[prefix] else 0]
        low = construct(depth + 1, prefix << 1)
        high = construct(depth + 1, (prefix << 1) | 1)
        return make(variables[depth], depth, low, high)

    return construct(0, 0)


def evaluate(diagram, index, variables):
    """Follow a path through the diagram for one row of the truth table.

    Each node says which position it tests, so a removed node simply does not
    appear on the path. Reading one bit per step instead would go wrong for
    exactly the functions the reduction helps most.
    """
    bits = format(index, f"0{variables}b")
    node = diagram

    while not node.is_leaf():
        node = node.high if bits[node.level] == "1" else node.low

    return bool(node.value)


def size(diagram):
    """How many distinct nodes the diagram has."""
    seen = set()

    def walk(node):
        """Count each node once."""
        if id(node) in seen:
            return
        seen.add(id(node))
        if not node.is_leaf():
            walk(node.low)
            walk(node.high)

    walk(diagram)
    return len(seen)


def canonical_form(diagram):
    """A hashable description of the diagram, for comparing two of them."""
    memo = {}

    def walk(node):
        """Describe a node by its variable and its children's descriptions."""
        if id(node) in memo:
            return memo[id(node)]
        if node.is_leaf():
            result = ("leaf", node.value)
        else:
            result = (node.variable, node.level, walk(node.low), walk(node.high))
        memo[id(node)] = result
        return result

    return walk(diagram)


def equivalent(first, second, variables):
    """Whether two truth vectors denote the same function.

    Decided by comparing the canonical forms, which is the operation OBDDs
    exist for. On a shared diagram it is a pointer comparison and takes no time
    at all; here the two are built separately, so the comparison walks them.
    """
    return canonical_form(build(first, variables)) \
        == canonical_form(build(second, variables))


def satisfiable(diagram):
    """Whether some assignment reaches the one leaf.

    Linear in the diagram, which is why satisfiability is easy once an OBDD
    exists and hard before: the whole difficulty moved into building the
    diagram, which can be exponential.
    """
    seen = set()

    def walk(node):
        """Look for a path to the one leaf."""
        if id(node) in seen:
            return False
        seen.add(id(node))
        if node.is_leaf():
            return bool(node.value)
        return walk(node.low) or walk(node.high)

    return walk(diagram)


def truth_vector(function, variables):
    """The truth vector of a Python function, for building a diagram."""
    return [int(bool(function(*[(index >> (variables - 1 - position)) & 1
                               for position in range(variables)])))
            for index in range(2 ** variables)]


def count_satisfying(diagram, variables):
    """How many assignments the function accepts.

    Counted by one walk with memoisation rather than by enumeration, which is
    the other operation OBDDs make cheap: the count of a diagram with a hundred
    variables is a walk of its nodes, not of its `2^100` rows.
    """
    memo = {}

    def walk(node, depth):
        """Count the accepting assignments below a node."""
        key = (id(node), depth)
        if key in memo:
            return memo[key]

        if node.is_leaf():
            result = (2 ** (variables - depth)) if node.value else 0
        else:
            skipped = node.level - depth
            result = (walk(node.low, node.level + 1)
                      + walk(node.high, node.level + 1)) * (2 ** skipped)

        memo[key] = result
        return result

    return walk(diagram, 0)
