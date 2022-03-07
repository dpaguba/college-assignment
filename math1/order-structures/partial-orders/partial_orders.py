"""Partial orders, their diagrams, and the counts that describe them.

A partial order is a relation, so everything about it can be decided by
enumeration on a finite set: which elements cover which, where the bounds
are, how long a chain can be, and how many ways the order can be extended to
a total one. The last of those is the number that grows fastest, and it is
the reason a topological sort is a choice rather than a computation of the
order.
"""

import itertools


class Poset:
    """A finite set with a reflexive, antisymmetric, transitive relation.

    The relation is stored as given and closed reflexively and transitively
    on construction, so a caller may write down only the covering pairs.
    """

    def __init__(self, elements, relation):
        """An order over the elements, closing the given pairs."""
        self.elements = list(elements)
        self.relation = self._close(set(relation))

    def _close(self, relation):
        """The reflexive and transitive closure of the given pairs."""
        closed = set(relation) | {(item, item) for item in self.elements}
        while True:
            additions = {(left, right) for left, middle in closed
                         for other, right in closed
                         if middle == other and (left, right) not in closed}
            if not additions:
                return closed
            closed |= additions

    def leq(self, left, right):
        """Whether the first element is below or equal to the second."""
        return (left, right) in self.relation

    def less(self, left, right):
        """Whether it is strictly below."""
        return left != right and self.leq(left, right)

    def is_partial_order(self):
        """Whether the relation is reflexive, antisymmetric and transitive."""
        for left in self.elements:
            if not self.leq(left, left):
                return False
            for right in self.elements:
                if self.leq(left, right) and self.leq(right, left) and left != right:
                    return False
                for third in self.elements:
                    if (self.leq(left, right) and self.leq(right, third)
                            and not self.leq(left, third)):
                        return False
        return True

    def is_total(self):
        """Whether any two elements are comparable."""
        return all(self.leq(left, right) or self.leq(right, left)
                   for left in self.elements for right in self.elements)

    def covers(self):
        """The pairs with nothing strictly between them, which is the diagram."""
        found = set()
        for left in self.elements:
            for right in self.elements:
                if not self.less(left, right):
                    continue
                if any(self.less(left, middle) and self.less(middle, right)
                       for middle in self.elements):
                    continue
                found.add((left, right))
        return found

    def minimal(self):
        """The elements with nothing strictly below them."""
        return [item for item in self.elements
                if not any(self.less(other, item) for other in self.elements)]

    def maximal(self):
        """The elements with nothing strictly above them."""
        return [item for item in self.elements
                if not any(self.less(item, other) for other in self.elements)]

    def upper_bounds(self, left, right):
        """The elements above both."""
        return [item for item in self.elements
                if self.leq(left, item) and self.leq(right, item)]

    def lower_bounds(self, left, right):
        """The elements below both."""
        return [item for item in self.elements
                if self.leq(item, left) and self.leq(item, right)]

    def supremum(self, left, right):
        """The least upper bound, or nothing when the bounds have no least one."""
        bounds = self.upper_bounds(left, right)
        for candidate in bounds:
            if all(self.leq(candidate, other) for other in bounds):
                return candidate
        return None

    def infimum(self, left, right):
        """The greatest lower bound, or nothing."""
        bounds = self.lower_bounds(left, right)
        for candidate in bounds:
            if all(self.leq(other, candidate) for other in bounds):
                return candidate
        return None

    def longest_chain(self):
        """The size of the largest totally ordered subset."""
        best = 0
        for size in range(len(self.elements), 0, -1):
            for subset in itertools.combinations(self.elements, size):
                if all(self.leq(left, right) or self.leq(right, left)
                       for left in subset for right in subset):
                    return size
        return best

    def widest_antichain(self):
        """The size of the largest subset of pairwise incomparable elements."""
        for size in range(len(self.elements), 0, -1):
            for subset in itertools.combinations(self.elements, size):
                if all(left == right or not (self.leq(left, right)
                                             or self.leq(right, left))
                       for left in subset for right in subset):
                    return size
        return 0

    def count_linear_extensions(self):
        """How many total orders extend this one."""
        return sum(1 for order in itertools.permutations(self.elements)
                   if self._extends(order))

    def _extends(self, order):
        """Whether the sequence lists every element after everything below it."""
        position = {item: index for index, item in enumerate(order)}
        return all(position[left] <= position[right]
                   for left, right in self.relation)


def divisor_order(number):
    """The divisors of a number, ordered by divisibility."""
    divisors = [value for value in range(1, number + 1) if number % value == 0]
    return Poset(divisors, {(left, right) for left in divisors for right in divisors
                            if right % left == 0})


def subset_order(base):
    """The subsets of a set, ordered by inclusion."""
    items = sorted(base, key=str)
    subsets = []
    for size in range(len(items) + 1):
        for combination in itertools.combinations(items, size):
            subsets.append(frozenset(combination))
    return Poset(subsets, {(left, right) for left in subsets for right in subsets
                           if left <= right})


def chain_order(length):
    """The numbers below the length, ordered as usual."""
    return Poset(list(range(length)),
                 {(left, right) for left in range(length)
                  for right in range(length) if left <= right})
